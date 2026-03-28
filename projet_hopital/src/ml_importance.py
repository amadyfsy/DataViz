import pandas as pd
from sklearn.inspection import permutation_importance


def regression_permutation_importance(
    model, X_test, y_test, feature_names, random_state=42, n_repeats=15
):
    """Importance des variables par permutation (baisse de R² si la variable est mélangée)."""
    r = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=n_repeats,
        random_state=random_state,
        scoring="r2",
    )
    return (
        pd.DataFrame(
            {
                "variable": list(feature_names),
                "importance_moyenne": r.importances_mean,
                "importance_ecart_type": r.importances_std,
            }
        )
        .sort_values("importance_moyenne", ascending=False)
        .reset_index(drop=True)
    )


def classification_permutation_importance(
    model, X_test, y_test, feature_names, random_state=42, n_repeats=15
):
    """Importance des variables par permutation (baisse de précision / score par défaut)."""
    r = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=n_repeats,
        random_state=random_state,
        scoring="accuracy",
    )
    return (
        pd.DataFrame(
            {
                "variable": list(feature_names),
                "importance_moyenne": r.importances_mean,
                "importance_ecart_type": r.importances_std,
            }
        )
        .sort_values("importance_moyenne", ascending=False)
        .reset_index(drop=True)
    )
