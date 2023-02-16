"""
Script qui permet, pour un fichier csv contenant les métadonnées de tout un magazine Medecine\Science de former le sommaire
en HTML correspondant
Auteur:Juliette Janes
Date:20/09/2022
Contexte: Préparation des documents Medecine\Sciences
"""

import pandas as pd
from lxml import etree as ET
import click
import os
import re
from difflib import SequenceMatcher
import sys

def create_page(df):
    """
    Fonction qui, à partir d'un dataframe, récupère pour chaque ligne le numéro de page décrit dans une de ses colonnes et
    en fait une colonne séparée.
    :param df: dataframe
    :return: dataframe avec la colonne page contenant le numéro de chaque article et trié dans l'ordre
    """
    # récupération du numéro de page de chaque article et ajout dans le dataframe dans la colonne page
    length_df = int(len(df.index))
    # initialisation du n et de la liste liste_page
    liste_page=[]
    # Pour chaque ligne du csv (soit les métadonnées d'un fichier) je réalise les opérations suivantes
    for n in range(length_df):
        # récupération de la ligne de métadonnées dans le csv
        MD_fichier = df.loc[n]
        # récupération du contenu de la cellule dc.source et stockage dans la variable source
        source = MD_fichier["dc.source[]"]
        # récupération du contenu de la cellule dc.source et stockage dans la variable source
        source = MD_fichier["dc.source[]"]
        # récupération du numéro de page de la dernière page de l'article
        page = re.findall(r'\d{1,4}$', source)
        page = "".join(page)
        if "-" in page:
            page = int(page.replace("-", ""))
        else:
            page = int(page)
        # ajout du numéro obtenu dans la liste liste_page
        liste_page.append(page)
    # ajout d'une colonne page dans le dataframe qui correspond au numéro de page de l'article
    df["page"]=liste_page
    # organisation de la dataframe en fonction du numéro de page
    df = df.sort_values(["page"])
    # on retourne le nouveau dataframe
    return df


def create_df_cat(df):
    """
    Fonction qui récupère la liste des catégories accessibles dans le csv
    :param df: dataframe
    :return: liste des catégories
    """
    # stockage dans une variable liste_cat des valeurs dans la colonne catégorie
    liste_cat = df["dc.relation.ispartof[]"].tolist()
    unique_liste_cat = list(dict.fromkeys(liste_cat))

    return unique_liste_cat

def auteur_nom_propre(el_auteur):
    # récupération du nom et du prénom de l'auteur avec des regex
    prenom = re.sub(r'([a-zA-ZéÉ]|-)*, ', '', el_auteur)
    nom = re.sub(r', ([a-zA-ZéÉ]|-)*', '', el_auteur)
    # reformulation du nom de l'auteur selon le choix éditorial réalisé
    auteur_propre = prenom + " " + nom
    return el_auteur

def construction_auteur(df):
    """
    Fonction qui à partir de la ligne de métadonnées d'un article, récupère les auteurs de l'article et le structure
    selon le schéma demandé Prénom Nom, Prénom1 Nom1 et Prénom2 Nom2
    :param df:dataframe
    :return: chaîne de caractères avec tout les auteurs
    """
    # récupération de la valeur de la cellule dc.contributor.author pour la ligne étudiée (soit les auteurs de l'article)
    auteurs = df['dc.contributor.author[-]']
    # division de la chaîne de caractères obtenue en une liste d'auteurs
    list_auth = list(auteurs.split("||"))

    # pour chaque auteur de la liste
    # si il n'y a qu'un seul auteur dans notre liste d'auteur
    string_auth = ""
    for i, el in enumerate(list_auth, start=1):
        # dernier élément
        if i == len(list_auth):
            el_propre = auteur_nom_propre(el)
            string_auth += el_propre
            # avant dernier élément
        elif i == len(list_auth) - 1:
            el_propre = auteur_nom_propre(el)
            string_auth += (el_propre + " et ")
            # élément quelconque
        else:
            el_propre = auteur_nom_propre(el)
            string_auth += (el_propre + ", ")


    # on tranforme la liste d'auteurs propres en une chaîne de caractères unique
    return string_auth


