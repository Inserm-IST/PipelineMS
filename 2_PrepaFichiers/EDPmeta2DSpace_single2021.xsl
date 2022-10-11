<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

<!-- de articles ou article (avec tt ou front ou partie de front) de fichier EDP/INSERM à Notice DC numéro -->
	
<!-- pour 2010 hs1 : pas d'élt de sortie relation.isPartOf, mais pas de rubrique
		pas de N° renseigné dans source et citation -->
<xsl:output encoding="UTF-8" indent="yes"/>

	<xsl:template match="/">
		<xsl:choose>   <!-- marchera si une (cas 2) ou +ieurs notices (cas 1) -->
			<xsl:when test="article">
				<!--<xsl:element name="dspace_num">-->
					<xsl:for-each select="article/front">
						<xsl:sort select="@page" data-type="number" order="ascending"/>
						<xsl:apply-templates select="."/>
					</xsl:for-each>
				<!--</xsl:element>-->
			</xsl:when>
			<xsl:when test="front"><xsl:apply-templates select="front"/></xsl:when>
			<xsl:otherwise>
				<xsl:element name="erreur"><xsl:text>**** attention à la structure ***</xsl:text></xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>


<xsl:template match="front">

	<xsl:element name="dublin_core">
		<xsl:attribute name="page">
			<xsl:choose>
				<!-- localisation dépend de l'année (et même de l'item en 2009 : 2° OK en majorité, parfois 1° (ex : 1126 num 12) : -->
				<xsl:when test="article-meta/fpage"><xsl:value-of select="article-meta/fpage"/></xsl:when> 
				<xsl:when test="@page"><xsl:value-of select="@page"/></xsl:when>
				<xsl:otherwise><xsl:text>00</xsl:text></xsl:otherwise>			
			</xsl:choose>
		</xsl:attribute>
		<xsl:apply-templates select="article-meta/title-group"/>
		<!-- ne fonctionne plus en 2010, why ? <xsl:apply-templates select="article-meta/article-categories"/> test :-->
		<xsl:apply-templates select="//article-categories"/>  <!-- comme ça, il trouve, et OK  -->
		
		<xsl:apply-templates select="article-meta/contrib-group"/>
		<xsl:apply-templates select="article-meta/aff/addr-line"/>
		<xsl:call-template name="pubdate"/> <!-- 4 pubdate, il en fo une, *** test si tj ppub et epub et si =, et choisir après -->
		<xsl:apply-templates select="article-meta/article-id[@pub-id-type='doi']"/>
		<xsl:apply-templates select="article-meta/article-id[@pub-id-type='pmid']"/>
		<xsl:apply-templates select="article-meta/kwd-group[@kwd-group-type='MESH']"/>
		<!--<xsl:apply-templates select="article-meta/permissions/license[@license-type='open-access']"/>-->
		<xsl:apply-templates select="article-meta/abstract"/>
		<xsl:apply-templates select="article-meta/trans-abstract"/>
		<!-- <xsl:apply-templates select="article-meta"/> -->
	
		
		<xsl:call-template name="source"/>
		<xsl:call-template name="citation"/>
		<xsl:call-template name="fixe"/>
	
	</xsl:element>
</xsl:template>

