# Programme MS_automate_XML.py

## But du programme
Le programme MS_automate_XML.py a pour but le nettoyage et l'alimentation automatique des fichiers XML des articles présents dans les lots Medecine\Sciences. Le script gère:
  - la récupération et l'ajout du pmid de l'article dans le XML au sein d'une balise **article-id pub-id-type="pmid"** dans la partie **article-meta**
  - la traduction des mots clefs MeSH indexant l'article en français et leur ajout dans le XML dans la balise **kwd-group kwd-group-type="MESH"**
  - la suppression des mentions d'images non employées (tiff, tif, small, img1)
  
## Fonctionnement du programme
Le programme python traite chaque xml présent dans un dossier lot.<br/>
La lecture et les modifications (ajouts comme suppressions de balises) dans le XML sont réalisées avec le module etree de librairie python [lxml](https://pypi.org/project/lxml/) et la librairie [minidom](https://docs.python.org/3/library/xml.dom.minidom.html).<br/>
Le script récupère d'abord le DOI de l'article présent dans les métadonnées du XML et utilise une fonction *doi2pmid* disponible dans la librairie python [metapub](https://pypi.org/project/metapub/) qui permet d'interagir avec les API de la NLM (National Librairy of Medecine des Etats Unis). Cela permet d'obtenir le pmid de l'article.<br/>
Les mots clefs MeSH sont traduits par le biais du [traducteur](http://ccsdmesh.in2p3.fr/FrenchMesh/admin/translate.jsp) associé au site du MeSH bilingue français-anglais, géré par l'IST. Il est ouvert automatiquement dans une page Web par le programme grâce à la librairie [Selenium](https://selenium-python.readthedocs.io/) et aux fichiers geckodriver.exe et chromedriver.exe fournis dans le dossier. Le programme ajoute ensuite le pmid de l'article dans le formulaire de recherche, appuyer sur le bouton de recherche et récupérer le résultat affiché dans la page html.<br/>
**A noter le temps de latence prévu à ce moment: un délai de 30 secondes permet d'attendre le résultat de la recherche, avant sa récupération par le programme.**<br/>
Dans le cas d'un délai d'attente trop long ou bien d'un gel du navigateur employé, une option a été implémentée au sein du programme et permet de basculer sur chrome au lieu de firefox. La commande est indiquée dans la procédure.<br/>
Le programme cherche et supprime ensuite les balises **graphic** qui ont pour sujet des images tiff, tif, small et img<br/>

## Utilisation du programme
Pour l'utilisation du programme hors de la pipeline, se reférer à la procédure procedure_MS_XML.txt présente au sein de ce dossier.
