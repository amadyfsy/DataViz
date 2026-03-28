import os


def create_folder_if_not_exists(path):
    """
    Crée un dossier s'il n'existe pas.
    """
    os.makedirs(path, exist_ok=True)


def print_section(title):
    """
    Affiche un titre de section lisible dans le notebook.
    """
    print("\n" + "=" * 70)
    print(title.upper())
    print("=" * 70)