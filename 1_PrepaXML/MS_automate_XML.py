"""
Programme N1 pour la préparation des lots Medecine\Science. Gère le XML M\S.
    - Automatisation de l'enrichissement des métadonnées des articles de Medecine/Sciences:
        - Obtient le pmId de chaque article à partir du DOI récupéré et en interrogeant PubMed
        - Récupère les mots clefs MeSH (en anglais) + leurs UIDs en interrogeant PubMed
        - Récupère les traductions des termes MeSH en français à partir du fichier 
            lookups.json du MeSH bilingue (extraction de MTW)
    - Suppression des balises graphic associés à des images qui ne seront pas utilisées
      (small, tiff...)

Auteur: Juliette Janes
Role: Ingénieure Traitement de Métadonnées et Langages Documentaires
Date: 20/01/2022
Corrections réalisées le 31/08/2022 à la demande C.Iizuka, responsable éditoriale d'iPubli
---
Modification du programme le 27/01/2025 par Fanny Pesle, à la demande de Charlotte Iizuka
---
Corrections apportées le 10/02/2026 par F.Pesle & C.Iizuka suite à la modification du format 
des termes MeSH récupérés via PubMed
"""
import os
# chargement de la clef d'API pour augmenter la capacité de requetes sur PubMed 
# (10 rq/sec au lieu de 3)
os.environ["NCBI_API_KEY"] = "e06fe9a4b0a2afd3b3bf68bc141081712508"

import time
from xml.dom import minidom
import metapub
import os
from lxml import etree as ET
import click
import json


