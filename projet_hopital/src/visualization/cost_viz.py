import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def plot_cost_by_department(df, dept_col="department", cost_col="cost"):
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x=dept_col, y=cost_col)
    plt.title("Coût d’hospitalisation par département")
    plt.xlabel("Département")
    plt.ylabel("Coût")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_top_costly_diseases(df, disease_col="disease", cost_col="cost"):
    avg_cost = df.groupby(disease_col)[cost_col].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    avg_cost.plot(kind="bar")
    plt.title("Maladies générant les coûts moyens les plus élevés")
    plt.xlabel("Maladie")
    plt.ylabel("Coût moyen")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_stay_vs_cost(df, stay_col="duration_of_stay", cost_col="cost"):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x=stay_col, y=cost_col)
    plt.title("Relation entre durée de séjour et coût")
    plt.xlabel("Durée de séjour")
    plt.ylabel("Coût")
    plt.tight_layout()
    plt.show()


def plot_cost_by_treatment(df, treatment_col="treatment", cost_col="cost"):
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x=treatment_col, y=cost_col)
    plt.title("Comparaison des coûts selon les traitements")
    plt.xlabel("Traitement")
    plt.ylabel("Coût")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()