import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def plot_age_distribution(df, age_col="age"):
    plt.figure(figsize=(8, 5))
    sns.histplot(df[age_col], bins=20, kde=True)
    plt.title("Distribution de l'âge des patients")
    plt.xlabel("Âge")
    plt.ylabel("Effectif")
    plt.tight_layout()
    plt.show()


def plot_gender_distribution(df, gender_col="gender"):
    plt.figure(figsize=(6, 4))
    df[gender_col].value_counts().plot(kind="bar")
    plt.title("Répartition des patients selon le sexe")
    plt.xlabel("Sexe")
    plt.ylabel("Effectif")
    plt.tight_layout()
    plt.show()


def plot_top_departments(df, dept_col="department"):
    plt.figure(figsize=(10, 5))
    df[dept_col].value_counts().plot(kind="bar")
    plt.title("Départements recevant le plus de patients")
    plt.xlabel("Département")
    plt.ylabel("Nombre de patients")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_top_diseases(df, disease_col="disease"):
    plt.figure(figsize=(10, 5))
    df[disease_col].value_counts().plot(kind="bar")
    plt.title("Maladies les plus fréquentes")
    plt.xlabel("Maladie")
    plt.ylabel("Nombre de cas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Camembert sexe : module dédié (évite soucis de cache / anciennes versions du fichier)
from .charts_extra import plot_gender_pie  # noqa: E402, F401