""""
Programme N2 pour la préparation des lots Medecine\Science. Gère les fichiers et la structure des dossiers.
    - Suppression automatique des images non souhaitées (tif,tiff, img1 et small)
    - Création du dublin core
    - Renommage des items
    - Création du content
    - Création du métadata
Author:Juliette Janes
Role: Ingénieure traitement de métadonnées et langages documentaires
Date:25/08/2022
"""

from lxml import etree
import os
import click


def creation_db(dir):
    """
    fonction qui créé le dublin core de l'article a partir de son xml
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier dublin_core xml contenant les métadonnées de l'article traité
    """
    # lecture et stockage de la feuille XSL de transformation du XML de l'article en dublin core XML
    creation_dublincore = etree.parse(r".\2_PrepaFichiers\EDPmeta2DSpace_single2021.xsl")
    # transformation de la feuille de XSL en XSLT pour python afin de permettre son utilisation
    xslt_transformation = etree.XSLT(creation_dublincore)

    # pour chaque fichier présent dans le dossier lot traité
    for el in os.listdir(dir):
        # si le fichier est un xml
            if ".xml" in el:
                # on lit le fichier xml
                xml_parse = etree.parse(dir + el)
                # on applique la feuille de transformation XSLT sur le XML et on stocke le résultat
                dublin_core = xslt_transformation(xml_parse)
    # on imprime le résultat dans un nouveau fichier dublin_core.xml
    dublin_core.write(dir + "/dublin_core.xml", encoding="utf-8")


def sup_images(dir):
    """
    fonction qui supprime chaque image inutile dans un dossier
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: dossier de travail sans les images inutiles
    """
    # pour chaque fichier présent dans le dossier lot traité
    for el in os.listdir(dir):
        # si le nom du fichier traité contient un des termes typiques des images que l'on souhaite supprimer
        if "tif" in el or "small" in el or "img" in el:
            # on supprime le fichier en question du dossier
            os.remove(dir+"/"+el)


def creation_metadata(dir):
    """
    Fonction qui ajoute le fichier métadata au dossier traité
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier XML nommé metadata qui paramètre Dspace pour la construction des métadonnées
    """
    # on créé une balise XML racine nommé dublin_core avec pour attribut schema qui a une valeur inserm
    racine = etree.Element("dublin_core", schema="inserm")
    # on associe à cette balise une sous balise dc_value avec pour attribut language (valeur autocreation) et element
    # (valeur lexicon)
    langage1 = etree.SubElement(racine,"dcvalue", language="",qualifier="autocreation", element="lexicon")
    # on ajoute le texte true encadrée par la balise language précédemment créée
    langage1.text="true"
    # on associe à la balise racine une deuxième sous balise language similaire avec des valeurs d'attribut différentes
    langage2 = etree.SubElement(racine,"dcvalue", language="",qualifier="conversion", element="bitstream")
    # on ajoute le texte true dans la balise langage 2
    langage2.text = "true"
    # on transforme la balise racine en un arbre XML
    racine = etree.ElementTree(racine)
    # on imprime l'arbre XML racine dans un fichier metadata.xml dans le dossier lot traité
    racine.write(dir + "/metadata_inserm.xml", encoding="utf-8")


def renommage_files(dir,nom_standard,renommage):
    """
    Fonction qui renomme les items selon la procédure d'izumi
    :param dir: chemin vers le dossier lot
    :type dir: str
    :param nom_standard: forme du nom standardisé nécessaire pour le renommage des fichiers
    :type nom_standard: str
    """
    # pour chaque fichier contenu dans le dossier lot traité
    for el in os.listdir(dir):
        # si le nom du fichier traité contient msc et pdf (si il s'agit du pdf de l'article)
        if renommage in el and "pdf" in el:
            # on créé le renommage du fichier avec le nom_standard et son extension pdf
            nom = nom_standard+".pdf"
            # on renomme le pdf
            os.rename(dir+"/"+el, dir+nom)
        # si le fichier traité correspond au xml de l'article
        elif renommage in el and "xml" in el:
            # on créé le nom par lequel on souhaite renommer le fichier
            nom = nom_standard+".xml"
            # on renomme le fichier
            os.rename(dir+"/"+el, dir+nom)


def renommage_items(dossier, dir):
    """
    Fonction qui créé les noms standardisés des fichiers pour le renommage
    :param dossier: chemin vers le dossier principal contenant les lots
    :type dossier: str
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: nom standardisé des items et nombre d'item
    :rtype: str et int
    """
    # on lit le dublin_core xml
    xml_dublin_core = etree.parse(dir+"/dublin_core.xml")
    # on récupère le numéro de l'item traité
    num_item = int(xml_dublin_core.xpath('/dublin_core/@page')[0])
    # si le numéro d'item est plus petit que 10
    if num_item < 10:
        # on lui ajoute des 0 devant le nombre de façon à avoir un nombre avec 4 chiffres
        num_item = "000"+str(num_item)
    # si le numéro d'item est compris entre 10 et 100
    elif 10<=num_item<100:
        # on lui ajoute des 0 devant le nombre de façon à avoir un nombre avec 4 chiffres
        num_item = "00"+str(num_item)
    # si le numéro d'item est compris entre 100 et 1000
    elif 100<=num_item<=1000:
        # on lui ajoute des 0 devant le nombre de façon à avoir un nombre avec 4 chiffres
        num_item = "0"+str(num_item)
    # on renomme le nom du dossier lot avec le numéro d'item
    os.rename(dir, dossier+'/item_'+str(num_item))
    # on récupère le nouveau nom du dossier
    nom_item = dossier+"/item_"+str(num_item)
    # on retourne le nouveau nom de dossier et le nombre de l'item traité
    return nom_item, num_item


