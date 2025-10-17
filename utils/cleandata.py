import pandas as pd


def split_and_clean(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Splits multi-valued entries in `column` into separate rows,
    preserving study metadata. Only splits on semicolon or comma.
    Slashes within terms (e.g., ERD/ERS) are preserved.
    """
    required_cols = ["title", "citation", column]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing columns in dataframe: {missing_cols}")

    temp = df[required_cols].copy()

    # Clean list-like strings
    temp[column] = temp[column].astype(str).str.replace(r"[\[\]'\"]", "", regex=True)

    # Split only on ; or , and explode to multiple rows
    exploded = temp[column].str.split(r"[;,]").explode().str.strip()
    
    # Keep metadata aligned by repeating original rows
    df_out = temp.loc[exploded.index, ["title", "citation"]].copy()
    df_out[column] = exploded

    # Drop empty entries
    df_out = df_out[df_out[column].notna() & (df_out[column] != "")]
    df_out.reset_index(drop=True, inplace=True)
    
    return df_out