def create_long_stay_target(df, stay_column="duration_of_stay"):
    """
    Crée une variable binaire indiquant si le séjour est long.
    Séjour long = 1 si durée > moyenne, sinon 0.
    """
    df = df.copy()
    threshold = df[stay_column].mean()
    df["long_stay"] = (df[stay_column] > threshold).astype(int)
    return df, threshold