# -*- coding: utf-8 -*-

# setting include dir to parent path
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
#sys.path.insert(0, currentdir)


#import libs
import cherrypy


from lib.file import get_web_config, get_level_config

from lib.view.base_manager import BaseViewManager
from lib.simulation.params import SimulationParams

from levelconfig import common as CommonLevelConfig

from final_cost_info import final_cost_info
#Increase the recursion limit to avoid the limits of recursion with scipy #copied
sys.setrecursionlimit(5000)


class Home(object):



    def __init__(self, viewManager):
        #load stuff
        self.viewManager = viewManager


    @cherrypy.expose
    def reload(self): #reloads views
        return self.viewManager.reload()


    @cherrypy.expose
    def index(self):
        data = {}
        return self.viewManager.render_homepage(data)


    @cherrypy.expose
    def full(self): #full simulation
        # default param type = text, if options present then it's a select
        data = get_level_config('1-start')

        return self.viewManager.render_full_simulation(data)


    @cherrypy.expose
    def scenarios(self, **kwargs):
        """scenarios / levels - there are vars that will be carried over from one level to the other."""

        print (kwargs)
        level = kwargs.get('level') or 1
        level = int(level)
        if level == 1:
            self.__initializeSession()

        print ("loading level", level)
        levelConfig = get_level_config('level_{:0>3}'.format(level))

        for assetId in ['TOTAL_WORKERS', 'TOTAL_BSC', 'TOTAL_INCUBATORS', 'TOTAL_BIOREACTORS']:
            CommonLevelConfig.set_param(levelConfig, 'factory', assetId, cherrypy.session[assetId])

        cherrypy.session['level'] = level
        levelConfig['balance'] = cherrypy.session['balance']
        return self.viewManager.render_level(levelConfig)


    @cherrypy.expose
    def simulation_submit(self, **kwargs):
#        print ("kwargs", kwargs)
        self.simulationParams = SimulationParams()
        self.simulationParams.update(kwargs)

        self.__checkPurchases(self.simulationParams)

#        print (self.simulationParams)
        self.simulationResult = self.__run_simulation(self.simulationParams)

#        print ("Params Text", self.simulationParams.text.val)

#        print ("Sim Result", self.simulationResult)

        try:
            old_balance = cherrypy.session['balance']#int(kwargs.get('balance'))
        except:
            old_balance = 0 #fail?

        self.simulationResult.set_balance(self.simulationParams.NET_PROFIT)

        new_balance = old_balance + self.simulationParams.NET_PROFIT
        cherrypy.session['balance'] = new_balance

        print ("balance", old_balance, new_balance)


        if new_balance < 0: return self.viewManager.render_bankrupt({"results": self.simulationResult})

        #self.simulationResult.next_level = int(kwargs.get('level')) + 1

        currentLevel = cherrypy.session['level']
        data = {
            'params': self.simulationParams,
            'results': self.simulationResult,
            'nextlevel': currentLevel + 1
        }

        levelConfig = get_level_config('level_{:0>3}'.format(currentLevel))

        if self.simulationResult.doses_manufactured < self.simulationParams.ANNUAL_DEMAND:
            offset = self.simulationParams.ANNUAL_DEMAND - self.simulationResult.doses_manufactured
            data['missingDemandDoses'] = offset
            data['demandNotMetPenalty'] = levelConfig['demandNotMetPenalty']['balance'] * offset
            cherrypy.session['balance']+= data['demandNotMetPenalty']
            return self.viewManager.render_demand_not_met(data)


        if self.simulationParams.NET_PROFIT <= 0:
            return self.viewManager.render_loss(data)

        #elif major profit(2 stars, 3 stars a la angry birds based on a fixed value per level?)
        else: # profit
            data['successBonus'] = levelConfig['successBonus']['balance'] * self.simulationResult.days_bf_deadline
            cherrypy.session['balance']+= data['successBonus']
            return self.viewManager.render_profit(data)


    @cherrypy.expose
    def retry(self):
        for key in ['balance', 'TOTAL_WORKERS', 'TOTAL_BSC', 'TOTAL_INCUBATORS', 'TOTAL_BIOREACTORS']:
            cherrypy.session[key] = cherrypy.session['old_{}'.format(key)]
            return self.scenarios(level=cherrypy.session['level'])



    def __run_simulation(self, simulationParams):
        import simpy
        from int_database import InternalDatabase
        from labsetup_new import labsetup

        db = InternalDatabase(simulationParams)
        env = simpy.Environment()
        env.process(labsetup(env, simulationParams, db))
        #env.run(until=365.25) # a year
        env.run(until=simulationParams.MAX_SIM_TIME) # a month <- make this variable
#        env.run(until=60) # a month <- make this variable

        #may recall this function again if already called before
        #print("ACAC - ", env.now, len(simulationParams.results.donors))
        #print("results", simulationParams.results)
        #if len(simulationParams.results.donors) == 0:
        if simulationParams.results.costStructure.costPerDose == 0:
            final_cost_info(env, simulationParams.lab, simulationParams, db)

        return simulationParams.results


    def __NIY(self): return self.viewManager.NIY()


    #set the priority according to your needs if you are hooking something
    #else on the 'before_finalize' hook point.
    @cherrypy.tools.register('before_finalize', priority=60)
    def secureheaders():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['Content-Security-Policy'] = "script-src self ajax.googleapis.com "

        port = get_web_config('global')["server.socket_port"]
        if port != 80:
            headers['Content-Security-Policy']+= "localhost:{0} 127.0.0.1:{0}".format(port) #TODO change localhost by servername


    def __initializeSession(self):
        cherrypy.session['balance'] = CommonLevelConfig.startingBalance
        cherrypy.session['AREA_FACILITY'] = 100
        cherrypy.session['TOTAL_WORKERS'] = 0
        cherrypy.session['TOTAL_BSC'] = 0
        cherrypy.session['TOTAL_INCUBATORS'] = 0
        cherrypy.session['TOTAL_BIOREACTORS'] = 0


    def __assetPurchase(self, assetId, qty):
        asset = CommonLevelConfig.get_asset(assetId)
        cherrypy.session['old_' + assetId] = cherrypy.session[assetId]
        cherrypy.session[assetId] += qty
        cherrypy.session['balance']-= qty * asset['price']
        if cherrypy.session['balance'] < 0:
            raise Exception("Not enough funds")


    def __checkPurchases(self, params):
        print ("Balance before purchases: {}".format(cherrypy.session['balance']))
        cherrypy.session['old_balance'] = cherrypy.session['balance']
        for assetId in ['TOTAL_WORKERS', 'TOTAL_BSC', 'TOTAL_INCUBATORS', 'TOTAL_BIOREACTORS']:
            submittedAmount = params.get_param(assetId)
            if cherrypy.session[assetId] < submittedAmount:
                qty = submittedAmount - cherrypy.session[assetId]
                print ("Purchasing {} {}".format(qty, assetId))
                self.__assetPurchase(assetId, qty)
                print ("balance after purchasing {} {}: {}".format(qty, assetId, cherrypy.session['balance']))

        print ("Balance after purchases: {}".format(cherrypy.session['balance']))


if __name__ == '__main__':
    viewManager = BaseViewManager()
    controller = Home(viewManager)

    cherrypy.config.update(get_web_config('global'))
    cherrypy.tree.mount(controller, '/', get_web_config('root'))

    cherrypy.engine.start()
    cherrypy.engine.block()


