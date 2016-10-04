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
    def simulate(self, scenario=None, jsonParams=None):
        return self.viewManager.render_simulation_result(data)


    def __NIY(self): return self.viewManager.NIY()


    # set the priority according to your needs if you are hooking something
    # else on the 'before_finalize' hook point.
    @cherrypy.tools.register('before_finalize', priority=60)
    def secureheaders():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['Content-Security-Policy'] = "script-src self"


if __name__ == '__main__':
    viewManager = BaseViewManager()
    controller = Home(viewManager)

    cherrypy.config.update(get_web_config('global'))
    cherrypy.tree.mount(controller, '/', get_web_config('root'))

    cherrypy.engine.start()
    cherrypy.engine.block()


