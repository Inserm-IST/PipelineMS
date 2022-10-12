"""
Programme N1 pour la préparation des lots Medecine\Science. Gère le XML M\S.
    - Automatisation de l'enrichissement des métadonnées des articles de Medecine/Sciences:
        - Obtient le pmId de chaque article à partir du DOI récupéré et en interrogeant PubMed
        - Récupère les mots clefs MeSH en français à partir du moteur de traduction du MeSH bilingue
    - Suppression des balises graphic associés à des images qui ne seront pas utilisées (small, tiff...)

Auteur: Juliette Janes
Role: Ingénieure Traitement de Métadonnées et Langages Documentaires
Date: 20/01/2022
Corrections réalisées le 31/08/2022 à la demande C.Iizuka, responsable éditoriale d'iPubli
"""

from selenium import webdriver
import requests
import time
import re
from xml.dom import minidom
import metapub
import os
from lxml import etree as ET
import click


def nettoyage_page(page):
    """
    Fonction qui pour une page html fournie, retourne en sortie uniquement les mots clefs mesh en français
    :param page: code source de la page html résultat
    :type page: str
    :return: mots clefs mesh en français structurés en xml
    :rtype: str
    """
    # récupération de la réponse dans la page html à l'aide d'une expression régulière
    kwd_group = re.search('<li>&lt;kwd-group kwd-group-type="MESH"&gt;(.|\n)*?<li>&lt;\/kwd-group&gt;<\/li>',
                          page).group()
    # plusieurs nettoyages de la réponse récupérée afin de supprimer les balises html et conserver uniquement la réponse
    # en texte plein
    kwd_group_1 = kwd_group.replace('<li>', '')
    kwd_group_2 = kwd_group_1.replace('</li>', '')
    kwd_group_3 = kwd_group_2.replace('</ul>', '')
    kwd_group_4 = kwd_group_3.replace('<ul style="list-style-type:none">', '')
    kwd_group_5 = kwd_group_4.replace('&lt;', '<')
    kwd_group_propre = kwd_group_5.replace('&gt;', '>')
    # on retourne la réponse propre
    return kwd_group_propre


def traduction(pmid,browser,nom):
    """
    Fonction qui pour un pmid donné, ouvre un navigateur internet à la page de traduction des mots clefs meshs, qu'elle
    donne en sortie
    :param pmid: identifiant pubmed
    :type pmid: str
    :param browser: page html du traducteur mesh
    :type browser: webdriver
    :param nom: chemin vers le fichier xml
    :type nom: str
    :return: mots clefs mesh en français de l'article structuré en xml
    :trype: str
    """
    # trouver le formulaire à remplir dans la page (formulaire nommé pmids)
    formElem = browser.find_element_by_id('pmIds')
    # nettoyage du formulaire
    formElem.clear()
    # rentrer le pmId
    formElem.send_keys(pmid)
    # trouver le bouton go
    buttonElem = browser.find_element_by_id('goButton')
    # cliquer sur le bouton go
    buttonElem.click()
    # Attendre 30 secondes pour laisser le temps au serveur de donner la réponse
    time.sleep(30)
    # au bout de 30 secondes, si le bouton a encore comme valeur chargement
    if 'Chargement' in buttonElem.get_attribute('value'):
        # On indique à l'utilisateur que le fichier n'a pas pu être traité
        print("Le fichier "+ nom+" n'a pas pu être traité. Veuillez fournir le pmid et les mots-clefs MESH manuellement. Le nom du fichier est disponible dans le document 'fichiers_a_corriger'.")
        # on ouvre le fichier txt contenant les fichiers non corrigés
        with open("fichiers_a_corriger.txt", "a") as f:
            # on y ajoute le nom du fichier avec la mention chargement trop long pour indiquer que tout est à refaire
            f.write("Chargement trop long: "+nom+"\n")
    else:
        # Sinon on récupère le html de la page réponse
        page_resultat = browser.page_source
        # on fait appel à la fonction nettoyage_page qui permet d'obtenir la réponse nettoyée de ses balises html
        mesh_group =nettoyage_page(page_resultat)
        # si une des traductions n'a pas été trouvée dans la réponse
        if "non trouvé" in mesh_group:
            # On indique à l'utilisateur qu'une traduction n'a pas été trouvée
            print("Une traduction n'a pas été trouvée. Le nom du fichier est disponible dans le document 'fichiers_a_corriger'.")
            # on ouvre le fichier txt contenant les fichiers non corrigés
            with open("fichiers_a_corriger.txt", "a") as f:
                # on y ajoute le nom du fichier avec la mention traduction non trouvée pour indiquer qu'un des mots clefs mesh n'a pas été traduit et doit être réalisé manuellement
                f.write("Traduction non trouvée: "+nom+"\n")
    # on retourne les mots clefs mesh traduits et un fichier fichier_a_corriger rempli
    return mesh_group


