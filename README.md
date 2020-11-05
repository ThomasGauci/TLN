# TLN

Ecriture d'un petit programme qui récupère des questions dans un document au format XML puis qui interroge la base de dbpedia après avoir récupérer les informations les plus importantes.
# Commenaire 
En ce qui concerne le faible taux de réponses cela est du a des erreurs du XML. En effet la plupart des query sont exactement les mêmes que ceux du XML. Cependant il reste certaine question très difficile à résoudre tel que comprendre que la femme de devient l'épouse dans la recherche. Pour améliorer ce programme il faudrait un XML plus précis sur les query ainsi qu'un meilleir dictionnaire de liason des mots

# Lancement 
```bash
git clone https://github.com/ThomasGauci/TLN.git
cd /TLN/TP
python3 tp3.py
```

# Librairies 
 - https://sparqlwrapper.readthedocs.io/en/latest/
 - https://docs.python.org/2.4/lib/sequence-matcher.html
 - https://pypi.org/project/termcolor/