<xsl:template name="fixe">
	<xsl:element name="dcvalue"><xsl:attribute name="element">identifier</xsl:attribute>
		<xsl:attribute name="qualifier">issn</xsl:attribute>
		<xsl:value-of select="journal-meta/issn[@pub-type='epub']"/>
	</xsl:element>        <!-- 2010, source : <issn pub-type="ppub">0767-0974</issn><issn pub-type="epub">1958-5381</issn> donc OK-->
	<xsl:element name="dcvalue"><xsl:attribute name="element">publisher</xsl:attribute>
		<xsl:choose> <!-- changement de condition après 2013 -->
			<!-- ici : journal-meta/publisher/publisher-name -->
			<xsl:when test="//publisher-name">
			<xsl:value-of select="//publisher-name"/>
		</xsl:when>
			<xsl:otherwise>Éditions EDK, Groupe EDP Sciences</xsl:otherwise>
		
		</xsl:choose>
	</xsl:element>
	<xsl:element name="dcvalue"><xsl:attribute name="element">language</xsl:attribute>
		<xsl:attribute name="qualifier">iso</xsl:attribute>
		<xsl:choose>
			<xsl:when test="@xml:lang"><xsl:value-of select="@xml:lang"/></xsl:when>
			<xsl:otherwise><xsl:text>fr</xsl:text></xsl:otherwise>			
		</xsl:choose>
	</xsl:element>
	
	<!--<xsl:element name="dcvalue">
		<xsl:attribute name="element">rights</xsl:attribute>
		<xsl:attribute name="language">fr</xsl:attribute>
		<xsl:text>Article en libre accès - CC BY 4.0</xsl:text>
	</xsl:element>-->
	

	<xsl:element name="dcvalue"><xsl:attribute name="element">rights</xsl:attribute>
		<xsl:attribute name="language">fr</xsl:attribute>
		<xsl:choose>
			<xsl:when test="article-meta/permissions/license">
				<xsl:text>Article en libre accès - License CC BY 4.0</xsl:text>
			</xsl:when>
			<xsl:otherwise><xsl:text>Article en libre accès</xsl:text></xsl:otherwise>			
		</xsl:choose>
	</xsl:element>
	<xsl:element name="dcvalue"><xsl:attribute name="element">rights</xsl:attribute>
		<xsl:attribute name="qualifier">uri</xsl:attribute>
		<xsl:choose>
			<xsl:when test="article-meta/permissions/license[@license-type='open-access']">
				<xsl:text>http://creativecommons.org/licenses/by/4.0</xsl:text>
			</xsl:when>
			<xsl:otherwise><xsl:text></xsl:text></xsl:otherwise>			
		</xsl:choose>
	</xsl:element>
	
	<xsl:element name="dcvalue">
		<xsl:attribute name="element">rights</xsl:attribute>
		<xsl:attribute name="language">fr</xsl:attribute>
		<xsl:text>Médecine/Sciences - Inserm - SRMS</xsl:text>
	</xsl:element>
	
	<xsl:element name="dcvalue">
		<xsl:attribute name="element">type</xsl:attribute>
		<xsl:text>Article</xsl:text>
	</xsl:element>
</xsl:template>

<xsl:template match="article-meta/title-group">

	<xsl:element name="dcvalue">
		<xsl:attribute name="element">title</xsl:attribute><xsl:attribute name="qualifier">none</xsl:attribute>
		<xsl:attribute name="language"><xsl:value-of select="article-title/@xml:lang"/></xsl:attribute>
		
		<xsl:if test="subtitle='Chroniques génomiques'">
			<xsl:text>Chroniques génomiques - </xsl:text>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="article-title">
				<xsl:apply-templates select="article-title"/>   <!-- dans le 1° exemple, on a un fils 'italic' ; la DTD ne le mentionne pas -->
			</xsl:when>
			<xsl:otherwise><xsl:text>*** chercher le titre principal ***</xsl:text></xsl:otherwise>
		</xsl:choose>
		<xsl:if test="subtitle!='Chroniques génomiques'">
			<xsl:text> : </xsl:text>
			<xsl:value-of select="subtitle"/>
		</xsl:if>
	</xsl:element>
	<!-- au niveau de article-title :
		<trans-title-group xml:lang="en">
			<trans-title>Revisiting HIV-1 assembly</trans-title>
		</trans-title-group> -->
	<xsl:for-each select="trans-title-group"> <!-- plusieurs possibles dans la DTD, et c'est lui qui porte @lang -->
	 <!-- *** vérifier la présence de ti traduits, nouveau 2008-09 *** -->
	<xsl:if test="string-length(normalize-space(trans-title))&gt;'0'">
			<xsl:element name="dcvalue">
				<xsl:attribute name="element">title</xsl:attribute><xsl:attribute name="qualifier">alternative</xsl:attribute>
				<xsl:attribute name="language"><xsl:value-of select="@xml:lang"/> <!-- il est in transtitle-group --></xsl:attribute>
				<xsl:apply-templates select="trans-title"/>  <!-- pas value-of car par ex : un fils trans-title dans lequel 'italic' contient le titre, alors que le sous-titre dans trans-title sans fils, avec blanc en début : à affiner sur exemples -->
			</xsl:element>
		</xsl:if>
	</xsl:for-each>
	<!-- modèle :
	<title-group xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			<article-title xml:lang="fr">L’ambroisie</article-title>
			<subtitle xml:lang="fr">Chronique de l’extension d’un « pollutant biologique » en France</subtitle>
			<trans-title-group xml:lang="en">
				<trans-title>Ragweed (<italic>Ambrosia Artemisiifolia</italic> L.): expansion history of a «biological pollutant» in France</trans-title>
			</trans-title-group>
		</title-group>
