from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


def build_regression_preprocessor(numeric_features, categorical_features):
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    return ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])


def get_regression_models(preprocessor):
    return {
        "LinearRegression": Pipeline([
            ("preprocessor", preprocessor),
            ("model", LinearRegression())
        ]),
        "RandomForest": Pipeline([
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(random_state=42))
        ]),
        "GradientBoosting": Pipeline([
            ("preprocessor", preprocessor),
            ("model", GradientBoostingRegressor(random_state=42))
        ])
    }
