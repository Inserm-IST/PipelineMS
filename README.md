# PipelineMS
Pipeline de programmes python visant à une préparation facilitée des documents à importer dans la collection [Medecine\Sciences](https://www.ipubli.inserm.fr/handle/10608/224) d'[iPubli](https://www.ipubli.inserm.fr/), l'archive ouverte institutionnelle de l'Inserm, gérée par le service de l'Information Scientifique et Technique.

## Guide d'utilisation
1) Récupération des lots fournis par EDP Sciences, éditeur de la revue Medecine\Sciences. Pour chaque magazine, ils contiennent un dossier par article composé d'un PDF de l'article, un XML du texte et des images présentées dans le texte.

Dans Anaconda Prompt (pour un utilisateur Windows):

2) Navigation dans le bureau: `cd Users\[nom]\Desktop\`
3) Téléchargement du dépôt github: `git clone https://github.com/Inserm-IST/PipelineMS.git` et navigation dedans: `cd PipelineMS`
4) Ajout manuel du dossier de lots téléchargés dans le 1 dans le dossier PipelineMS tout juste créé
5) Lancement du programme MS_automate_XML.py qui nettoie et alimente le XML de chaque article:<br/>
 `python 1_PrepaXML\MS_automate_XML.py [nom_du_dossier_à_traiter]`<br/>
  Pour plus d'informations: [1_PrepaXML](https://github.com/Inserm-IST/PipelineMS/tree/main/1_PrepaXML)

6) Lancement du programme MS_automate_file.py qui organise automatiquement la structure des dossiers (renommage, suppression et création automatique de fichiers):<br/>
    `python 2_PrepaFichiers\MS_automate_file.py [nom_du_dossier_à_traiter] [Année_du_magazine] [mois_du_magazine]`<br/>
   Les mois et années doivent être notés en chiffres.<br/>
   Pour plus d'informations: [2_PrepaFichiers](https://github.com/Inserm-IST/PipelineMS/tree/main/2_PrepaFichiers)<br/>
7) Ajout des lots avec le programme d'import
8) Création du sommaire html du magazine: 
        - Dans la nouvelle page du magazine ajouté, *Contexte>exporter les métadonnées* et télécharger le csv dans le dossier PipelineMS
        - Lancement du programme MS_automate_sommaire.py:<br/>
        `python 3_Sommaire_creation\MS_automate_sommaire.py [nom_du_csv]`<br/>
 Pour plus d'informations: [3_Sommaire_creation](https://github.com/Inserm-IST/PipelineMS/tree/main/3_Sommaire_creation)

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
