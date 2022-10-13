# Programme MS_automate_file.py

## But du programme
Le programme MS_automate_file.py a pour but le nettoyage et la structuration des lots Medecine\Sciences en vue de leur importation automatique dans iPubli. Le script gère:
  - la création d'un fichier XML contenant les métadonnées en dublin core `dublin_core.xml`
  - le renommage des lots et des fichiers PDF et XML de chaque article selon la procédure de base
  - la création d'un fichier XML paramétrant l'insertion des métadonnées dans iPubli `metadata.xml`
  - la création d'un fichier content en UNIX récapitulant les éléments présents dans chaque lot: PDF, XML et images, avec leur renommage dans iPubli
  - la suppression des images non souhaitées (tif, tiff, small, img1)
 
  
## Fonctionnement du programme
Le programme python traite chaque dossier lot.<br/>
La lecture et la création de documents XML (ajouts comme suppressions de balises) sont réalisées avec le module etree de librairie python [lxml](https://pypi.org/project/lxml/).<br/>
Le script créé tout d'abord le fichier dublin_core.xml à partir des métadonnées contenues dans le XML de l'article et grâce à la feuille de transformation XSLT EDPmeta2DSpace_single2021.xsl créée par EDP Sciences et fournie dans le dossier.<br/>
Il renomme ensuite le nom du dossier lot en *item_numéro* en utilisant le numéro d'item de l'article présent dans le XML grâce à la librairie [os](https://docs.python.org/fr/3/library/os.html).<br/>
Les images non souhaitées sont repérées dans le dossier à partir de leur nom puis supprimées avec des fonctions de la librairie os.<br/>
Les noms des PDF et XML sont renommés en *MS_annee_mois_numéroItem.xml* et *MS_annee_mois_nuemroItem.PDF*. Dans le cas d'un lot Hors-Série, une option a été implémentée dans le programme afin de pouvoir les traiter en ajoutant un HS dans le nom des fichiers, voir dans la procédure Procédure_MS_file.txt.<br/>


## Utilisation du programme
Pour l'utilisation du programme hors de la pipeline, se reférer à la procédure procedure_MS_XML.txt présente au sein de ce dossier.
