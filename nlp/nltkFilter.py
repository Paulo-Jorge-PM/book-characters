#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import nltk
from nltk import pos_tag, word_tokenize, data, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from collections import Counter
import pprint
import os

class Filter:

    def __init__(self, text):
        ### DATA
        self.text = text

        #Config NLTK base data dir i corpus pre downloaded, so the user don't need to download it
        baseDir = os.path.dirname(__file__)
        nltk_data = os.path.join(baseDir, 'nltk_data')
        data.path.append(nltk_data)

        ### PROCESS
        self.tokens = self.getTokens(self.text)
        self.tags = self.tagging(self.tokens)
        self.properNouns = self.getProperNouns(self.tags)
        self.nouns = self.summarizeText(self.properNouns, 100)

        self.bigrams = self.bigramsNouns(self.nouns)
        self.frequency = self.gramFrequency(self.text, self.nouns)
        #self.printNouns(self.nouns)

    def getTokens(self, txt):
        tokenize = word_tokenize(txt)
        return tokenize

    def tagging(self, tokens):
        tags = pos_tag(tokens)
        return tags

    def getProperNouns(self, taggedText):
        properNouns = []
        i = 0
        while i < len(taggedText):
            if taggedText[i][1] == 'NNP':
                if taggedText[i+1][1] == 'NNP':
                    properNouns.append(taggedText[i][0].lower() +
                                        " " + taggedText[i+1][0].lower())
                    i+=1 # extra increment added to the i counter to skip the next word
                else:
                    properNouns.append(taggedText[i][0].lower())
            i+=1 # increment the i counter
        return properNouns

    def summarizeText(self, properNouns, topNum):
        '''
        Counts and agreggates the data. TopNum is a int e.g. 100
        '''
        counts = dict(Counter(properNouns).most_common(topNum))
        return counts

    def bigramsNouns(self, words):
        n = 2
        ngrams = []
        for l in words:
            for i in range(n,len(l)+1):
                ngrams.append(l[i-n:i])
        return ngrams

    def gramFrequency(self, text, words):
        n = 3
        tokenized_text = [list(map(str.lower, word_tokenize(sent))) for sent in sent_tokenize(text)]
        #tokenized_text = self.tokens
        train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)
        model = MLE(n)
        model.fit(train_data, padded_sents)

        #model.counts['language'] will print how mnay times language appear
        #model.counts[['language']]['is'] #bi grams for "Language is"
        #model.counts[['language', 'is']]['never'] #trigrams

        #or to get a scroe value use scroe instead:
        #model.score('is', 'language'.split())
        #model.score('never', 'language is'.split())
        print(model.counts[['Harry']]['is'])

    def printNouns(self, nouns=None):
        if nouns == None:#this if allows it to work without invoking all the class
            nouns = self.nouns
        p = pprint.PrettyPrinter(indent=4)
        p.pprint(nouns)

if __name__ == '__main__':
    text = ""
    for line in fileinput.input():
        text += line
    Filter(text)