-->

</xsl:template>

<!-- rubriques, valeurs à amender, voir Izumi années dans Medecine Sciences/notices, en local -->
<!--	2010 : article-meta/<article-categories>
		<subj-group subj-group-type="section" xml:lang="fr">
			<subject>Éditorial</subject>
		</subj-group>
	</article-categories> -->
	<xsl:template match="article-categories">
	
		<xsl:element name="dcvalue">
			<xsl:attribute name="element">relation</xsl:attribute>
			<xsl:attribute name="qualifier">ispartof</xsl:attribute>
				
	<!-- remplissage de l'élément :
	1 - en 2004, la "rubrique est dans un fils subject, donc on teste pour la suite -->
		<!-- pas utilisé :
			<xsl:variable name="rubrique"> -->
			<xsl:choose>
				<xsl:when test="subj-group[@subj-group-type='section']/subject">
					<xsl:value-of select="subj-group[@subj-group-type='section']/subject"/>
				</xsl:when>		
				<xsl:when test="subj-group[@subj-group-type='section']">
				 	<xsl:value-of select="subj-group[@subj-group-type='section']"/>
				</xsl:when>
				<xsl:otherwise>** rubrique absente **</xsl:otherwise>
			</xsl:choose>
		<!-- </xsl:variable> et si on a des test comme dans les autres années, cidessous, les mettre juste ci-après -->
		</xsl:element>
	</xsl:template>
		
		<!-- 2 - normalisation des rubriques, à continuer : -->				
			<!--	<xsl:choose> 
				
	 2009 : bcp d'erreurs, et traité tout seul après (retour tardif), ce sera plus simple que de reprendre ici. idée :  
				<xsl:when test="$rubrique='M/S revues'">
					<xsl:text>M/S revues : Synthèse</xsl:text>
				</xsl:when>
				<xsl:when test="starts-with($rubrique, 'I - De la conception à la production')">
					<xsl:text>M/S revues : Synthèse : De la conception à la production</xsl:text>
				</xsl:when>
				<xsl:when test="starts-with($rubrique, 'II - La réalité clinique')">
					<xsl:text>M/S revues : Synthèse : La réalité clinique</xsl:text>
				</xsl:when>
				<xsl:when test="starts-with($rubrique, 'Forum : Recherche et partenariat')">
					<xsl:text>Recherche et partenariat</xsl:text>
				</xsl:when>
				<xsl:when test="dcvalue[@element='title']='Brèves'">
					<xsl:text>Le Magazine : Brèves</xsl:text>
				</xsl:when>
				
				<xsl:otherwise><xsl:value-of select="normalize-space($rubrique)"/></xsl:otherwise> 
				
				</xsl:choose> -->
			
				
<!-- 2004 : on a la sous-rubrique, mais pas la rubrique 
EDITORIAL	
	(article Editorial)
	Le mot du mois
LE MAGAZINE	
	Nouvelles
	Brèves ... 
					<xsl:when test="starts-with($rubrique, 'Le mot ')">
						<xsl:text>Editorial : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when> -->
					<!-- cas particulier : inversion, 2004 : 
					<xsl:when test="contains($rubrique, 'Nouvelles : Le ')">
						<xsl:text>Le Magazine : Nouvelles</xsl:text>
						</xsl:when>
					<xsl:when test="contains($rubrique, 'Nouvelles : le ')">
						<xsl:text>Le Magazine : Nouvelles</xsl:text>
						</xsl:when>
					<xsl:when test="contains($rubrique, 'M/S Revues – Série Thématique :')"> -->
<!-- spécif 2002 : 
						<xsl:text>M/S Revues : Série Thématique</xsl:text>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Nouvelles')">
						<xsl:text>Le Magazine : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Brèves')">
						<xsl:text>Le Magazine : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when> -->
	<!-- M/S REVUES	
	(articles de Synthèses)
	"Syndromes coronariens aigues"
	"Polarité"
	Contrôle du mouvement du regard
	Dossier technique
					
					<xsl:when test="starts-with($rubrique, 'Syndrômes coronariens')">
						<xsl:text>M/S Revues : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Polarité')">
						<xsl:text>M/S Revues : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Contrôle du mouvement')">
						<xsl:text>M/S Revues : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Dossier')">
						<xsl:text>M/S Revues : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>  -->

