#!/usr/bin/env python3
"""
Analyse complète sans Jupyter : charge les données, graphiques, ML.

Usage (depuis n'importe quel répertoire) :
  python /chemin/vers/projet_hopital/scripts/run_analysis.py

Ou depuis projet_hopital :
  python scripts/run_analysis.py

Les figures sont enregistrées dans projet_hopital/visuals/run_cli/
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "visuals" / "run_cli"
FIG_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_fig_n = [0]


def _show_save() -> None:
    _fig_n[0] += 1
    path = FIG_DIR / f"fig_{_fig_n[0]:03d}.png"
    plt.savefig(path, bbox_inches="tight", dpi=120)
    plt.close()
    print(f"  Figure -> {path.relative_to(ROOT)}")


plt.show = _show_save  # type: ignore[method-assign]

import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

import src.config as _cfg
import src.data_loader as _dl
import src.preprocessing as _prep

from src.config import DATA_FILE, TEST_SIZE, RANDOM_STATE
from src.data_loader import load_data
from src.evaluation import evaluate_classification, evaluate_regression
from src.feature_engineering import create_long_stay_target
from src.ml_importance import (
    classification_permutation_importance,
    regression_permutation_importance,
)
from src.models.classification import (
    build_classification_preprocessor,
    get_classification_models,
)
from src.models.regression import build_regression_preprocessor, get_regression_models
from src.visualization.charts_extra import plot_gender_pie
from src.visualization.cost_viz import (
    plot_cost_by_department,
    plot_cost_by_treatment,
    plot_stay_vs_cost,
    plot_top_costly_diseases,
)
from src.visualization.duration_plots import plot_mean_stay_by_disease
from src.visualization.exploration_viz import (
    plot_age_distribution,
    plot_gender_distribution,
    plot_top_departments,
    plot_top_diseases,
)
from src.visualization.hospitalisation_viz import (
    plot_age_vs_stay,
    plot_stay_by_department,
    plot_treatment_distribution,
)


def main() -> None:
    importlib.reload(_cfg)
    importlib.reload(_dl)
    importlib.reload(_prep)
    clean_data = _prep.clean_data
    sns.set_theme(style="whitegrid")

    print("=== Chargement ===")
    df = clean_data(load_data(DATA_FILE))
    print(f"Dimensions: {df.shape}")
    print(f"Colonnes: {list(df.columns)}")

    print("\n=== Visualisations ===")
    plot_age_distribution(df)
    plot_gender_distribution(df)
    plot_gender_pie(df)
    plot_top_departments(df)
    plot_top_diseases(df)
    print("Durée moyenne de séjour:", df["duration_of_stay"].mean())
    avg_stay_dept = df.groupby("department")["duration_of_stay"].mean().sort_values(ascending=False)
    print(avg_stay_dept.head().to_string())
    avg_stay_dis = df.groupby("disease")["duration_of_stay"].mean().sort_values(ascending=False)
    print(avg_stay_dis.head(10).to_string())
    plot_mean_stay_by_disease(df)
    plot_stay_by_department(df)
    plot_treatment_distribution(df)
    plot_age_vs_stay(df)
    print("Coût moyen:", df["cost"].mean())
    plot_cost_by_department(df)
    plot_top_costly_diseases(df)
    plot_stay_vs_cost(df)
    plot_cost_by_treatment(df)

    print("\n=== Régression (coût) ===")
    features = ["age", "gender", "department", "disease", "treatment", "duration_of_stay"]
    X = df[features]
    y = df["cost"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    prep = build_regression_preprocessor(
        ["age", "duration_of_stay"],
        ["gender", "department", "disease", "treatment"],
    )
    models = get_regression_models(prep)
    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        m = evaluate_regression(y_test, y_pred)
        m["Model"] = name
        rows.append(m)
    reg_df = pd.DataFrame(rows).sort_values(by="R2", ascending=False)
    print(reg_df.to_string(index=False))
    best_name = reg_df.iloc[0]["Model"]
    imp = regression_permutation_importance(
        models[best_name], X_test, y_test, features, random_state=RANDOM_STATE
    )
    print("\nImportance (permutation, meilleur modèle):")
    print(imp.to_string(index=False))

    print("\n=== Classification (séjour long) ===")
    dfc, threshold = create_long_stay_target(df, stay_column="duration_of_stay")
    print(f"Seuil durée: {threshold:.3f}")
    feats_c = ["age", "gender", "department", "disease", "treatment", "cost"]
    Xc = dfc[feats_c]
    yc = dfc["long_stay"]
    Xtr, Xte, ytr, yte = train_test_split(
        Xc, yc, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    prep_c = build_classification_preprocessor(
        ["age", "cost"],
        ["gender", "department", "disease", "treatment"],
    )
    models_c = get_classification_models(prep_c)
    rows_c = []
    for name, model in models_c.items():
        model.fit(Xtr, ytr)
        yp = model.predict(Xte)
        ev = evaluate_classification(yte, yp)
        ev["Model"] = name
        rows_c.append(ev)
    clf_df = pd.DataFrame(rows_c).sort_values(by="F1-score", ascending=False)
    print(clf_df.to_string(index=False))
    best_c = clf_df.iloc[0]["Model"]
    imp_c = classification_permutation_importance(
        models_c[best_c], Xte, yte, feats_c, random_state=RANDOM_STATE
    )
    print("\nImportance (permutation, meilleur modèle):")
    print(imp_c.to_string(index=False))

    print(f"\nTerminé. {_fig_n[0]} figures dans {FIG_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