# Création d'un dictionnaire local de traduction des termes MeSH
with open('2024_lookups.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
lookups = data['lookups_base']
mesh_trads = {t['dui']:t for t in lookups}


def traduction(pmid : str, nom : str):
    """
    Fonction qui pour un pmid donné, récupère les mots clefs mesh, et retourne
      les correspondances depuis le MeSH bilingue en local (.json)
    :param pmid: identifiant pubmed
    :return: mots clefs mesh en français de l'article PubMed
    :trype: str
    """
    fetch = metapub.PubMedFetcher()
    article = fetch.article_by_pmid(pmid)
    article_MeSH = article.mesh
    mesh_terms_fr = []
    continue_yn = 'y'

    # par securité, ralentir la cadence des requêtes vers l'API PubMed pour ne pas
    # faire planter le programme (Erreur 500 Server)
    time.sleep(0.5)

    # Pour chaque dui de descripteur MeSH associé à l'article, s'il y en a
    for dui in article_MeSH.keys():
        # on essaie de récuperer la traduction FR du descripteur
        try:
            # assert continue_yn == 'y'
            # si une trad est trouvée pour le terme, on l'ajoute à la liste des mots clefs de l'article
            descriptor_fr = mesh_trads[dui]['trx']
            mesh_terms_fr.append(descriptor_fr)
        except KeyError:
            # si pas de trad pour ce dui dans le MeSH local, on informe l'utilisatrice
            print(f"Fichier {nom} (PMID = {pmid}) : Traduction MeSH non trouvée pour le terme : {dui} : {article_MeSH[dui]['descriptor_name']}")
            with open("fichiers_a_corriger.txt", "a", encoding='utf-8') as f:
                # on ecrit le même message d'erreur dans le fichier de rapport d'erreurs que dans la console
                f.write(f"Fichier {nom} (PMID = {pmid}) : Traduction MeSH non trouvée pour le terme : {dui} : {article_MeSH[dui]['descriptor_name']}")
            continue_yn = input('Continuer le traitement des fichiers ? (y/n)')
            if continue_yn == 'n':
                break

        # si le descripteur a un qualifieur associé, on applique le même traitement pour l'ajouter à la liste
        term = article_MeSH[dui]
        if len(term['qualifiers'])>0:
            for q in term['qualifiers']:
                # combinaison du qualifier avec son descripteur
                qualifier_fr = mesh_trads[q['qualifier_ui']]['trx']
                combo_q_d = descriptor_fr + ' - ' + qualifier_fr
                mesh_terms_fr.append(combo_q_d)
    # formattage XML des mots clefs si trouvés
    if len(mesh_terms_fr)>0 :
        open_xml_tag_str = '\n<kwd-group kwd-group-type="MESH">\n<kwd>'
        close_xml_tag_str = '</kwd>\n</kwd-group>\n'
        join_xml_tag_str = '</kwd>\n<kwd>'

        mesh_terms_fr_str = join_xml_tag_str.join(mesh_terms_fr)
        mesh_terms_fr_str = open_xml_tag_str + mesh_terms_fr_str + close_xml_tag_str
    
    # si aucun terme MeSH associé à l'article sur pubmed
    else:
        # renvoyer une tring vide
        mesh_terms_fr_str = ''
    
    return mesh_terms_fr_str




def CreationArbre(root, pmid, kwd_group_xml):
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
    # si des mots clefs MeSH sont trouvés
    if len(kwd_group_xml)>0:
        # récupération de la balise counts
        sibling_node_place = root.getElementsByTagName("counts")[0]
        # transformation des mots clefs traduits en arbre XML
        kwd_group_xml = minidom.parseString(kwd_group_xml).documentElement
        # ajout des mots clefs juste avant la balise counts
        article_meta.insertBefore(kwd_group_xml, sibling_node_place)
    # on retourne l'arbre xml enrichi
    return root



def enrichissementXML(nom : str):
    """
    Fonction qui pour un fichier xml donné, enrichi son contenu en ajoutant
      le pmid de l'article et les mots-clefs mesh en français.
    :param nom: chemin du fichier XML
    :return: fichier XML complété avec pmid et termes MeSH
    :rtype: fichier xml
    """
    # lecture du fichier XML avec la librairie minidom
    root = minidom.parse(nom)
    # récupération de la balise du doi de l'article indiqué dans le fichier XML
    article_id_tags = root.getElementsByTagName("article-id")
    doi_xml = [tag for tag in article_id_tags if tag.getAttribute('pub-id-type')=='doi'][0]
    # récupération du doi en lui même (le contenu de la balise doi)
    doi = doi_xml.firstChild.nodeValue
    # fonction permettant à partir d'un doi d'obtenir le pmid équivalent.
    print("> doi: %s" % doi)
    pmid = metapub.convert.doi2pmid(doi)
    # Si le pmid n'est pas trouvé ou est ambigu
    if (pmid is None) or (pmid == 'AMBIGUOUS') or ('NOT FOUND' in pmid):
        # on vérifie si c'est normal de ne pas trouver le pmid (= on sait qu'il n'existe pas)
        subject_tags = root.getElementsByTagName("subject")
        subject_content_type_series = [tag for tag in subject_tags if tag.getAttribute('content-type')=='series']
        if len(subject_content_type_series)>0 :
            if subject_content_type_series[0].firstChild.nodeValue == 'Les mots de la science':
                pass
        else:
            print("Le pmid de l'article ne peut pas être trouvé. Le document n'est pas traité.")
            # on y ajoute le nom du fichier avec la mention pmid non trouvé
            print("pmid: %s" % pmid)
            with open("fichiers_a_corriger.txt", "a") as f:
                f.write(f"Pmid non trouvé: {nom}. Doi: {doi}")
    # si pmid trouvé
    else:
        try:
            print("> pmid :"+pmid)
            print("> Recherche traduction en cours...")
            start_time = time.time()
            # application de la fonction traduction qui recupère les traductions dans le fichier MeSH local
            kwd_group = traduction(pmid, nom)
            end_time = time.time()
            print(f"> Traduction trouvée en {end_time - start_time} secondes")
            # application de la fonction creationArbre qui intègre le pmid et le groupe des mots clefs mesh traduits dans le fichier XML
            root = CreationArbre(root, pmid, kwd_group)
            # ouverture du fichier XML
            f = open(nom, 'w', encoding='utf-8')
            # impression dans le fichier de l'arbre XML obtenu
            root.writexml(f, addindent='    ', newl=' \n ', encoding='utf-8')
            # fermeture du fichier
            f.close()
        except Exception as err:
            print(err)
            print(f"Une erreur {err.__class__} est survenue. Le document n'est pas traité.")
            with open("fichiers_a_corriger.txt", "a") as f:
                # on y ajoute le nom du fichier avec la mention erreur
                f.write("Erreur survenue : Document non traité : " + nom + "\n")


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
def automate_ms_motsclefs(doc):
    """
    Script faisant partie de la pipeline de traitement des Médecine\Sciences pour leur intégration dans iPubli.
    Programme qui, à partir d'un dossier contenant les lots de Medecine\Science pour import extrait d'EDP Sciences,
    nettoie les XML de chaque article en supprimant les mentions d'images non utilisées dns iPubli, en ajoutant le pmid
    et en récupérant puis ajoutant les mots clefs MeSH en français qui indexe l'article.\n
    
    :param doc: chemin vers le dossier contenant les lots Medecine\Science à traiter.\n
    :return: fichiers XML mis à jour dans les lots
    """

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
                    enrichissementXML(nom)
                    # on supprime les images du XML avec la fonction sup_graphic
                    sup_graphic(nom)
                # si il n'y a ni mots clefs MeSH ni pmid dans le fichier
                else:
                    # on ajoute le pmid et les mots clefs MeSH avec la fonction enrichissement XML
                    enrichissementXML(nom)
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
