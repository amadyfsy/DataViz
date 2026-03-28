from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import nbformat
import os
from bs4 import BeautifulSoup, Comment

# import nbformat
import asyncio
import platform


# ----------------------------------------------------------------------
# Supprimer les commentaires
# ----------------------------------------------------------------------
def remove_html_comments(html_content):
    """
    Fonction pour supprimer les commentaires HTML du contenu.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return str(soup)


# -----------------------------------------------------------------------
# ajout de commentaire
# ----------------------------------------------------------------------


def add_toc(html_content):
    """
    Fonction pour ajouter un sommaire (table of contents) au contenu HTML avec une hiérarchie de sections.

    Parameters:
    html_content (str): Contenu HTML du notebook.

    Returns:
    str: Contenu HTML avec le sommaire hiérarchisé ajouté.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Trouver tous les titres
    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    if not headers:
        return html_content

    # Initialisation de la hiérarchie des niveaux de titres
    toc_list = []
    current_level = 0
    toc_stack = []

    def add_to_toc(header, level):
        nonlocal current_level, toc_stack

        # Enlever les symboles de paragraphe
        header_text = header.get_text().replace("¶", "").strip()
        header_id = header_text.replace(" ", "-").lower()
        header["id"] = header_id

        # Créer un nouvel item pour le sommaire
        toc_item = f'<li><a href="#{header_id}">{header_text}</a>'

        # Initialisation de toc_stack si vide
        if not toc_stack:
            toc_stack.append(toc_item)
        else:
            # Si c'est un sous-titre (h2 ou plus), on l'ajoute au niveau approprié
            if level > current_level:
                # Ajouter une sous-liste pour les sous-sections
                toc_stack[-1] += "<ul>"
                toc_stack.append(toc_item)
            elif level == current_level:
                toc_stack[-1] += "</li>"
                toc_stack.append(toc_item)
            else:
                # Fermer les sous-listes jusqu'à revenir au bon niveau
                while current_level > level:
                    toc_stack[-1] += "</li></ul>"
                    current_level -= 1
                toc_stack[-1] += "</li>"
                toc_stack.append(toc_item)

        current_level = level

    # Ajouter chaque titre à la table des matières hiérarchique
    for header in headers:
        level = int(header.name[1])  # h1 -> 1, h2 -> 2, etc.
        add_to_toc(header, level)

    # Fermer toutes les balises <ul> restantes
    while current_level > 0:
        toc_stack[-1] += "</li></ul>"
        current_level -= 1

    # Fermer la dernière balise <li>
    if toc_stack:
        toc_stack[-1] += "</li>"

    # Générer le HTML final du sommaire
    toc_html = (
        '<div id="toc"><h2>Table of Contents</h2><ul>'
        + "".join(toc_stack)
        + "</ul></div>"
    )

    # Insérer le sommaire au début du body
    body_tag = soup.body
    if body_tag:
        body_tag.insert(0, BeautifulSoup(toc_html, "html.parser"))

    return str(soup)


# Corriger l'avertissement "Proactor event loop..." sous Windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# -----------------------------------------------------------------------------------------------------
# convertir notebook to HTML
# -----------------------------------------------------------------------------------------------------


def notebook_to_html_plotly(
    notebook_path,
    output_directory=".",
    execute=True,
    timeout=600,
    kernel_name="python3",
):
    """
    Convertit un fichier Jupyter Notebook en HTML, en exécutant toutes les cellules,
    tout en conservant les graphiques Plotly interactifs dans le rapport final.

    Paramètres
    ----------
    notebook_path : str
        Chemin vers le fichier Jupyter Notebook (.ipynb).
    output_directory : str
        Répertoire où enregistrer le fichier HTML (par défaut : répertoire courant).
    execute : bool
        Si True, exécute le notebook avant export (sinon utilise les sorties déjà sauvegardées).
    timeout : int
        Délai max par cellule (secondes).
    kernel_name : str
        Nom du noyau Jupyter (ex. python3).

    Retour
    ------
    str
        Chemin vers le fichier HTML créé.
    """

    notebook_path = os.path.abspath(notebook_path)
    output_directory = os.path.abspath(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    # 1. Lire le contenu du notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_content = f.read()

    # 2. Charger le notebook au format nbformat
    notebook = nbformat.reads(notebook_content, as_version=4)

    # 3. Exécuter le notebook (cwd = dossier du notebook, important pour sys.path / chemins relatifs)
    if execute:
        executor = ExecutePreprocessor(
            timeout=timeout,
            allow_errors=False,
            kernel_name=kernel_name,
        )
        resources = {"metadata": {"path": os.path.dirname(notebook_path)}}
        executor.preprocess(notebook, resources)

    # 4. Créer un Exporter HTML sans exclure la sortie
    html_exporter = HTMLExporter(template_name="classic")
    html_exporter.exclude_input = True  # Masquer le code
    html_exporter.exclude_input_prompt = True  # Masquer "In[x]"
    html_exporter.exclude_output_prompt = True  # Masquer "Out[x]"
    # IMPORTANT: Ne pas mettre "html_exporter.exclude_output = True"
    #            sinon les graphiques ne s'afficheront pas.

    # Passer 'embed_widgets': True dans resources
    resources = {"embed_widgets": True}

    # 5. Convertir le notebook en contenu HTML
    (body, _) = html_exporter.from_notebook_node(notebook, resources=resources)

    # 6. (Optionnel) Supprimer les commentaires HTML
    body = remove_html_comments(body)

    # 7. (Optionnel) Ajouter un sommaire en fonction des titres HTML
    body = add_toc(body)

    # 8. Définir le nom et le chemin du fichier HTML de sortie
    notebook_name = os.path.splitext(os.path.basename(notebook_path))[0]
    html_file_path = os.path.join(output_directory, f"{notebook_name}.html")

    # 9. Écrire le contenu HTML dans le fichier final
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    return html_file_path
