# Programme MS_automate_sommaire.py

## But du programme
Le programme MS_automate_sommaire.py a pour but la construction automatique du sommaire d'un numéro Medecine\Science. Le script gère:
  - la construction de la structure HTML du sommaire selon le patron disponible dans le dossier (***sommaire_patron.html***)
  - l'ajout des informations textuelles dans chacune des balises HTML du sommaire (nom des catégories, titre et auteurs de l'article)
  - la récupération et l'ajout du handle de chaque article afin d'obtenir un lien cliquable vers chaque article
 
  
## Fonctionnement du programme
Le programme python traite un tableur en format csv contenant les métadonnées d'un numéro et extrait d'iPubli.<br/>
Il est nécessaire d'ajouter dans le csv une colonne ***categorie*** informant de la catégorie de chaque article, afin de permettre au programme de générer une structure correspondant à l'organisation du sommaire.<br/>
La lecture du tableur et la récupération des métadonnées en son sein est effectuée avec la librairie [pandas](https://pandas.pydata.org/).<br/>
La construction de la structure HTML est réalisée avec le module etree de librairie python [lxml](https://pypi.org/project/lxml/).<br/>
Le programme génère un fichier xml avec une balise style contenant la feuille de style css du sommaire et une balise div contenant le sommaire en lui même.<br/>
Le résultat est à vérifier et coller dans les métadonnées de la collection traitée (numéro).

## Utilisation du programme
Pour l'utilisation du programme hors de la pipeline, se référer à la procédure procedure_MS_sommaire.txt présente au sein de ce dossier.