def CreationArbre(root,nom, pmid, kwd_group_xml):
    """
    Fonction qui, en prenant en entrée un fichier Medecine/Sciences, son pmid et les mots clefs mesh en français,
    ajoute les deux derniers éléments à l'arbre XML.
    :param root: arbre XML du fichier traité
    :type root: ElementTree
    :param nom: chemin vers le fichier xml
    :type nom: str
    :param pmid: identifiant pubmed
    :type pmid: str
    :param kwd_group_xml: mots clefs mesh en français de l'article structuré en xml
    :type kwd_group_xml: str
    :return: arbre xml associant le contenu du fichier xml, le pmid et les mots clefs mesh
    """
    # navigation dans l'arbre XML créé à partir du fichier XML jusqu'au premier noeud article-meta
    article_meta = root.getElementsByTagName("article-meta")[0]
    # création de la balise article-id pour ajouter le pmid
    pmid_xml = root.createElement("article-id")
    # ajout d'un attribut de valeur pmid à cette balise
    pmid_xml.setAttribute("pub-id-type", "pmid")
    # création du pmid comme texte node
    pmid_texte = root.createTextNode(pmid)
    # ajout du pmid dans la balise pmid
    pmid_xml.appendChild(pmid_texte)
    # ajout de la balise article-id et de ses enfants tout juste créés sous la balise article-meta
    article_meta.insertBefore(pmid_xml, article_meta.childNodes[0])
    # récupération de la balise counts
    sibling_node_place = root.getElementsByTagName("counts")[0]
    # transformation des mots clefs traduits en arbre XML
    kwd_group_xml = minidom.parseString(kwd_group_xml).documentElement
    # ajout des mots clefs dans la balise counts
    article_meta.insertBefore(kwd_group_xml, sibling_node_place)
    # on retourne l'arbre xml corrigée
    return root



def enrichissementXML(nom,browser, pmid_verif=False):
    """
    Fonction qui pour un fichier xml donné, enrichie son contenu en ajoutant le pmid de l'article et les mots
    clefs mesh en français.
    :param nom: chemin du fichier XML
    :type nom: str
    :param browser: page html du traducteur mesh
    :type browser: webdriver
    :param pmid_verif: booléen indiquant la présence ou non d'un pmid dans le fichier XML traité
    :type pmid_verif: bool
    :return: fichier XML complété sans pmid
    :rtype: fichier xml
    """
    # lecture du fichier XML avec la librairie minidom
    root = minidom.parse(nom)
    # récupération de la balise du doi de l'article indiqué dans le fichier XML
    doi_xml = root.getElementsByTagName("article-id")[0]
    # récupération du doi en lui même (le contenu de la balise doi)
    doi = doi_xml.firstChild.nodeValue
    # fonction permettant à partir d'un doi d'obtenir le pmid équivalent.
    pmid = metapub.convert.doi2pmid(doi)
    # application de la fonction traduction qui permet d'interroger le traducteur web du mesh et en récupère les mots clefs
    # mesh
    kwd_group = traduction(pmid,browser,nom)
    # application de la fonction creationArbre qui intègre le pmid et le groupe des mots clefs mesh traduits dans le fichier XML
    root = CreationArbre(root,nom, pmid, kwd_group)
    # ouverture du fichier XML
    f = open(nom, 'w', encoding='utf-8')
    # impression dans le fichier de l'arbre XML obtenu
    root.writexml(f, addindent='    ', newl=' \n ', encoding='utf-8')
    # fermeture du fichier
    f.close()


