import pandas as pd

def split_and_clean(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Splits multi-valued entries (semicolon or comma separated) in `column`
    into separate rows, preserving study metadata.
    Automatically detects title/citation column names.
    """
    # detect metadata columns dynamically
    col_map = {c.lower(): c for c in df.columns}
    title_col = col_map.get("title")
    citation_col = col_map.get("citation")

    # handle missing
    if not title_col or not citation_col:
        print("Warning: 'Title' or 'Citation' column not found in DataFrame.")
        return pd.DataFrame(columns=["title", "citation", column])

    # if target column missing, skip
    if column not in df.columns:
        print(f"Column '{column}' not found.")
        return pd.DataFrame(columns=[title_col, citation_col, column])

    temp = df[[title_col, citation_col, column]].copy()

    # Clean list-like strings and split
    temp[column] = (
        temp[column]
        .astype(str)
        .str.replace(r"[\[\]'\"]", "", regex=True)
        .str.split(r"[;,/]\s*")
    )

    temp = temp.explode(column, ignore_index=True)
    temp[column] = temp[column].str.strip()
    temp = temp[temp[column].notna() & (temp[column] != "")]
    return temp