<!-- REPERES	
	Faits et chiffres
	Histoire et Sciences sociales
	Perspective/Horizons
	Prix Nobel 2004
					<xsl:when test="starts-with($rubrique, 'Faits')">
						<xsl:text>Repères : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Histoire et Sciences')">
						<xsl:text>Repères : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Histoire et sciences')">
						<xsl:text>Repères : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>

					<xsl:when test="starts-with($rubrique, 'Perspective')">
						<xsl:text>Repères : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Prix Nobel')">
						<xsl:text>Repères : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>  -->
					
					

<!-- FORUM	
	Chronique bioéthiques
	Chronique génomique
	Hypothèses/Débats
	Recherche et partenariat 
					<xsl:when test="starts-with($rubrique, 'Chronique')">
						<xsl:text>Forum : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Hypothèse')">
						<xsl:text>Forum : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:when test="starts-with($rubrique, 'Recherche')">
						<xsl:text>Forum : </xsl:text>
						<xsl:value-of select="$rubrique"/>
					</xsl:when>
					<xsl:otherwise><xsl:value-of select="normalize-space($rubrique)"/></xsl:otherwise>
				</xsl:choose>				
			</xsl:element>
	</xsl:template> -->
	<!-- Composition des rubriques pour MS 2003
		RUBRIQUES	Sous-rubriques
		EDITORIAL	(article Editorial)
					Le mot du mois
		LE MAGAZINE	Nouvelles
					Brèves
					Dernière heure
		M/S REVUES	(articles de Synthèses)
						Dossier technique
						Série thématique		
		REPERES	
					Faits et chiffres
					Histoire et Sciences sociales
					Perspective/Horizons
					Perspective/Historique
					Prix Nobel 2003
					Horizons
		FORUM	
			Chronique bioéthiques
			Hypothèses/Débats -->
		

<xsl:template match="contrib-group">
	<xsl:for-each select="contrib[@contrib-type='author']">
		<xsl:element name="dcvalue">
			<xsl:attribute name="element">contributor</xsl:attribute><xsl:attribute name="qualifier">author</xsl:attribute>
			<xsl:attribute name="language">-</xsl:attribute>
		<!-- inconstant et pas le même dans l'affil:
			<xsl:attribute name="rid"><xsl:value-of select="xref[@ref-type='corresp']/@rid"/></xsl:attribute> -->
			<xsl:value-of select="name/surname"/><xsl:text>, </xsl:text><xsl:value-of select="name/given-names"/>
		</xsl:element>
	</xsl:for-each>
</xsl:template>

<!-- <aff id="AFF1">
				<addr-line>Équipe Protéines virales et trafics intracellulaires, Département de Maladies Infectieuses, Inserm U.567, Cnrs UMR 8104, Institut Cochin, Bâtiment Gustave Roussy, 27, rue du Faubourg Saint- Jacques, 75014 Paris, France</addr-line>
			</aff> -->
<xsl:template match="aff/addr-line">   <!-- ** revoir si plusieurs affiliations -->
	<xsl:element name="dcvalue">
		<xsl:attribute name="element">contributor</xsl:attribute>
		<xsl:attribute name="qualifier">affiliation</xsl:attribute>
		<!-- à revoir : pas le même que l'affiliation et ici, on n'en a qu'une, sur 'aff' -->
		<!-- <xsl:attribute name="id"><xsl:value-of select="../@id"/></xsl:attribute> -->
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:element>
</xsl:template>

