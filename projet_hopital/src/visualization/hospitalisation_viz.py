import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def plot_stay_by_department(df, dept_col="department", stay_col="duration_of_stay"):
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x=dept_col, y=stay_col)
    plt.title("Durée de séjour par département")
    plt.xlabel("Département")
    plt.ylabel("Durée de séjour")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_treatment_distribution(df, treatment_col="treatment"):
    plt.figure(figsize=(10, 5))
    df[treatment_col].value_counts().plot(kind="bar")
    plt.title("Répartition des traitements")
    plt.xlabel("Traitement")
    plt.ylabel("Effectif")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_age_vs_stay(df, age_col="age", stay_col="duration_of_stay"):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x=age_col, y=stay_col)
    plt.title("Relation entre âge et durée de séjour")
    plt.xlabel("Âge")
    plt.ylabel("Durée de séjour")
    plt.tight_layout()
    plt.show()


from .duration_plots import plot_mean_stay_by_disease  # noqa: E402, F401