import pandas as pd


def retro_dictify(frame):
    d = {}
    for row in frame.values:
        here = d
        for elem in row[:-2]:
            if elem not in here:
                here[elem] = {}
            here = here[elem]
        here[row[-2]] = row[-1]
    return d

def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return list(frame.values.squeeze())
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:,1:]) for k,g in grouped}
    return d

def hierarchy_flat(df, hierarchy_cols = None):
    if hierarchy_cols is None:
        hierarchy_cols = df.select_dtypes('object').nunique().index.tolist()
    df = df[hierarchy_cols]
    df = df.sort_values(hierarchy_cols).drop_duplicates()
    df = df.reset_index(drop = True)
    return df

def hierarchy_nested(df, hierarchy_cols = None):
    df_flat = hierarchy_flat(df, hierarchy_cols)
    return recur_dictify(df_flat)

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