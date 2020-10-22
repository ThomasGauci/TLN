import xml.etree.ElementTree as ET
import nltk
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from termcolor import colored
from difflib import SequenceMatcher
import re 
# Chargement des données
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

# Tableau contenant les relations
relations = []

# Chargement des relations dans un tableau
file = open("relations.txt","r")
for ligne in file:
    relations.append(ligne.rstrip('\n\r'))
#print(relations)

# Methode pour envoyer les requêtes sparql
def sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query()
        results.print_results()
        print()
    except:
        print(colored("ERREUR : BAD REQUEST","yellow"))


# Remplace les espaces par un _
def replace(message):
  return message.replace(" ", "_")

# Méthode permettant de chercher la relation qui ressemble syntaxematiquement au plus a notre paramètre message
def check_relations(message):
    print("Recherche de la relation machant avec : " + message)
    rel = "none"
    # Ratio prendra la valeur du ratio du mot qui match le plus avec le paramètre message
    ratio = 0
    for r in relations:
        if(SequenceMatcher(None,message,r).ratio() >= ratio):
            ratio = SequenceMatcher(None,message,r).ratio()
            rel = r
            #print(r + " " + str(ratio))
    print("Mot matchant le mieux, res : " + rel)
    # On retourne la relation qui a le meilleur ratio de ressemblance avec le paramètre message
    return rel

# Parsing du xml
tree = ET.parse('questions.xml')
dataset = tree.getroot()

# Tableau de données des questions
# list[ [STRING] , [TOKENS], [TAGS], [ENTITIES] ]
liste_questions = []
for i in range(4):
    liste_questions.append([])

# On va charger notre tableau des questions 
for questions in dataset:
    for child in questions:
        if(child.attrib.get('lang') == "en"):
            if(child.tag == "string"):
                #print("String : " + str(child.text))
                # On récupère les string
                liste_questions[0].append(child.text)
                tokens = nltk.word_tokenize(child.text)
                # On récupère les tokens
                liste_questions[1].append(tokens)
                tagged = nltk.pos_tag(tokens)
                # On récupère les tags
                liste_questions[2].append(tagged)
                # On récupère les entities
                liste_questions[3].append(nltk.chunk.ne_chunk(tagged))
for anwsers in dataset.findall('anwsers'):
    print("ee")
    print(anwsers.find('anwser').text)

# Fichier contenant toutes les query
fichier = open("evaluations.txt", "a")

# On va maintenant chercher les élements importants des questions 
for tokens in range(0): #liste_questions[2]
    #print(tokens)  
    for token in tokens:
        # Ici on s'occupe des questions commençant par "who" 3/9
        if(token[0] == "Who" or token[0] == "who"):
            print(colored(tokens,"red"))
            # res
            ressources = ""
            # dbo
            rel = ""
            for token in tokens:  
                if(token[1] == "VBD"):
                    # On cherche le verbe qui ressemble le plus aux relations (ex : created -> creator)
                    rel = check_relations(token[0])
                if(token[1] == "NNP"):
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
            # Création du query pour sparql        
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri WHERE {res:" + replace(ressources)  + " " + rel + " ?uri .}"
            print(colored("Query: " + q,"green"))
            print("\n")
            fichier.write(q + "\n")
            if (ressources != "" and rel != ""):
                sparql_query(q)
        # Ici on s'occupe des questions commençant par "When" 1/1
        if(token[0] == "When" or token[0] == "when"):
            print(colored(tokens,"red"))
            # res
            ressources = ""
            bool = False
            for token in tokens:  
                if(token[1] == "NNP"):
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    ressources += " " + token[0]
                    bool = False
                else:
                    bool = False
            # Création du query pour sparql
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?date WHERE {res:"+ replace(ressources)  +" dbo:date ?date .}"
            print(colored("Query: " + q,"green"))
            print("\n")
            fichier.write(q + "\n")
            if (ressources != "" and rel != ""):
                sparql_query(q)
        # Ici on s'occupe des questions commençant par "Which" 6/8
        if(token[0] == "Which" or token[0] == "which"):
            print(colored(tokens,"red"))
            # res
            ressources = ""
            # dbo
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
                    if(ressources == ""):
                       ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    ressources += " " + token[0]
                    bool = False
                else:
                    bool = False
            # On cherche la relation qui match le plus
            rel = check_relations(rel)
            # Création du query
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri WHERE {res:"+ replace(ressources)  + " " + rel + " ?uri .}"
            print(colored("Query: " + q,"green"))
            print("\n")
            fichier.write(q + "\n")
            if (ressources != "" and rel != ""):
                sparql_query(q)
        # Ici on s'occupe des questions commençant par "What" 4/5
        if(token[0] == "What" or token[0] == "what"):
            print(colored(tokens,"red"))
            # res
            ressources = ""
            # dbo
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
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = False
                else:
                    bool = False
            # On cherche la relation qui match le plus
            rel = check_relations(rel)
            # Création du query
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri WHERE {res:"+ replace(ressources)  + " " + rel +" ?uri .}"
            print(colored("Query: " + q,"green"))
            print("\n")
            fichier.write(q + "\n")
            if (ressources != "" and rel != ""):
                sparql_query(q)
        # Ici on s'occupe des questions commençant par "Give" 1/2
        if(token[0] == "Give" or token[0] == "give"):
            print(colored(tokens,"red"))
            # res
            ressources = ""
            # foaf
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
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = False
                else:
                    bool = False
            #rel = check_relations(rel)
            # Création du query
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?string WHERE {res:"+ replace(ressources) + " foaf:" + rel +" ?string .}"
            print(colored("Query: " + q,"green"))
            print("\n")
            fichier.write(q + "\n")
            if (ressources != "" and rel != ""):
                sparql_query(q)
        # Ici on s'occupe des questions commençant par "How" 1/1
        if(token[0] == "How" or token[0] == "how"):
            print(colored(tokens,"red"))
            # res
            ressources = ""
            # foaf
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
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = True
                elif(token[1] == "IN" and bool == True):
                    if(ressources == ""):
                        ressources += token[0]
                    else:
                        ressources += " " + token[0]
                    bool = False
                else:
                    bool = False
            rel = check_relations(rel)
            # Création du query
            q = "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?number WHERE {res:"+ replace(ressources)  + " " + rel +" ?number .}"
            print(colored("Query: " + q,"green"))
            print("\n")
            fichier.write(q + "\n")
            if (ressources != "" and rel != ""):
                sparql_query(q)
fichier.close()

# To do :
# Evaluation 
# Récupérer les anwsers
# Récupérer les questions ??