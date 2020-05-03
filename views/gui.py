#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import webview
import sys
import threading
import webview
import os

from nlp import graph

from flask import Flask, current_app
from views.routes import flaskRoutes

class Gui(Flask):
    def __init__(self, import_name=__name__, configs=None, pairs=None, characters=None, text=None, dirMain=None):
        super(Gui, self).__init__(import_name=__name__, static_folder='static', template_folder='templates')

        self.configs = configs
        self.pairs = pairs
        self.entities = characters
        self.text = text
        self.baseDir = dirMain
        #[print(x) for x in self.characters]

        #c=1
        #self.filteredData = self.pairs
        #for p in self.pairs:
        #    if c<=33:
        #        self.filteredData.append(p)
        #        c+=1

        print('>Drawing Graphs with NetworkX & Matplotlib...')
        self.emptyGraph = graph.Graph()
        self.graph = graph.Graph(self.pairs)

        #Start a Flask server in a thread
        self.server = threading.Thread(target=self.startServer)
        self.server.daemon = True
        self.server.start()

        #Start a Graph server in a thread
        #self.g = threading.Thread(target=self.threadGraph)
        #self.g.daemon = True
        #self.g.start()

        #Start weview GUI
        self.webview = self.startWebview()

    def startServer(self):
        self.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0#disable caching so it refresh the view in each start
        #self.configApp()
        self.register_blueprint(flaskRoutes)
        self.run(debug=False, threaded=False)

    def startWebview(self):
        webview.create_window("MEI", "http://127.0.0.1:5000/")
        webview.start()
        return webview

    #CONFIGURATIONS SAVE
    def configApp(self):
        self.config.update(
            gui = self.configs[0],
            default = self.configs[1],
            storage = self.configs[2]
        )

    #def threadGraph(self):
    #    self.graph = graph.Graph(self.filteredData)

    #def newGraph(self, data):
    #    graph = threading.Thread(target=startGraph, args=(data,))
    #    graph.daemon = True
    #    graph.start()

        #return g

#def startGraph(data):
#    g = graph.Graph()
#    g.addNodes(data)
#    g.configEdges()
#    g.draw()
#    g.start()