<xsl:template name="pubdate">
<!-- 4 pubdate avec @pub-type="ppub" différent : ppub, epub, final (??? bien plus tardif), given-online. ** Vérifier que ppub =tj epub -->
	<xsl:element name="dcvalue">
		<xsl:attribute name="element">date</xsl:attribute>
		<xsl:attribute name="qualifier">issued</xsl:attribute>
		<xsl:choose>				<!-- On vérifiait que ppub et epub bien pareilles sur le mois ... puis on inactive le mois car trouble le xsl INSERM de génération des liens de Explorer, qui prend l'année là. On privilégie l'année papier, et basta -->				
			<xsl:when test="article-meta/pub-date[@pub-type='ppub']">	 
				<xsl:value-of select="article-meta/pub-date[@pub-type='ppub']/year"/>
				<!-- <xsl:text>-</xsl:text><xsl:value-of select="article-meta/pub-date[@pub-type='ppub']/month"/> -->
				
				<!-- <xsl:variable name="papier" select="article-meta/pub-date[@pub-type='ppub']/month"/>
				<xsl:variable name="num" select="article-meta/pub-date[@pub-type='epub']/month"/>
				<xsl:if test="$papier!=$num">
					<xsl:text>(édition papier); </xsl:text>
					<xsl:value-of select="article-meta/pub-date[@pub-type='epub']/year"/><xsl:text>-</xsl:text>
					<xsl:value-of select="article-meta/pub-date[@pub-type='epub']/month"/>
					<xsl:text>(édition numérique)</xsl:text>
				</xsl:if> -->
			</xsl:when> 	
			<xsl:when test="pub-date[@pub-type='epub']">
				<xsl:value-of select="article-metadata/pub-date[@pub-type='epub']/year"/>
				<!-- <xsl:text>-</xsl:text><xsl:value-of select="article-metadata/pub-date[@pub-type='epub']/month"/> -->
			</xsl:when>
			<!-- variante 2016 num spécial : -->
			<!-- <pub-date date-type="pub" publication-format="print">
				<month>04</month>
				<year>2016</year>
			</pub-date> -->
			<xsl:when test="//pub-date[@publication-format='print']">
				<xsl:value-of select="//pub-date[@publication-format='print']/year"/>
			</xsl:when>
			<xsl:otherwise>** trouver la date **</xsl:otherwise>
		</xsl:choose>
	</xsl:element>
</xsl:template>

