# -*- coding: utf-8 -*-


import os, inspect, codecs
import importlib


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
webrootdir = os.path.dirname(currentdir)



def file_get_contents(relFilePath, size=100000): # ~100k
    filename = os.path.join(webrootdir, relFilePath)
    return codecs.open(filename, 'r', 'utf-8').read(size)


def get_web_template(filename):
    template = os.path.join('templates', filename) + '.html'
    return file_get_contents(template)


def get_partial_template(filename):
    return get_web_template(os.path.join('partials', filename))


def get_web_config(filename='global'):
    configModule = importlib.import_module('webconfig.{}'.format(filename))
    return configModule.config


def get_level_config(level):
    configModule = importlib.import_module('levelconfig.{}'.format(level))
    return configModule.config
