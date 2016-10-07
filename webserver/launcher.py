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

cherrypy.config.update({'server.socket_port': 8099})
cherrypy.engine.restart()


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

        level = kwargs.get('level') or 1
        print ("loading level", level)
        data = get_level_config('level_{:0>3}'.format(level))

        return self.viewManager.render_level(level, data)


    @cherrypy.expose
    def simulation_submit(self, **kwargs):
#        print ("kwargs", kwargs)
        self.simulationParams = SimulationParams()
        self.simulationParams.update(kwargs)
#        print (self.simulationParams)
        self.simulationResult = self.__run_simulation(self.simulationParams)

#        print ("Params Text", self.simulationParams.text.val)

#        print ("Sim Result", self.simulationResult)

        try:
            old_balance = int(kwargs.get('balance'))
        except:
            old_balance = 0 #initial balance
        new_balance = old_balance + self.simulationParams.NET_PROFIT
        self.simulationResult.balance = balance

        if balance < 0: return self.viewManager.render_bankrupt(self.simulationResult)

        self.simulationResult.next_level = int(kwargs.get('level')) + 1
        data = {'params': self.simulationParams, 'results': self.simulationResult}
        if self.simulationParams.NET_PROFIT <= 0:
            self.viewManager.render_loss(data)
        #elif major profit(2 stars, 3 stars a la angry birds based on a fixed value per level?)
        else: # profit
            return self.viewManager.render_profit(data)


    def __run_simulation(self, simulationParams):
        import simpy
        from int_database import InternalDatabase
        from labsetup_new import labsetup

        db = InternalDatabase(simulationParams)
        env = simpy.Environment()
        env.process(labsetup(env, simulationParams, db))
        #env.run(until=365.25) # a year
        env.run(until=30) # a month <- make this variable
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


if __name__ == '__main__':
    viewManager = BaseViewManager()
    controller = Home(viewManager)

    cherrypy.config.update(get_web_config('global'))
    cherrypy.tree.mount(controller, '/', get_web_config('root'))

    cherrypy.engine.start()
    cherrypy.engine.block()


