from pathlib import Path

import pandas as pd


def _resolve_data_path(path) -> Path:
    """Si le chemin fourni n'existe pas, essaie les emplacements habituels sous projet_hopital/data."""
    p = Path(path).expanduser()
    if p.is_file():
        return p
    from src.config import BASE_DIR

    candidates = (
        BASE_DIR / "data" / "hospital_data.csv",
        BASE_DIR / "data" / "raw" / "hospitalisations.csv",
    )
    for cand in candidates:
        if cand.is_file():
            return cand
    raise FileNotFoundError(
        f"Fichier introuvable : {path}. Emplacements testés : "
        + ", ".join(str(c) for c in (p, *candidates))
    )


def _detect_sep(file_path: Path) -> str:
    with open(file_path, encoding="utf-8") as f:
        line = f.readline()
    return ";" if line.count(";") > line.count(",") else ","


def load_data(path):
    """
    Charge les données depuis un fichier CSV.
    Accepte un chemin obsolète (ex. ancien DATA_FILE en cache) et retombe sur data/hospital_data.csv.
    """
    p = _resolve_data_path(path)
    return pd.read_csv(p, sep=_detect_sep(p), encoding="utf-8")


def get_head(df, n=5):
    """
    Retourne les premières lignes du dataset.
    """
    return df.head(n)


def get_shape(df):
    """
    Retourne les dimensions du dataset.
    """
    return df.shape


def get_columns(df):
    """
    Retourne la liste des colonnes.
    """
    return df.columns.tolist()


def get_dtypes(df):
    """
    Retourne les types des colonnes.
    """
    return df.dtypes


def get_missing_values(df):
    """
    Retourne le nombre de valeurs manquantes par colonne.
    """
    return df.isnull().sum()


def get_descriptive_stats(df):
    """
    Retourne les statistiques descriptives.
    """
    return df.describe(include="all")

from sklearn.model_selection import train_test_split


def clean_data(df):
    df = df.copy()
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.drop_duplicates()
    return df


def create_long_stay_target(df, stay_column="duree_sejour"):
    df = df.copy()
    threshold = df[stay_column].mean()
    df["sejour_long"] = (df[stay_column] > threshold).astype(int)
    return df, threshold


def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)