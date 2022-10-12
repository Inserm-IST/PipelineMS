# Procédure d'utilisation du programme MS_automate_file.py

Créer un répertoire contenant
- un dossier avec les lots Medecine\Science non modifiés (XML, PDF, images)
- le programme Python (MS_automate_file.py)
- le fichier EDPmeta2DSpace_single2021.xsl


Lancer Anaconda Prompt

Aller à l'emplacement du programme : cd chemin/vers/le/programme

Lancer le script : *python MS_automate_file.py [Repertoire] [Annee] [Mois]*

Le mois et l'année doivent être indiqués en chiffres.

Vérifier les fichiers


### Dans le cas de dossier hors série à traiter:

Créer un repertoire séparé contenant:
- un dossier avec les lots hors séries
- le programme python
- le fichier XSLT

Puis reproduire le même travail que pour les lots lambdas à l'acception de la commande de lancement:
*python MS_automate_file.py [Repertoire] [Annee] [Mois] -h*
