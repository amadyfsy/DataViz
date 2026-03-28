"""Graphiques liés à la durée de séjour (module dédié pour éviter imports cassés)."""

import matplotlib.pyplot as plt


def plot_mean_stay_by_disease(df, disease_col="disease", stay_col="duration_of_stay"):
    """Durée moyenne de séjour par maladie (séjours les plus longs)."""
    avg = df.groupby(disease_col)[stay_col].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    avg.plot(kind="bar", color="steelblue")
    plt.title("Durée moyenne de séjour par maladie")
    plt.xlabel("Maladie")
    plt.ylabel("Durée moyenne (jours)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
