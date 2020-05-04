#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, sys
import pprint
from views import gui

from nlp import characters, graph, nltkFilter

class Main:

    def __init__(self):
        self.configs = self.readConfigs()
        self.text = self.getText()
        self.pairs, self.characters = self.startNLP(self.text)
        p = pprint.PrettyPrinter(indent=4)

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
        baseDir = os.path.dirname(__file__)
        if self.configs[0] == "webview":
            return gui.Gui(configs=self.configs, pairs=self.pairs, characters=self.characters, text=self.text, dirMain=baseDir)

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
        entities = characters.Characters(text)
        pairs = entities.pairs
        chars = entities.entities


        sortedPairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)
        sortedchars = sorted(chars.items(), key=lambda x: x[1], reverse=True)
        return sortedPairs, sortedchars

if __name__ == '__main__':
    #sys.dont_write_bytecode = True
    main = Main()