<!-- volume, issue, page : source et citation.-->
<xsl:template name="source">
	<xsl:element name="dcvalue">
		<xsl:attribute name="element">source</xsl:attribute>
		<xsl:text>M/S. Médecine sciences [ISSN papier : 0767-0974 ; ISSN numérique : 1958-5381]</xsl:text>
		<xsl:value-of select="article-meta/pub-date[@pub-type='epub']/year"/><xsl:text>, Vol. </xsl:text><xsl:value-of select="article-meta/volume"/>
		<xsl:text>, N° </xsl:text>
			<!-- *** test ajouté pour les HS et NS (HS1 de 2010, à affiner : *** -->
			<xsl:choose>
			<xsl:when test="article-meta/issue">
				<xsl:value-of select="article-meta/issue"/>
			</xsl:when>
			<xsl:otherwise><xsl:text>HS</xsl:text></xsl:otherwise> <!-- variantes à suivre -->
		</xsl:choose>
		<xsl:text>; p. </xsl:text><xsl:value-of select="article-meta/fpage"/>
		<xsl:if test="article-meta/lpage!=article-meta/fpage"><xsl:text>-</xsl:text><xsl:value-of select="article-meta/lpage"/></xsl:if>
	</xsl:element>
</xsl:template>
	
<xsl:template name="citation">
	<xsl:element name="dcvalue">
		<xsl:attribute name="element">identifier</xsl:attribute><xsl:attribute name="qualifier">citation</xsl:attribute>
		<xsl:for-each select="article-meta/contrib-group/contrib[@contrib-type='author']">
			<xsl:value-of select="name/surname"/><xsl:text>, </xsl:text><xsl:value-of select="name/given-names"/>
			<xsl:text> ; </xsl:text>
		</xsl:for-each>
			<xsl:apply-templates select="article-meta/title-group/article-title"/>
		<xsl:if test="article-meta/title-group/subtitle"><xsl:text> : </xsl:text><xsl:value-of select="normalize-space(article-meta/title-group/subtitle)"/></xsl:if>
			<xsl:text>, Med Sci (Paris)</xsl:text>
			<xsl:value-of select="article-meta/pub-date[@pub-type='epub']/year"/><xsl:text>, Vol. </xsl:text><xsl:value-of select="article-meta/volume"/>
			<xsl:text>, N° </xsl:text>
		<!-- *** test ajouté pour les HS et NS (HS1 de 2010, à affiner : *** -->
		<xsl:choose>
			<xsl:when test="article-meta/issue">
				<xsl:value-of select="article-meta/issue"/>
			</xsl:when>
			<xsl:otherwise><xsl:text>HS</xsl:text></xsl:otherwise> <!-- variantes à suivre -->
		</xsl:choose>
			<xsl:text> ; p. </xsl:text><xsl:value-of select="article-meta/fpage"/>
			<xsl:if test="article-meta/lpage!=article-meta/fpage"><xsl:text>-</xsl:text><xsl:value-of select="article-meta/lpage"/></xsl:if>
			<xsl:if test="article-meta/article-id[@pub-id-type='doi']">
				<xsl:text> ; DOI : </xsl:text><xsl:value-of select="article-meta/article-id[@pub-id-type='doi']"/>
			</xsl:if>
	</xsl:element>
</xsl:template>

<!-- identifiants -->
<xsl:template match="article-id[@pub-id-type='doi']">
	<xsl:element name="dcvalue"><xsl:attribute name="element">identifier</xsl:attribute><xsl:attribute name="qualifier">doi</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>

<xsl:template match="article-id[@pub-id-type='pmid']">
		<xsl:element name="dcvalue"><xsl:attribute name="element">identifier</xsl:attribute><xsl:attribute name="qualifier">pmid</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template> 

 <!-- il y a des p avec RC dans l'abstract de cette notice sans espace entre eux, pas de gras ou italique dans la 1°, mais ??? -->
<xsl:template match="abstract">   <!-- et 'abstract', quand on les aura étudiés; détour obligatoire pour le apply-templates -->
<!--	<xsl:if test="abstract">  -->
		<xsl:element name="dcvalue">
			<xsl:attribute name="element">description</xsl:attribute><xsl:attribute name="qualifier">abstract</xsl:attribute>
			<xsl:attribute name="language"><xsl:value-of select="@xml:lang"/></xsl:attribute>
		<!--  résumés de struture variée : normalement p, parfois avec éléments marqués et qui sait quoi d'autre? -->
		<!-- <xsl:apply-templates select="abstract"/> -->
		<xsl:choose>
			<xsl:when test="./p/*">  <!-- des éléments dans les p ; ça existe !  -->
				<xsl:apply-templates/>  <!-- au km, sans s'occuper -->
			</xsl:when>
			<xsl:when test="p">  <!-- structure normale, mais pas d'espace entre eux -->
				<xsl:for-each select="p">
					<xsl:value-of select="normalize-space(.)"/>
					<xsl:if test="position()!=last()"><xsl:text> </xsl:text></xsl:if>
				</xsl:for-each>
			</xsl:when>			<!-- texte sans p, autre -->
			<xsl:otherwise>
				<xsl:text>*** Attention, structure anormale ***</xsl:text>
				<xsl:apply-templates/></xsl:otherwise>
		</xsl:choose>
	</xsl:element>
<!--	</xsl:if> -->
</xsl:template>
<!-- idem -->
<xsl:template match="trans-abstract">
		<xsl:element name="dcvalue"><xsl:attribute name="element">description</xsl:attribute>
			<xsl:attribute name="qualifier">abstract</xsl:attribute>
			<xsl:attribute name="language">
				<xsl:choose>   <!-- il y en avait un sans attribut lang -->
					<xsl:when test="@xml:lang"><xsl:value-of select="@xml:lang"/></xsl:when>
					<xsl:otherwise><xsl:text>en</xsl:text></xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
			  <!-- à compléter comme abstract -->
			  <xsl:choose>
			<xsl:when test="./p/*">  <!-- des éléments dans les p ; ça existe !  -->
				<xsl:apply-templates/>  <!-- au km, sans s'occuper -->
			</xsl:when>
			<xsl:when test="p">  <!-- structure normale, mais pas d'espace entre eux -->
				<xsl:for-each select="p">
					<xsl:value-of select="normalize-space(.)"/>
					<xsl:if test="position()!=last()"><xsl:text> </xsl:text></xsl:if>
				</xsl:for-each>
			</xsl:when>			<!-- texte sans p, autre -->
			<xsl:otherwise>
				<xsl:text>*** Attention, structure anormale ***</xsl:text>
				<xsl:apply-templates/></xsl:otherwise>
		</xsl:choose>

		</xsl:element>
	<!-- </xsl:if> -->
</xsl:template>

<xsl:template match="kwd-group[@kwd-group-type='MESH']">
	<xsl:for-each select="kwd">
		<xsl:element name="dcvalue"><xsl:attribute name="element">subject</xsl:attribute>
		<xsl:attribute name="qualifier">mesh</xsl:attribute>
		<xsl:attribute name="language">fr</xsl:attribute>
		<xsl:value-of select="."/>
		</xsl:element>
	</xsl:for-each>
</xsl:template>

</xsl:stylesheet>
