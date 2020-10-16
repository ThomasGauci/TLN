import xml.etree.ElementTree as ET
import nltk
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from termcolor import colored
from difflib import SequenceMatcher
import re 

#nltk.download('maxent_ne_chunker')
#nltk.download('words')
relations = []
file = open("relations.txt","r")
for ligne in file:
    relations.append(ligne.rstrip('\n\r'))
#print(relations)
def check_relations(message):
    print(message)
    rel = "none"
    ratio = 0
    for r in relations:
        if(SequenceMatcher(None,message,r).ratio() >= ratio):
            ratio = SequenceMatcher(None,message,r).ratio()
            rel = r
            #print(r + " " + str(ratio))
    print("Res : " + rel)
    return rel

# Parsing du xml
tree = ET.parse('questions.xml')
dataset = tree.getroot()

# list[ [STRING] , [TOKENS], [TAGS], [ENTITIES] ]
liste_questions = []
for i in range(4):
    liste_questions.append([])

for questions in dataset:
    for child in questions:
        if(child.attrib.get('lang') == "en"):
            if(child.tag == "string"):
                #print("String : " + str(child.text))
                liste_questions[0].append(child.text)
                tokens = nltk.word_tokenize(child.text)
                liste_questions[1].append(tokens)
                tagged = nltk.pos_tag(tokens)
                liste_questions[2].append(tagged)
                liste_questions[3].append(nltk.chunk.ne_chunk(tagged))


for tokens in liste_questions[2]:
    #print(tokens)  
    for token in tokens:
        #Moyen demande amélioration sur le fait de trouver la relation 3/9
        if(token[0] == "WhoXX" or token[0] == "whoXX"):
            print(colored(tokens,"red"))
            ressources = ""
            rel = ""
            for token in tokens:  
                if(token[1] == "VBD"):
                    rel = check_relations(token[0])
                    # on cherche le verbe qui ressemble le plus aux relations (ex : created -> creator)
                    #savoir si on cherche une personne ou une organisation
                if(token[1] == "NNP"):
                    ressources += token[0] + " "
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri WHERE {res:" + ressources +rel+" ?uri .}"
            print(colored("Query: " + q,"green"))
            print("\n")
        #Nickel 1/1
        if(token[0] == "WhenXX" or token[0] == "whenXX"):
            print(colored(tokens,"red"))
            ressources = ""
            bool = False
            for token in tokens:  
                if(token[1] == "NNP"):
                    ressources += token[0] + " "
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    ressources += token[0] + " "
                    bool = False
                else:
                    bool = False
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?date WHERE {res:"+ ressources +"dbo:date ?date .}"
            print(colored("Query: " + q,"green"))
            print("\n")
        # Amélioration de la recherche des bon mots de la relation dans la phrase 6/8
        if(token[0] == "WhichXX" or token[0] == "whichXX"):
            print(colored(tokens,"red"))
            ressources = ""
            rel = ""
            bool = False
            for token in tokens:
                if(token[1] == "NN"):
                    rel += token[0] + " "  
                if(token[1] == "NNS"):
                    rel += token[0] + " " 
                if(token[1] == "VBG"):
                    rel += token[0] + " "
                if(token[1] == "NNP"):
                    ressources += token[0] + " "
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    ressources += token[0] + " "
                    bool = False
                else:
                    bool = False
            rel = check_relations(rel)
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?date WHERE {res:"+ ressources + rel + " ?date .}"
            print(colored("Query: " + q,"green"))
            print("\n")
        # Presque parfait voir une amélioration pour bruce carver die    4/5
        if(token[0] == "WhatXX" or token[0] == "whatXX"):
            print(colored(tokens,"red"))
            ressources = ""
            rel = ""
            bool = False
            for token in tokens:  
                if(token[1] == "NN"):
                    rel += token[0] + " "
                if(token[1] == "JJ"):
                    rel += token[0] + " "
                if(token[1] == "JJS"):
                    rel += token[0] + " "
                if(token[1] == "NNS"):
                    rel += token[0] + " "
                if(token[1] == "NNP" or token[1] == "NNPS"):
                    ressources += token[0] + " "
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    ressources += token[0] + " "
                    bool = False
                else:
                    bool = False
            rel = check_relations(rel)
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?date WHERE {res:"+ ressources + rel +" ?date .}"
            print(colored("Query: " + q,"green"))
            print("\n")
        # 1/2
        if(token[0] == "Give" or token[0] == "give"):
            print(colored(tokens,"red"))
            ressources = ""
            rel = ""
            bool = False
            for token in tokens:  
                if(token[1] == "NN"):
                    rel += token[0] + " "
                if(token[1] == "JJ"):
                    rel += token[0] + " "
                if(token[1] == "JJS"):
                    rel += token[0] + " "
                if(token[1] == "NNS"):
                    rel += token[0] + " "
                if(token[1] == "VBG"):
                    rel += token[0] + " "
                if(token[1] == "NNP" or token[1] == "NNPS"):
                    ressources += token[0] + " "
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    ressources += token[0] + " "
                    bool = False
                else:
                    bool = False
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?date WHERE {res:"+ ressources + "foaf:" + rel +" ?date .}"
            print(colored("Query: " + q,"green"))
            print("\n")




# exact match / levenshtein owst / WN similarities
# regex on cherche dans les tokens si il y a un des mots 
# WHO qui (personne ou organisation) (verbe) + (après le verbe)     X
# WHICH quel (direct après le which) groupe nominal                 X
# WHAT quoi (après the)                                             X
# WHEN quand (date) (après le verbe)                                X   
# GIVE                                                              X

# SELECT DISTINCT ?uriWHERE {res:Wikipedia dbo:author ?uri .}
#sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#ressources = "test"
#author = "test"
#q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri WHERE {res:" + ressources + "dbo:" +author+" ?uri .}"
#sparql.setQuery(q)
#sparql.setReturnFormat(JSON)
#results = sparql.query()
#results.print_results()
#print()