def sup_graphic(fichier):
    """
    Fonction qui pour un fichier XML donné supprime toutes les références à des images non employées
    :param fichier: chemin du fichier XML
    :type fichier: str
    :return: fichier XMl corrigé sans les images inutiles
    :type: fichier XML
    """
    # lecture du fichier XML
    tree = ET.parse(fichier)

    # on récupère une liste de balise graphic dont la valeur est tiff avec xpath
    for tif in tree.xpath("//graphic[@mime-subtype=\"tiff\"]"):
        # on supprime la balise graphic, ses enfant et les balises de parents
        tif.getparent().remove(tif)

    # on récupère une liste de balise graphic dont la valeur est thumbnail
    for small in tree.xpath("//graphic[@specific-use=\"thumbnail\"]"):
        # on supprime les balises correspondantes, ses enfants et la balise parent
        small.getparent().remove(small)

    # on récupère une liste de balise inline-graphic
    for img1 in tree.xpath("//inline-graphic"):
        # suppression des balises correspondantes, ses enfants et la balise parent
        img1.getparent().remove(img1)
    # on récupère une liste des balises legendes de l'image précédente
    for legend_img1 in tree.xpath("//inline-graphic/parent::p/following-sibling::p[1]"):
        # et on les supprime
        legend_img1.getparent().remove(img1)
    # l'arbre xml nettoyé est imprimé dans le fichier XML
    tree.write(fichier, encoding="utf-8")


def test_fichier(nom):
    """
    Fonction qui, pour un fichier XML donné, vérifie si celui-ci a déjà été traité
    :param nom: nom du fichier XML
    :type nom: str
    :return kwd_verif: booléen indiquant la présence ou non des mots clefs mesh en français dans le fichier XML
    :rtype kwd_verif: bool
    :return pmid_verif: booléen indiquant la présence ou non d'un pmid dans le fichier XML
    :rtype pmid_verif: bool
    """
    # initialisationd des booléens pmid_verif et kwd_verif
    pmid_verif = False
    kwd_verif=False
    # lecture du fichier XML
    tree = ET.parse(nom)
    # récupération du pmid de l'article
    pmid = tree.xpath("//article-id[@pub-id-type=\"pmid\"]")
    # si il y a un pmid dans le fichier
    if pmid:
        # on change la valeur du booléen pmid_verif en true
        pmid_verif = True
    # récupération de la balise kwd
    kwd_grpe = tree.xpath("//kwd-group[@kwd-group-type=\"MESH\"]")
    # si il y a bien une balise kwd
    if kwd_grpe:
        # on change la valeur du booléen kwd_verif en true
        kwd_verif=True
    # on retourne les 2 booléens
    return kwd_verif, pmid_verif


def remove_pmid(fichier):
    """
    Fonction qui supprime le pmid si existant
    :param fichier: chemin vers le fichier XML traité
    :type fichier: str
    :return: fichier XML complété sans pmid
    :rtype: fichier xml
    """
    # lecture du fichier XML
    tree = ET.parse(fichier)
    # on récupère la balise pmid dans le document
    for pmid in tree.xpath("//article-id[@pub-id-type=\"pmid\"]"):
        # on la supprime
        pmid.getparent().remove(pmid)
    # impression de l'arbre obtenu dans le fichier XML
    tree.write(fichier, encoding="utf-8")


