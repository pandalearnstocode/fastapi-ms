import pandas as pd


def generate_schema(df):
    str_col_mapper = {}
    num_col_mapper = {}
    date_col_mapper = {}
    cols = df.columns.tolist()
    num_cols = df.select_dtypes("number").columns.tolist()
    str_cols = df.select_dtypes("object").columns.tolist()
    date_cols = df.select_dtypes("datetime").columns.tolist()
    for col in str_cols:
        str_col_mapper[col] = df[col].fillna("").sort_values().unique().tolist()
    for col in num_cols:
        num_col_mapper[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "is_na": bool(df[col].isna().any()),
        }
    for col in date_cols:
        date_col_mapper[col] = {"date_freq": None, "date_format": None}
    data_schema = {
        "columns": cols,
        "num_cols": num_cols,
        "str_cols": str_cols,
        "date_cols": date_cols,
        "str_col_metadata": str_col_mapper,
        "num_col_metadata": num_col_mapper,
        "date_col_metadata": date_col_mapper,
    }
    return data_schema