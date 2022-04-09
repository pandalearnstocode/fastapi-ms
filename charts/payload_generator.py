import random

import names
import numpy as np
import pandas as pd


def _clamp(x):
    return max(0, min(x, 255))


def col_gen():
    return "#{0:02x}{1:02x}{2:02x}".format(
        _clamp(random.randint(10, 255)),
        _clamp(random.randint(10, 255)),
        _clamp(random.randint(10, 255)),
    )


def _bar_payload_generator(type="pct"):
    # type = "pct" or "abs"
    label_len = random.randint(1, 10)
    x_max = random.randint(1, 100)
    y_max = random.randint(1, 100)
    df = pd.DataFrame(
        {
            "label": [names.get_full_name() for _ in range(label_len)],
            "X": np.random.uniform(0, x_max, label_len),
            "Y": np.random.uniform(0, y_max, label_len),
        }
    )
    colors = [col_gen() for _ in range(df.shape[1] - 1)]
    df_cols = df.columns.tolist()
    df_cols.remove("label")
    df["pct_X"] = df["X"] / df[["X", "Y"]].sum(1)
    df["pct_Y"] = df["Y"] / df[["X", "Y"]].sum(1)
    df = df.round(2)
    colors_df = pd.DataFrame({"label": df_cols, "fill": colors})
    if type == "pct":
        df_cols = ["pct_" + col for col in df_cols]
        colors_df = pd.DataFrame({"label": df_cols, "fill": colors})
        return {
            "data": df[["pct_X", "pct_Y"]].to_dict("records"),
            "fill": colors_df.to_dict("records"),
            "value_type": type,
            "chart_type": "bar",
        }
    if type == "abs":
        return {
            "data": df[["X", "Y"]].to_dict("records"),
            "fill": colors_df.to_dict("records"),
            "value_type": type,
            "chart_type": "bar",
        }


def _donut_payload_generator(type="pct"):
    label_len = random.randint(1, 10)
    x_max = random.randint(1, 100)
    df = pd.DataFrame(
        {
            "label": [names.get_full_name() for _ in range(label_len)],
            "value": np.random.uniform(0, x_max, label_len),
        }
    )
    if type == "pct":
        df["value"] = df["value"] / df["value"].sum()
    df = df.round(2)
    colors = [col_gen() for _ in range(df["label"].size)]
    colors_df = pd.DataFrame({"label": df["label"].tolist(), "fill": colors})
    return {
        "data": df.to_dict("records"),
        "fill": colors_df.to_dict("records"),
        "value_type": type,
        "chart_type": "donut",
    }


def _line_payload_generator():
    label_len = random.randint(1, 10)
    x_max = random.randint(1, 100)
    y_max = random.randint(1, 100)
    df = pd.DataFrame(
        {
            "label": [names.get_full_name() for _ in range(label_len)],
            "X": np.random.uniform(0, x_max, label_len),
            "Y": np.random.uniform(0, y_max, label_len),
        }
    )
    df = df.round(2)
    colors = [col_gen() for _ in range(df.shape[1] - 1)]
    df_cols = df.columns.tolist()
    df_cols.remove("label")
    colors_df = pd.DataFrame({"label": df_cols, "fill": colors})
    return {
        "data": df.to_dict("records"),
        "fill": colors_df.to_dict("records"),
        "value_type": "abs",
        "chart_type": "line",
    }
