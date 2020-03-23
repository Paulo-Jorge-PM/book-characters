#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, sys
import pprint
from views import gui

from nlp import characters, graph, nltkFilter

class Main:

    def __init__(self):
        self.configs = self.readConfigs()
        
        self.pairs, self.characters = self.startNLP(self.getText())
        p = pprint.PrettyPrinter(indent=4)
        #p.pprint(self.pairs)
        #print(self.pairs)

        self.gui = self.setGui()

    def readConfigs(self):
        #to do: read constants from a config file instead
        gui = "webview"
        baseDir = os.path.dirname(__file__)
        default = os.path.join(baseDir, 'data/harryPotter.txt')
        storage = os.path.join(baseDir, 'data/storage')
        return(gui, default, storage)

    def setGui(self):
        print('>Loading GUI (Webview Frame + Flask Server)...')
        if self.configs[0] == "webview":
            return gui.Gui(configs=self.configs, pairs=self.pairs, characters=self.characters)

    def getText(self):
        print('>Loading text...')
        baseDir = os.path.dirname(__file__)
        defaultText = os.path.join(baseDir, 'data/harryPotter.txt')
        text = ""
        with open(defaultText, "r") as file:
            for line in file:
                text += line
        return text

    def startNLP(self, text):
        print('>Loading NLP analysis...')
        #entities = characters.Characters(text)
        #pairs = entities.pairs
        #characters = entities.characters
        entities = characters.Characters(text)
        pairs = entities.pairs
        chars = entities.entities
        #characters = entities.entities
        

        #textNLTK = nltkFilter.Filter(text)
        #bigramsNLTK = textNLTK.bigrams
        #print(bigramsNLTK)

        sortedPairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)
        sortedchars = sorted(chars.items(), key=lambda x: x[1], reverse=True)
        return sortedPairs, sortedchars

if __name__ == '__main__':
    #sys.dont_write_bytecode = True
    main = Main()

    """baseDir = os.path.dirname(__file__)
    defaultText = os.path.join(baseDir, 'data/harryPotter.txt')

    text = ""

    with open(defaultText, "r") as file:
        for line in file:
            text += line

    p = pprint.PrettyPrinter(indent=4)

    pairs = characters.Characters(text).pairs
    entities = characters.Characters(text)
    nouns = nltkFilter.Filter(text)

    p.pprint(entities.pairs)

    sortedPairs = sorted(entities.pairs.items(), key=lambda x: x[1], reverse=True)
    graph = graph.Graph(sortedPairs)"""




    #print(sorted(entities.pairs.items(), key=lambda x: x[1]))
    #p.pprint(entities.pairs)
    #p.pprint(entities.characters)

    #nouns.printNouns()
    #print(sortedPairs)

    #main = Main()