@click.command()
@click.argument('doc', type=str)
@click.option("-c","--Ch","chrome", is_flag=True, default=False, help="si on souhaite utiliser Chrome plutôt que Firefox")
def automate_ms_motsclefs(doc):
    """
    Script faisant partie de la pipeline de traitement des Médecine\Sciences pour leur intégration dans iPubli.
    Programme qui, à partir d'un dossier contenant les lots de Medecine\Science pour import extrait d'EDP Sciences,
    nettoie les XML de chaque article en supprimant les mentions d'images non utilisées dns iPubli, en ajoutant le pmid
    et en récupérant puis ajoutant les mots clefs MeSH en français qui indexe l'article.\n
    L'outil emploie le traducteur MeSH ci-joint: http://ccsdmesh.in2p3.fr/FrenchMesh/admin/translate.jsp et communique
    avec Firefox sur votre ordinateur pour ce faire. \n
    :param doc: chemin vers le dossier contenant les lots Medecine\Science à traiter.\n
    :return: fichiers XML mis à jour dans les lots
    """
    if chrome:
        # Ouvre le navigateur
        browser = webdriver.Chrome(
            executable_path=r"C:\Users\juliette.janes\Desktop\Boite_a_outils\Pipeline_MS\PrepaXML\chromedriver.exe")
    else:
        # Ouvre le navigateur
        browser = webdriver.Firefox(
            executable_path=r"C:\Users\juliette.janes\Desktop\Boite_a_outils\Pipeline_MS\PrepaXML\geckodriver.exe")
    # accès à la page du traducteur mesh
    browser.get('http://ccsdmesh.in2p3.fr/FrenchMesh/admin/translate.jsp')
    # création doc fichiers à corriger vide
    with open('fichiers_a_corriger.txt', 'w') as f:
        pass
    # pour chaque fichier xml du dossier
    for dossier in os.listdir(doc):
        # on créé le chemin absolu vers le dossier traité
        nom_dossier = os.path.join(doc,dossier)
        # pour chaque fichier du dossier traité
        for fichier in os.listdir(nom_dossier):
            # si le fichier traité est un xml, on réalise les étapes suivantes
            if ".xml" in fichier:
                # on indique à l'utilisateur le traitement du fichier en question
                print("Traitement du fichier "+fichier)
                # on créé le chemin absolu vers le fichier traité
                nom = os.path.join(doc, dossier, fichier)
                # on vérifie que le fichier n'a pas déjà été traité avec la fonction test_fichier présente plus haut
                mesh_verif, pmid_verif = test_fichier(nom)
                # si les mots clefs mesh et le pmid sont présents dans le fichier
                if mesh_verif==True and pmid_verif==True:
                    # on indique à l'utilisateur que le fichier a été traité
                    print("Le fichier a déjà été traité.")
                    # on passe au fichier suivant
                    pass
                # si il y a un pmid mais pas de mots clefs mesh
                elif mesh_verif==False and pmid_verif==True:
                    # on indique à l'utilisateur l'erreur et la correction
                    print("Le fichier a été partiellement traité. Nous le retraitons.")
                    # on supprime le pmid du fichier avec la fonction remove_pmid
                    remove_pmid(nom)
                    # on ajoute le pmid et les mots clefs avec la fonction enrichissement XMl
                    enrichissementXML(nom, browser, pmid_verif)
                    # on supprime les images du XML avec la fonction sup_graphic
                    sup_graphic(nom)
                # si il n'y a ni mots clefs MeSH ni pmid dans le fichier
                else:
                    # on ajoute le pmid et les mots clefs MeSH avec la fonction enrichissement XML
                    enrichissementXML(nom, browser)
                    # on supprime les images du XML avec la fonction sup_graphic
                    sup_graphic(nom)
    print("""Tous les XML ont été traités.\n 
    Vous pouvez les retrouver à leur place dans chacun des lots.\n
    Nous vous conseillons de vérifier sur certains XML si le travail a bien été réalisé:\n
        - Suppression des mentions d'images non souhaitées \n
        - Ajout du pmid\n
        - Ajout des mots clefs MeSH traduits\n""")

# on lance la fonction principale avec le lancement du script
if __name__=='__main__':
    automate_ms_motsclefs()