def windows2unix(dir):
    """
    Fonction qui permet de transformer un fichier contents encodé sous windows en fichier linux
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier content encodé en unix
    """
    # création des chaînes de remplacement
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    # chemin du fichier traité
    file_path = dir + "\contents"
    # ouverture du fichier et lecture
    with open(file_path, 'rb') as open_file:
        content = open_file.read()
    # remplacement des lignes windows par ligne unix
    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    # impression du nouveau contenu dans un fichier unix
    with open(file_path, 'wb') as open_file:
        open_file.write(content)

def creation_content(dir):
    """
    Fonction qui récupère les éléments présents dans le dossier et créé le fichier content à partir de ceux-ci
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier content détaillant le contenu du lot
    """
    # pour chaque fichier du dossier
    for el in os.listdir(dir):
        # si le fichier traité est le xml de l'article
        if "xml" in el and "MS" in el:
            # on ouvre un fichier content
            with open(dir+"/contents","a") as f:
                # on ajoute le nom du fichier avec sa description (le nom souhaité dans iPubli)
                f.write(el+"\t\tdescription:Lire l'article HTML\n")
        # si le fichier traité est le pdf de l'article
        elif "pdf" in el:
            # on ouvre le fichier content
            with open(dir+"/contents", "a") as f:
                # on ajoute le nom du fichier avec sa description
                f.write(el+"\t\tdescription:Lire l'article PDF\n")
        elif "jpg" in el or "jpeg" in el or "png" in el:
            with open(dir+"/contents","a") as f:
                f.write(el+"\n")
    # mobilisation de la fonction windows2unix qui permet d'encoder le fichier contents en unix
    windows2unix(dir)



@click.command()
@click.argument("dossier", type=str)
@click.argument("annee", type=int)
@click.argument("mois", type=int)
@click.option("-h", "--HS", "Horsserie", is_flag=True, default=False, help="si Hors-série")
def automate_file(dossier, annee, mois, Horsserie):
    """
    Script faisant partie de la pipeline de traitement des Médecine\Sciences pour leur intégration dans iPubli.\n
    Intervient en seconde position de la pipeline suite au programme MS_automate_XML.py qui corrige le XML présent
    dans le lot.\n
    Programme qui, à partir d'un dossier contenant les lots de Medecine\Science pour import extrait d'EDP Sciences,
    nettoie les lots et gère la structure des dossiers. Il supprime les images non souhaitées (tif, tiff, img1 et small),
    créé le dublin core XML contenant les métadonnées de l'article, renomme les items selon la procédure, créé le
    fichier content qui détaille les différents éléments présents dans le dossier et le fichier métadata qui gère les
    paramètres des métadonnées dans DSpace.\n
    :param doc: chemin vers le dossier contenant les lots Medecine\Science à traiter.\n
    :return: lots nettoyés 
    """
    # si le mois rentré est plus petit que 10
    if len(str(mois))<2:
        # on ajoute un 0 afin d'avoir un mois avec 2 chiffres
        mois="0"+str(mois)
    # pour chaque lot dans le dossier
    for ms in os.listdir(dossier):
        # on stocke le chemin vers le lot traité
        dir = dossier + "/" + ms+"/"
        # on indique à l'utilisateur le traitement du lot
        print("Traitement du lot " + ms)
        # création du dublin core en mobilisant la fonction creation_db créé plus haut
        creation_db(dir)
        # renommage des items avec la fonction item et récupération du nouveau chemin du dossier suite à son renommage et
        # du numéro d'item
        dir, num_item = renommage_items(dossier, dir)
        print("Le lot est renommé "+dir[-9:])
        # suppression des images inutiles avec la fonction sup_images
        sup_images(dir)
        # si il s'agit d'un hors série
        if Horsserie:
            # on créé le nom standard utilisé pour le renommage avec un HS
            nom_standard = "/MS_" + str(annee) + "_" + str(mois) + "_HS_" + str(num_item)
            renommage = "med"
        # sinon
        else:
            # on créé le nom standard utilisé pour le renommage des fichiers avec l'année, le mois et le numéro d'item
            nom_standard = "/MS_" + str(annee) + "_" + str(mois) + "_" + str(num_item)
            renommage="ms"
        # on lance le renommage des fichiers avec la fonction renommage_files en utilisant les noms standards tout juste créé
        renommage_files(dir, nom_standard,renommage)
        # création du  fichier métadata en mobilisant la fonction creation_metadata
        creation_metadata(dir)
        # création du fichier content en mobilisant la fonction creation_content
        creation_content(dir)

    print("""Tous les lots ont été traités.\n 
                 Vous pouvez les retrouver à leur place dans le dossier """ + dossier +
          """.\n Nous vous conseillons de bien vérifier les résultats obtenus:\n
            - la création d'un fichier XML 'dublin_core.xml' contenant les métadonnées en dublin core\n
            - le renommage des items \n
            - la création d'un fichier 'metadata.xml' paramétrant les métadonnées dans Dspace\n
            - la création d'un fichier content en UNIX\n
            - la supression des images non souhaitées (tif, tiff, small, img1)\n""")


if __name__ == "__main__":
    automate_file()

