"""Camembert sexe uniquement (module léger si cache / sync défaillant sur d’autres fichiers)."""

import matplotlib.pyplot as plt


def plot_gender_pie(df, gender_col="gender"):
    """Diagramme circulaire (camembert) — répartition par sexe."""
    plt.figure(figsize=(6, 6))
    counts = df[gender_col].value_counts()
    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Répartition des patients selon le sexe (diagramme circulaire)")
    plt.tight_layout()
    plt.show()
