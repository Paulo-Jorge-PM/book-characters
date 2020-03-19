#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading, multiprocessing
from flask import Blueprint, render_template, current_app, Response, request, redirect

from nlp import graph

#from core import nlp

#flaskRoutes = Decorator da function routes do Flask started em gui.py
flaskRoutes = Blueprint('routes', __name__)

#===General config for templates without router
#@flaskRoutes.context_processor
#def globalContext():
#    return dict()
#    return dict(default=current_app.configs[1], storage = current_app.configs[2])

#===Disable cache for all pages
@flaskRoutes.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


#===Ajax API Assíncrona
#@flaskRoutes.route('/terminal')
#def terminal():
#    os.system('gnome-terminal --working-directory=' + '"' + current_app.configs[1] + '"')
#    return Response("ok")

@flaskRoutes.route('/pairs')
def pairs():
    data = current_app.pairs

    print("=============================")
    print("=============================")
    print("GRAPH DATA FOR THE MOST COMMON RELASHIONSHIPS IS:")
    print(current_app.filteredData)
    print("=============================")
    print("=============================")

    #Need to run in other thread, or else it enters in conflit with Flask
    #graph = multiprocessing.Process(target=drawGraph, args=(data, ))
    #graph.start()

    current_app.graph.addNodes(data)
    current_app.graph.configEdges()
    current_app.graph.draw()
    current_app.graph.start()

    current_app.graph.start()
    #g = graph.Graph(data)
    #graph = threading.Thread(target=drawGraph, args=(g,))
    #graph.daemon = True
    #graph.start()

    return Response("Draw ok")

def drawGraph(data):
    #data = current_app.pairs
    g.draw()
    #g = graph.Graph(data)


@flaskRoutes.route('/pair')
def pair():
    entity = request.args.get('entity')
    print("=============================")
    print("=============================")
    print(entity + "GRAPH DATA IS:")
    data = current_app.filteredData

    newData = []
    for pp in data:
        if pp[0][0] == entity or pp[0][1] == entity:
            newData.append(pp)

    #print(newData)

    """newData = []
    for pp in data:
        if pp[0][0] == entity or pp[0][1] == entity:
            newData.append(pp)"""

    print(newData)
    print("=============================")
    print("=============================")
    
    current_app.emptyGraph.clear()
    current_app.emptyGraph.addNodes(newData)
    current_app.emptyGraph.configEdges()
    current_app.emptyGraph.draw()
    current_app.emptyGraph.start()

    #current_app.newGraph(newData)
    #g.start()

    return Response("Draw ok")

#===Pages routes
@flaskRoutes.route('/')
def index():
    #default=current_app.configs[1]
    data = current_app.pairs

    c=1
    filteredData = []
    for p in data:
        #print(p)
        if c<=33:
            filteredData.append(p)
            c+=1

    entities=[]
    for pp in filteredData:
        if pp[0][0] not in entities:
            entities.append(pp[0][0])
        if pp[0][1] not in entities:
            entities.append(pp[0][1])
    return render_template("index.html", pairs=filteredData, persons=entities)