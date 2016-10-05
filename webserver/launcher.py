# -*- coding: utf-8 -*-

# setting include dir to parent path
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
#sys.path.insert(0, currentdir)


#import libs
import cherrypy

from lib.file import get_web_config

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
        data = {
            'scenarios': {
                'level1': {'title' : 'Level 1' },
                'level2': {'title' : 'Level 2' }
            }
        }
        return self.viewManager.render_homepage(data)


    @cherrypy.expose
    def full(self): #full simulation
        # default param type = text, if options present then it's a select
        data = {
            'panels': [
                {
                    'id': 'factory',
                    'label': 'Factory',
                    'params': [
                        {
                            'id': 'AREA_FACILITY',
                            'label': 'Total GMP Facility Area',
                            'hidden': True,
                            'value': 400
                        },
                        {
                            'id': 'AREA_UNIT',
                            'label': 'Area unit',
                            'combobox': True,
                            'options': [
                                { 'value': '1', 'desc': 'sq. mt.'},
                                { 'value': '2', 'desc': 'sq. ft.'},
                            ]
                        },
                        {
                            'id': 'TOTAL_WORKERS',
                            'label': 'Number of workers'
                        },
                        {
                            'id': 'TOTAL_BSC',
                            'label': 'Number of BSCs'
                        },
                        {
                            'id': 'TOTAL_INCUBATORS',
                            'label': 'Number of incubators'
                        },
                        {
                            'id': 'TOTAL_BIOREACTORS',
                            'label': 'Number of bioreactor systems'
                        }
                    ]
                },
                {
                    'id': 'culture',
                    'label': 'Culture Conditions'
                },
                {
                    'id': 'growth',
                    'label': 'Growth Characteristics'
                },
                {
                    'id': 'manualOps',
                    'label': 'Manual Operations'
                },
                {
                    'id': 'manufacturing',
                    'label': 'Manufacturing Demand'
                }
            ]
        }

        return self.viewManager.render_full_simulation(data)


    @cherrypy.expose
    def submit_simulation(self, scenario=None, jsonParams=None):
        return self.viewManager.render_simulation_result(data)


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
            headers['Content-Security-Policy']+= "localhost:{}".format(port) #TODO change localhost by servername


if __name__ == '__main__':
    viewManager = BaseViewManager()
    controller = Home(viewManager)

    cherrypy.config.update(get_web_config('global'))
    cherrypy.tree.mount(controller, '/', get_web_config('root'))
    cherrypy.config.update({'server.socket_port': 8099})
    cherrypy.engine.restart()

    cherrypy.engine.start()
    cherrypy.engine.block()