def creation_html(categorie, df, racine):
    """
    Fonction qui, à partir d'un dataframe pour une catégorie, met à jour l'arbre xml en y ajouter les balises et texte pour chaque article
    :param categorie: catégorie traitée
    :param df: dataframe de travail
    :param racine: arbre xml
    :return: arbre xml racine mis à jour avec les nouveaux articles traités pour 1 catégorie
    """
    # récupération des lignes du df qui font parti de la catégorie traitée
    df_categorie = df.loc[df['dc.relation.ispartof[]'] == categorie]
    # réorganisation de l'index du dataframe obtenu
    df_categorie = df_categorie.reset_index(drop=True)
    # recherche de ul dans l'arbre xml
    # création de la balise h3 contenu le titre de la catégorie et insertion dans le xml
    cat_html = ET.SubElement(racine, "p")
    cat_html.attrib['class']="som-titre-niveau1"
    i_cat_html = ET.SubElement(cat_html, "i")
    i_cat_html.text = categorie
    # tant que le nombre d'itération de la boucle n'est pas égale au nombre de ligne dans le dataframe, on réitère les
    # opérations suivantes
    for n in range(len(df_categorie)):
        df_line = df_categorie.iloc[n]
        # création des balises html pour l'article traité
        div1_html = ET.SubElement(racine, "div")
        div1_html.attrib['class']='artifact-description'
        div2_html = ET.SubElement(div1_html, "div")
        # création de la valeur class qui a pour valeur artifact title
        div2_html.attrib['class']='artifact-title'
        # stockage dans la valeur handle de la valeur de la cellule identifier
        handle = df_line['dc.identifier.uri']
        # suppression d'url pour conserver uniquement le handle
        handle_propre = handle[-5:]
        ul_html = ET.SubElement(div2_html, "ul")
        # création de la balise a qui contient le handle et permet de faire le lien avec la page de l'article. Ajout
        # de la valeur handle dans l'attribut handle et de l'attribut onclick permettant de création un lien
        a_html = ET.SubElement(ul_html, "a", href=handle_propre,onclick="window.open(this.href,'_blank');return false;")
        # création des balises suivantes
        li_div_html = ET.SubElement(a_html, "li")
        li_div_html.attrib['class'] = "som-titre-niveau2"
        # ajout du texte dans la cellule titre dans la balise titre
        li_div_html.text = df_line["dc.title[fr]"]
        li_author_html = ET.SubElement(ul_html, "li")
        li_author_html.attrib["class"]="author"
        span_html = ET.SubElement(li_author_html, "span")
        # ajout des auteurs de l'article, récupérés et reformulés dans la fonction construction_auteur dans la balise span
        span_html.text = construction_auteur(df_line)
        p_html = ET.SubElement(racine, "p")
    # la fonction retourne l'arbre xml mis à jour
    return racine


def creation_css(filename):
    """
    Fonction qui créé le css et l'ajoute en tête du document XML créé
    :param filename: nom du fichier
    :type filename: str
    :return: document XML avec css
    """
    xml_css = """<head>
        <style>
     ul {
        list-style-type: none;
        } 
            .author {
            font-size:13px; 
            margin-left: 30px;
			margin-top:0.1px;
        font-style: italic;
            color: #9e9e9e;
            }
                    p   {
    font-family: inherit;
        font-weight: 500;
        line-height: 1.1;
            font-size:15px;
    		margin-left: 0px;
            color: #999;	

            }
            .som-titre-niveau1 { 
         font-size:20px; 
            font-style: italic;
            font-weight: bold;
    margin: 15px;
    margin-left: 30px;
    display: block;
    color:#5db2b5;

            }

           .som-titre-niveau2  { 
            font-size:17px;
    		margin-left: 30px;
			margin-bottom: 0.1px;
    font family:"Open Sans", Calibri, Verdana, Arial, sans-serif;
    line-height: 1.428571429;
  
         }

        </style>
    </head>
        """
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(xml_css.rstrip('\r\n') + '\n' + content)


@click.command()
@click.argument("csv_file", type=str)
def creation_sommaire(csv_file):
    """
    Fonction qui, à partir d'un csv, retourne un fichier xml contenant le sommaire html Medecine\Science
    :return: fichier xml sommaire.xml
    """
    # lecture du fichier csv et stockage dans une variable df
    df = pd.read_csv(csv_file)
    print("Traitement du csv lancé")
    # mobilisation de la fonction create_page: tri le tableau par catégorie et par page ascendante.
    df_page = create_page(df)
    # la variable list_div mobilise la fonction create_df_cat qui récupère la liste des différentes catégories présentes dans
    # le csv
    liste_div = create_df_cat(df_page)
    # Création de l'élément xml racine du html sommaire
    racine = ET.Element("div", id="our_summary")
    sommaire = ET.SubElement(racine, "h3")
    sommaire.text = "Sommaire"
    # pour chaque catégorie de la liste list_div les actions suivantes sont réalisées
    for categorie in liste_div:
        #affichage de la catégorie traitée
        print("Traitement de la catégorie "+categorie)
        # mobilisation de la fonction creation_html qui, pour toutes les lignes du csv catégorie traitée, créé les balises
        # html correspondantes et y ajoute le texte et les valeurs d'attributs extraites du csv
        racine = creation_html(categorie, df_page,racine)

    # transformation de l'élément xml racine en arbre xml
    racine = ET.ElementTree(racine)

    # impression de l'arbre xml dans un fichier xml
    racine.write("sommaire.xml", encoding="utf-8")
    # ajout du css en tête de fichier:
    creation_css("sommaire.xml")
    print("Le sommaire a bien été généré, vous pouvez le retrouver dans le fichier sommaire.xml disponible dans votre dossier de traitement")


if __name__ == "__main__":
    creation_sommaire()
