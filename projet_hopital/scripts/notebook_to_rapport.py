from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import nbformat
import os
from bs4 import BeautifulSoup, Comment
import asyncio
import platform


def remove_html_comments(html_content):
    """
    Supprime les commentaires HTML du contenu.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return str(soup)


def add_toc(html_content):
    """
    Ajoute un sommaire hiérarchisé au contenu HTML.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    if not headers:
        return html_content

    toc_items = []
    for header in headers:
        header_text = header.get_text().replace("¶", "").strip()
        header_id = header_text.replace(" ", "-").lower()
        header["id"] = header_id
        toc_items.append(f'<li><a href="#{header_id}">{header_text}</a></li>')

    toc_html = '<div id="toc"><h2>Table of Contents</h2><ul>' + "".join(toc_items) + "</ul></div>"

    if soup.body:
        soup.body.insert(0, BeautifulSoup(toc_html, "html.parser"))

    return str(soup)


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_to_html_plotly(
    notebook_path,
    output_directory=".",
    execute=True,
    timeout=600,
    kernel_name="python3",
):
    """
    Exécute un notebook Jupyter et l’exporte en HTML.
    """
    notebook_path = os.path.abspath(notebook_path)
    output_directory = os.path.abspath(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    if execute:
        executor = ExecutePreprocessor(
            timeout=timeout,
            allow_errors=False,
            kernel_name=kernel_name,
        )
        resources = {"metadata": {"path": os.path.dirname(notebook_path)}}
        executor.preprocess(notebook, resources)

    html_exporter = HTMLExporter(template_name="classic")
    html_exporter.exclude_input = True
    html_exporter.exclude_input_prompt = True
    html_exporter.exclude_output_prompt = True

    resources = {"embed_widgets": True}
    body, _ = html_exporter.from_notebook_node(notebook, resources=resources)

    body = remove_html_comments(body)
    body = add_toc(body)

    notebook_name = os.path.splitext(os.path.basename(notebook_path))[0]
    html_file_path = os.path.join(output_directory, f"{notebook_name}.html")

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    return html_file_path