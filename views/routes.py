#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading, multiprocessing
from flask import Blueprint, render_template, current_app, Response, request, redirect

from nlp import graph
import os, re

#from core import nlp

#flaskRoutes = Decorator da function routes do Flask started em gui.py
flaskRoutes = Blueprint('routes', __name__, template_folder='views')

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
    print("GRAPH DATA FOR THE MOST COMMON RELASHIONSHIPS IS:")
    print(current_app.pairs)
    print("=============================")

    #Need to run in other thread, or else it enters in conflit with Flask
    #graph = multiprocessing.Process(target=drawGraph, args=(data, ))
    #graph.start()

    current_app.graph.addNodes(data)
    current_app.graph.configEdges()
    current_app.graph.draw()
    current_app.graph.start()

    #current_app.graph.start()
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
    print(entity + " GRAPH DATA IS:")
    
    data = current_app.pairs

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
    #globalEntities = current_app.entities

    #c=1
    #filteredData = []
    #for p in data:
    #    if c<=33:
    #        filteredData.append(p)
    ##        c+=1

    #entities={}
    entities=[]
    #for pp in filteredData:
    for pp in data:
        if pp[0][0] not in entities:
            #entities[pp[0][0]] = globalEntities[pp[0][0]]
            entities.append(pp[0][0])
        if pp[0][1] not in entities:
            #entities[pp[0][1]] = globalEntities[pp[0][1]]
            entities.append(pp[0][1])
    return render_template("index.html", pairs=data, persons=entities)


@flaskRoutes.route('/jinja', methods=['GET', 'POST'])
def jinja():
    Harry = request.args.get('heroi', None)
    Hermione = request.args.get('namorada', None)
    Ron = request.args.get('amigo', None)

    if Harry and Hermione and Ron:
        Harry = '<span class="harry">' + Harry + '</span>'
        Hermione = '<span class="hermione">' + Hermione + '</span>'
        Ron = '<span class="ron">' + Ron + '</span>'
        ready = 'True'
    else:
        ready = 'False'

    if request.method == 'POST':
        Harry = request.values.get('heroi')
        ready = 'post'

    data = current_app.pairs
    text = current_app.text

    text = text.replace('THE BOY WHO LIVED','')
    exp = r'Page \| (.*) Harry Potter and the Philosophers Stone - J.K. Rowling'
    exp2 = r'Page \| (.*) Harry Potter and the Philosophers Stone -J.K. Rowling'
    text = re.sub(exp, '', text)
    text = re.sub(exp2, '', text)
    text = text.replace('\n',' ')
    text = ' '.join(text.split())

    baseDir = current_app.baseDir
    persons=[]
    for pp in data:
        if pp[0][0] not in persons:
            persons.append(pp[0][0])
        if pp[0][1] not in persons:
            persons.append(pp[0][1])

    gerar(text, baseDir)

    return render_template("jinja.html", data="", 
        persons=persons, 
        pairs=data, 
        Harry= Harry,
        Hermione=Hermione,
        Ron=Ron,
        ready=ready)


def gerar(text, baseDir):
    #Herói
    templateText = re.sub(r'Harry Potter', '{{ Harry }}', text)
    templateText = re.sub(r'Harry(?! }})', '{{ Harry }}', templateText)
    templateText = re.sub(r'Mr\. Potter', '{{ Harry }}', templateText)

    #Namorada/o
    templateText = re.sub(r'Hermione Jean Granger', '{{ Hermione }}', templateText)
    templateText = re.sub(r'Hermione Granger(?! }})', '{{ Hermione }}', templateText)
    templateText = re.sub(r'Miss Hermione(?! }})', '{{ Hermione }}', templateText)
    templateText = re.sub(r'Miss Granger(?! }})', '{{ Hermione }}', templateText)
    templateText = re.sub(r'Hermione(?! }})', '{{ Hermione }}', templateText)

    #Melhor amigo 
    templateText = re.sub(r'Ron Weasley', '{{ Ron }}', templateText)
    templateText = re.sub(r'Mr. Weasley(?! }})', '{{ Ron }}', templateText)
    templateText = re.sub(r'Ron(?! }})', '{{ Ron }}', templateText)

    #SAFE
    templateText = templateText.replace('{{ Harry }}', '{{ Harry|safe }}')
    templateText = templateText.replace('{{ Hermione }}', '{{ Hermione|safe }}')
    templateText = templateText.replace('{{ Ron }}', '{{ Ron|safe }}')

    saveDir = os.path.join(baseDir, 'views/templates/harryPotter-template.html')
    with open(saveDir, "w") as file:
        file.write(templateText)