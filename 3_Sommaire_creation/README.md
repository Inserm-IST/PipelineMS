# Procédure pour l'utilisation du programme MS_automate_sommaire.py

Permet la création automatique du sommaire d'un magazine Medecine\Science une fois l'import par lots des articles et de leurs métadonnées réalisés dans iPubli.

Extraire en csv les métadonnées des articles du magazine.

Ajouter une nouvelle colonne au csv:
	- Nom de la colonne: categorie (sans accent ni espace)
	- Contenu de la colonne: la catégorie de l'article (Editorial, Forum, Nom de la rubrique). 
Attention => il est important d'écrire en toutes lettres le nom de la rubrique de l'article et de vérifier que lorsque plusieurs articles font partis de la même rubrique la catégorie soit exactement identique dans le csv (pas d'accent,
d'espace ou de majuscules qui changent). Conseil: réaliser un copier coller.

Créer un répertoire contenant:
	- le fichier csv des métadonnées du magazine
	- le programme python MS_automate_sommaire.py

Lancer Anaconda Prompt

Aller à l'emplacement du programme: cd chemin/vers/le/programme

Lancer le script: python MS_automate_sommaire.py [nom_du_csv]

Le programme va s'exécuter avec des informations affichées dans l'Anaconda Prompt. 

Le programme détecte (dans la mesure du possible) les erreurs de frappes lors de l'ajout des catégories dans le csv. Il l'indique et permet à l'utilisateur du script de les corriger puis de relancer le programme. 

A noter: si une faute de frappe dans les catégories du csv est trop éloignée des autres noms de rubriques, le programme ne trouvera pas d'erreur. Il est donc important de vérifier les rubriques indiquées dans le csv.

Un fichier sommaire.xml est créé à la fin du programme dans le répertoire de travail. Il contient le html à coller directement dans iPubli au niveau de la description de la collection. Bien le vérifier avant.