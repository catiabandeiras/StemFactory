# -*- coding: utf-8 -*-

import os

import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
webrootdir = os.path.dirname(currentdir)


config = {

    "/": {
        "tools.trailing_slash.on": 0,
        "tools.staticdir.root": webrootdir
    },

    "/static": {
        "tools.staticdir.on": 1,
        "tools.staticdir.dir": "./static"

    }
}
