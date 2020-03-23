#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
#import pylab

SHOW_N_NODES = 100

class Graph():
    def __init__(self, dataset=None):
        
        ### DATA & INIT
        self.dataset = dataset
        self.edge_colors = None

        self.G = nx.DiGraph()
        self.clear()

        ### PROCESS
        if dataset:
            self.addNodes(self.dataset)
            self.configEdges()
            self.draw()


    def addNodes(self, dataset):
        """self.G.add_edges_from([('A', 'B'),('C','D'),('G','D')], weight=1)
        self.G.add_edges_from([('D','A'),('D','E'),('B','D'),('D','E')], weight=2)
        self.G.add_edges_from([('B','C'),('E','F')], weight=3)
        self.G.add_edges_from([('C','F')], weight=4)"""
        counter=1
        for k in dataset:
            if counter <= SHOW_N_NODES:
                #self.G.add_edges_from([k], weight=dataset[k])
                self.G.add_edges_from([k[0]], weight=k[1])
                counter+=1

    def configEdges(self, red=None):
        #red_edges = [('C','D'),('D','A')]
        if red:
            pass
        else:
            red_edges = []
        self.edge_colors = ['black' if not edge in red_edges else 'red' for edge in self.G.edges()]

    def draw(self):
        #pos=nx.spring_layout(self.G)
        pos=nx.circular_layout(self.G)
        node_labels = {node:node for node in self.G.nodes()}; nx.draw_networkx_labels(self.G, pos, labels=node_labels)
        edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in self.G.edges(data=True)])

        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=edge_labels)
        
        #nx.draw(self.G,pos, node_size=1500,edge_color=self.edge_colors,edge_cmap=plt.cm.Reds, arrows=False)
        nx.draw_circular(self.G, node_size=500, arrows=False)
        #nx.draw_circular(self.G,pos, node_size=1500,edge_color=self.edge_colors,edge_cmap=plt.cm.Reds, arrows=False)

        #This forces the plot to update, otherwise it would show old jpg until refresh
        plt.pause(0.01)

    def start(self):
        pass
        #pylab.show()

    def clear(self):
        self.G.clear()
        plt.clf()

#def startThread(data):


#Graph()
"""
G = nx.DiGraph()

G.add_edges_from([('A', 'B'),('C','D'),('G','D')], weight=1)
G.add_edges_from([('D','A'),('D','E'),('B','D'),('D','E')], weight=2)
G.add_edges_from([('B','C'),('E','F')], weight=3)
G.add_edges_from([('C','F')], weight=4)

val_map = {'A': 1.0,
                   'D': 0.5714285714285714,
                              'H': 0.0}

values = [val_map.get(node, 0.45) for node in G.nodes()]

#nx.draw(G,pos, node_color = values, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)


edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])

red_edges = [('C','D'),('D','A')]

edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]

pos=nx.spring_layout(G)
node_labels = {node:node for node in G.nodes()}; nx.draw_networkx_labels(G, pos, labels=node_labels)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
nx.draw(G,pos, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds, arrows=False)
pylab.show()
"""