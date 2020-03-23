#!/usr/bin/env python3
#sudo cp ex1 /usr/local/bin

import fileinput
import re
from nlp import nltkFilter

class Characters:

    def __init__(self, text):

        ### DATA
        self.text = text

        self.phrases = []
        self.entities = {}
        self.rawPairs = []#tuples (x,y)
        self.pairs = {}#{(pair):count}
        self.bigrams = nltkFilter.Filter(self.text).bigrams

        ### PROCESS START
        #Clean text
        self.text = self.cleanText(self.text)
        
        #Get phrases
        self.phrases = self.getPhrases(self.text)

        #Get Proper Nouns (Characters + junk)
        #self.setCharacters(self.getProperNouns(self.text))

        #Get relationships of characters that appear in same phrases (note, will repeat and have junk, after we need to clean and count)
        #We get characters here instead too
        self.getRelationships()

        #Count and clean/filter Relationships:
        self.countRelationships()

        #NLTK
        #self.filterAllNouns()

        #print(self.pairs)



    def cleanText(self, text):
        print('>Cleaning text...')
        """
        ### Delete headers e.g.: "Page | 2 Harry Potter and the Philosophers Stone - J.K. Rowling"
        ### Note: it is not always the same, some headers have "- J.K. Rowling" others "-J.K. Rowling" without space
        ### And delete line breaks, and multiple spaces
        """

        text = text.replace('THE BOY WHO LIVED','')#delete title in upper case
        exp = r'Page \| (.*) Harry Potter and the Philosophers Stone - J.K. Rowling'
        exp2 = r'Page \| (.*) Harry Potter and the Philosophers Stone -J.K. Rowling'
        text = re.sub(exp, '', text)
        text = re.sub(exp2, '', text)
        #The phrases are broken in lines, and each line starts in upper case. We dont want upper case or it will be recognized as Proper Nound
        text = text.replace('\n',' ')
        #text = text.replace('\n','{{{@lb}}}')
        #exp3 = r'{{{@lb}}}([A-Z])'
        #Send regex \1 to function so we can lower case
        #text = re.sub(exp3, regexUpper, text)
        #text = text.replace('{{{@lb}}}','')
        text = ' '.join(text.split())#Transforme multiple spaces into one
        return text


    def getPhrases(self, text):
        print('>Getting phrases...')
        #filter cases with . that could trigher a phrase stop
        alphabets= "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"

        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences


    def getProperNouns(self, text):
        prefixes = r"(Mr.|Professor|Miss|St.|Mrs.|Ms.|Dr.|mr.|mrs.)\s"
        #junk = r"(Yes|But|Dear|Fer|For|The|To|Yet|As|Given|Make|Day|Very|See|Rise|Play)\s"
        #fakeEntities = r"(Good Lord|Slytherin|Hufflepuff|Great Britain|High Table|Happy Birthday|Potters|Merry Christmas|Quidditch|Know|Who|Know Who|Stone|Sorcerer|Nimbus Two Thousand|Nimbus Two|Thousand|Defense Against|Dark arts)"
        #titles = r"(?:[A-Z][a-z]*\.\s*)?"
        name1 = r"[A-Z][a-z]+,?\s+"
        nameAbrev = r"(?:[A-Z][a-z]*\.?\s*)?"
        name2 = r"[A-Z][a-z]+"
        #exp = r'([A-Z]{1}[a-z]{1,}(\s[A-Z]{1}[a-z]{1,})?)'
        #exp = r'[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+'
        #exp = name1 + nameAbrev + name2

        #Experiments, Ignore
        #exp = r'(([A-Z]([a-z]+|\.+))+(\s[A-Z][a-z]+)+)|([A-Z]{2,})|([a-z][A-Z])[a-z]*[A-Z][a-z]*'
        #exp2 = r'^([A-Z]\.?)+$'
        #exp3 = r'[A-Z][a-z]+'
        #exp4 = r'[A-Z]\w+(?:\s[A-Z]\w+?)?\s(?:[A-Z]\w+?)?[\s\.\,\;\:\$]'
        #exp4 = r'[A-Z]\w+(?:[-\']\w+)*'
        #upperWord = r'[A-Z]\w+'

        #exp5 = r'[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+'
        exp = r'[A-Z][a-z]+\s[A-Z][a-z]+[A-Z]*[a-z]*|[A-Z][a-z]+[A-Z]*[a-z]*'

        nounsRaw = re.findall(exp, text)

        #print(nounsRaw)

        #FILTER JUNK
        nouns=[]
        #exp2 = 
        for n in nounsRaw:
            #noun = n[0].strip()
            noun = n.strip()
            #Delete Mr. Professor, etc.
            
            noun = re.sub(prefixes, '', noun)
            #noun = noun.replace("Mrs", "")
            noun = noun.replace("Mr.", "")
            #noun = noun.replace("Mr", "")
            noun = noun.replace("Miss", "")
            noun = noun.replace("Professor", "")
            noun = noun.replace("Uncle", "")
            noun = noun.replace("Aunt", "")
            noun = noun.replace("Madam", "")
            noun = noun.replace("Mrs.", "")
            #noun = noun.replace("Slytherin", "")
            #noun = noun.replace("Hufflepuff", "")
            #noun = noun.replace("You", "")
            #noun = noun.replace("Hogwarts", "")

            noun = noun.strip()
            # Make names pattern. Sometimes same name has vary forms, f.e. Rornald = Ron = Wieasly
            if noun == "Mrs. Dursley":
                noun = "Petunia"
            elif noun == "Mr. Dursley":
                noun = "Vernon"
            elif noun == "mcGonagall":
                noun = "McGonagall"
            elif noun == "Ronald" or noun == "Ronald Weasley":
                noun = "Ron"
            elif noun == "Hermione Granger" or noun == "Granger":
                noun = "Hermione"
            elif noun == "Severus Snape":
                noun = "Snape"
            elif noun == "Albus Dumbledore":
                noun = "Dumbledore"
            elif noun == "Potter" or noun == "Harry" or noun == "Harry Potted":
                noun = "Harry Potter"
            else:
                #I want all other names only by 1st name
                noun = noun.split(" ")[0]


            #Delete Junk that appears capitalized in middle of phrases like Dear, The ("The Harry Potter"), etc
            #noun = re.sub(junk, '', noun)
            #Delete fake entities like Happy Birthday (capitalized but is not a noun)
            #noun = re.sub(fakeEntities, '', noun)
            noun = noun.strip()


            #FILTER WITH BIGRAMS
            noun = self.filterNouns(noun)

            if noun != "":
                nouns.append(noun)
                #print(noun)

        return nouns

    def filterNouns(self, noun):
        ### FILTERING STRATEGIES:
        ### If the Proper Noun gas an apostrofe after, f.e. Harry's, Ron's (possessive more common in Proper Nouns)

        #afterFilters = ['’']
        afterFilters = ["weren’t", "said"] #weren’t = for Crabbe (no Mr.); "said" because of Hagrid (has not Mr.). Proper Nouns usually have verbs after
        beforeFilters = ['Mr.', 'Miss', 'Professor', 'Uncle', 'Aunt', 'Madam', 'Mrs.']
        #beforeFilters = []

        n = ""

        ## USING NLTK bigrams takes a lot of time to check all. So opted for regex instead, but this commented code works
        """for f in afterFilters:
            pair = (noun, f)
            if pair in self.bigrams:
                n = noun
                break
        

        for f in beforeFilters:
            pair = (f, noun)
            if pair in self.bigrams:
                n = noun
                break
        """

        ### oun.split(" ")[0] because full names like Harry Potter would not be counted if only Mr. Harry appeared. I want only to search 1st names
        for f in beforeFilters:
            exp = r''+f+'\s'+noun.split(" ")[0]+''

            if re.search(exp, self.text):
                n = noun
                break
            #P.e. if it has Professor Dumledor in itself not before
            elif f in noun:
                n = noun

        for f in afterFilters:
            exp = r''+noun.split(" ")[0]+'\s'+f+''
            if re.search(exp, self.text):
                n = noun
                break

        if n in ["He", "There", "It", "We", "You", "s", "Next", "She", "No", "They", "Where", "Or", "Dunno"]:
            n = ""

        return n

    """def setCharacters(self, dataset):
        entities = []
        for entity in dataset:
            if entity[0] != '' and entity[0] not in entities:
                entities.append(entity[0])
        self.entities = entities"""



    def getRelationships(self):
        print('>Getting Proper Nouns...')
        for phrase in self.phrases:
            #We dont want the 1st letter to be capitalized, because it would be detected as noun:
            phrase = phrase.strip()
            #I strip " becasue if phrase starts with "What f.e. the W will not be converted to lower case next
            phrase = phrase.strip()
            if phrase[0] == '“':
                phrase = '“' + phrase[1].lower() + phrase[2:]
            
            phrase = phrase[0].lower() + phrase[1:]

            entitiesRaw = self.getProperNouns(phrase)

            entities = []

            for char in entitiesRaw:
                if char != '':
                    #Filter it so we don't get duplicated pairs
                    if char not in entities:
                        entities.append(char)
                    #Add to the Global list totals
                    if char not in self.entities:
                        self.entities[char] = 1
                    else:
                        self.entities[char] = self.entities[char] + 1

            #If more than one character in the sentence = character is with people/friends/enemies = has relashionship
            #Make and count pairs


            #entities = ["paulo", "rui"]

            total = len(entities)
            pairs = []

            #permutas / arranjos sem repetição p.e. paulo -> manel é a mesma coisa que manel -> paulo, por isso não repete. esgota todas as possibilidades de pares
            #Logic: 
            """
            E.g. a list of 4: paulo, maria, josé, manel

            All combinations without repeating, and considering that paulo-maria = maria-paulo, will be:
            paulo-maria
            paulo-jose
            paulo-manel
            maria-jose
            maria-manel
            maria-rui
            jose-rui

            If we make it like list keys starting at 0 for each character (char)
            step 1:
            char[0], char[1]
            char[0], char[2]
            char[0], char[3]

            setp 2:
            char[1], char[2]
            char[1], char[3]

            step 3:
            char[2], char[3]

            We conclude that each step (starting at 1) is the start of the of the 2nd char in the pair, and that it always stops at total-1
            """
            for k, v in enumerate(entities):
                step = k+1
                #for i in range(total-(k+1))
                
                for i in range(total-step):
                    tempPair = (entities[k], entities[step+i])
                    if tempPair not in pairs:
                        pairs.append(tempPair)

            for p in pairs:
                if p not in self.rawPairs:
                    self.rawPairs += pairs

            #At the end there will be repeated pairs, e.g. paulo-maria = maria-paulo. This is because we only filter this inside the phrase. Later we need to clean


    def countRelationships(self):

        print('>Getting relashionships per phrase...')
        #Make pairs unique and count them
        for pair in self.rawPairs:

            #Filter and join inverse pairs: Harry - Ron is the same as Ron - Harry
            if pair[::-1] in self.pairs:
                self.pairs[pair[::-1]] = self.pairs[pair[::-1]] + 1
            else:
                if pair not in self.pairs:
                    self.pairs[pair] = 1
                else:
                    self.pairs[pair] = self.pairs[pair] + 1

           
    def filterAllNouns(self):
        #ngrams = nltk.ngrams(input_list,n=2)
        #nltk = nltkFilter.Filter(self.text)
        #rams = nltk.bigrams

        ### FILTERING STRATEGIES:
        ### If the Proper Noun gas an apostrofe after, f.e. Harry's, Ron's (possessive more common in Proper Nouns)
        #format in the original: ('Mr.', 'Harry') ou ('Harry', '’')
        #[print(x) for x in self.bigrams]
        filteredCharacters = []
        for c in self.entities:
            
            #afterFilters = ['’']
            afterFilters = ['were']
            beforeFilters = ['Mr.', 'Miss', 'Professor', 'Uncle', 'Madam', 'Mrs.']

            for f in afterFilters:
                pair = (c, f)
                if pair in self.bigrams:
                    if c not in filteredCharacters:
                        filteredCharacters.append(c)

            for f in beforeFilters:
                pair = (f, c)
                if pair in self.bigrams:
                    if c not in filteredCharacters:
                        filteredCharacters.append(c)

        print(filteredCharacters)






#Suport functions
#def regexUpper(match):
#     return match.group(1).lower()