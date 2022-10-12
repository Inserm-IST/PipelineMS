# PipelineMS
Pipeline de programmes python visant à une préparation facilitée des documents à importer dans la collection [Medecine\Sciences](https://www.ipubli.inserm.fr/handle/10608/224) d'[iPubli](https://www.ipubli.inserm.fr/), l'archive ouverte institutionnelle de l'Inserm, gérée par le service de l'Information Scientifique et Technique.

## Guide d'utilisation
1) Récupération des lots fournis par EDP Sciences, éditeur de la revue Medecine\Sciences. Pour chaque magazine, ils contiennent un dossier par article composé d'un PDF de l'article, un XML du texte et des images présentées dans le texte.
2) Lancement du programme MS_automate_XML.py qui alimente automatiquement le XML de chaque article:
    - ajout du pmid
    - ajout des mots clefs MeSH traduits en français
    -suppression des images mentionnées non souhaitées
    Suivre la procédure disponible dans le dossier 1_PrepaXML
3) Lancement du programme MS_automate_file.py qui organise automatiquement la structure des fichiers à importer dans iPubli:
    - suppression des images non souhaités
    - création du fichier XML contenant les métadonnées de l'article en dublin core
    - renommage des fichiers
    - création du fichier content qui répertorie les fichiers présents dans chaque dossier article
    - création du fichier metadata.xml qui paramètre l'affichage des métadonnées dans iPubli
    Suivre la procédure disponible dans le dossier 2_PrepaFichiers
4) Ajout des lots avec le programme d'import
5) Création automatique du sommaire html de présentation du magazine
   Suivre la procédure disponible dans le dossier 3_Sommaire

## Crédits
Ce projet a été réalisé par le DISC-IST.
- Michel Pohl: Directeur adjoint du service de l'Information Scientifique et Technique de l'Inserm
- Juliette Janes: Responsable informatique du projet
- Charlotte Iizuka: Responsable éditoriale du projet
- Anna Marenelly: Soutien informatique

## Conditions d'utilisation
![68747470733a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f322e302f38387833312e706e67](https://user-images.githubusercontent.com/56683417/115525743-a78d2400-a28f-11eb-8e45-4b6e3265a527.png)

## Contacts
Pour toute question, contactez l'adresse générique du projet iPubli: ipubli@inserm.fr
