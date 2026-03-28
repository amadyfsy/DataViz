def standardize_columns(df):
    """
    Standardise les noms de colonnes (minuscules, espaces → _, sans BOM).
    """
    df = df.copy()

    def _norm(c):
        s = str(c).strip().lower().replace(" ", "_")
        return s.lstrip("\ufeff")

    df.columns = [_norm(c) for c in df.columns]
    return df


# Après normalisation (minuscules), alignement sur les noms attendus par le notebook (anglais)
_FRENCH_TO_ENGLISH = {
    "patientid": "patient_id",
    "sexe": "gender",
    "departement": "department",
    "maladie": "disease",
    "dureesejour": "duration_of_stay",
    "cout": "cost",
    "dateadmission": "date_admission",
    "datesortie": "date_discharge",
    "traitement": "treatment",
}


def map_columns_to_english(df):
    df = df.copy()
    rename = {}
    for fr, en in _FRENCH_TO_ENGLISH.items():
        if fr not in df.columns:
            continue
        if en in df.columns and fr != en:
            df = df.drop(columns=[fr])
            continue
        rename[fr] = en
    return df.rename(columns=rename)


def remove_duplicates(df):
    """
    Supprime les doublons.
    """
    df = df.copy()
    return df.drop_duplicates()


def handle_missing_values(df):
    """
    Gestion simple des valeurs manquantes.
    Cette version laisse sklearn gérer la suite dans les pipelines.
    """
    df = df.copy()
    return df


def clean_data(df):
    """
    Pipeline global de nettoyage.
    """
    df = standardize_columns(df)
    df = map_columns_to_english(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    return df