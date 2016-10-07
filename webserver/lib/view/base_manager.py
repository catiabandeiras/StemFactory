# -*- coding: utf-8 -*-


import pystache

from lib.file import get_web_template, get_partial_template


class BaseViewManager(object):

    formColumnLayout = 'col-xs-6 col-sm-3 col-md-2 col-lg-2'

    def __init__(self):
        #load stuff
        self.pages    = {}
        self.partials = {}
        self.load_templates()


    def load_templates(self):
        self.pages = {
            'homepage':             get_web_template('homepage'),
            'simulation.result':    get_web_template('simulation/results/profit'),
            'simulation.full':      get_web_template('simulation/full'),
            'not-implemented-yet':  get_web_template('not-implemented-yet'),
            'message':              get_web_template('message'),
            'level.1':              get_web_template('levels/level_1'),
            'level.2':              get_web_template('levels/level_2'),

        }

        self.partials = {
            'page_start':           get_partial_template('page_start'),
            'main_header':          get_partial_template('main_header'),
            'page_end':             get_partial_template('page_end'),
            'main_menu':            get_partial_template('main_menu'),

            'panel_content':        get_partial_template('panel/content'),
            'panel_tabs':           get_partial_template('panel/tabs'),

            'hidden_field':         get_partial_template('fields/hidden'),
            'combobox_field':       get_partial_template('fields/combobox'),
            'text_field':           get_partial_template('fields/text'),
        }

        self.renderer = pystache.Renderer(partials=self.partials)


    def reload(self, message=None):
        self.load_templates()
        data = {'alertType': 'success', 'alertMessage': 'Actualizado com successo'}
        return self.renderer.render(self.pages.get('message'), data, self.partials)
        #show message?


    def render_homepage(self, data):
        return self.renderer.render(self.pages.get('homepage'), data, self.partials)


    def render_full_simulation(self, data):
        return self.renderer.render(self.pages.get('simulation.full'), data, self.partials)


    def render_simulation_result(self, data):
        return self.renderer.render(self.pages.get('simulation.result'), data, self.partials)


    def render_level(self, levelNo, data):
        return self.renderer.render(self.pages.get('level.' + levelNo), data, self.partials)

    def NIY(self): return self.renderer.render(self.pages.get('not-implemented-yet'), {}, self.partials)


