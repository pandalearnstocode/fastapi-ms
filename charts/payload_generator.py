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


def _hist_payload_generate(step=50):
    s = pd.Series(np.random.uniform(0, 1000, size=1000))
    bin_range = np.arange(-200, 1000 + step, step)
    out, bins = pd.cut(
        s, bins=bin_range, include_lowest=True, right=False, retbins=True
    )
    df = (
        out.value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={"index": "name", 0: "freq"})
    )
    x_col = []
    for x in df["name"]:
        x_col.append(x.mid)
    df["name"] = df["name"].astype(str)
    df["name"] = df["name"].str.replace("\[", "", regex=True)
    df["name"] = df["name"].str.replace("\)", "", regex=True)
    df["name"] = df["name"].str.replace("\,", " -", regex=True)
    df["value"] = x_col
    df = df.rename(columns={"name": "label"})
    return {
        "data": df.to_dict("records"),
        "fill": None,
        "value_type": "abs",
        "chart_type": "hist",
    }


def _scatter_payload_generator():
    x = np.linspace(0, 10)
    y = np.random.uniform(0, 100, x.size)
    df = pd.DataFrame({"x": x, "y": y}).round(2).to_dict("records")
    colors_df = pd.DataFrame({"x": col_gen(), "y": col_gen()}).to_dict("records")
    return {
        "data": df.to_dict("records"),
        "fill": colors_df.to_dict("records"),
        "value_type": "abs",
        "chart_type": "scatter",
    }


def random_dates(
    start=pd.to_datetime("2015-01-01"),
    end=pd.to_datetime("2018-01-01"),
    unit="D",
    seed=None,
):
    n = random.randint(4, 12)
    if not seed:  # from piR's answer
        np.random.seed(0)
    ndays = (end - start).days + 1
    return pd.to_timedelta(np.random.rand(n) * ndays, unit=unit) + start


def _waterfall_payload_generator():
    dates_list = (
        pd.Series(random_dates().sort_values())
        .dt.to_period("M")
        .drop_duplicates()
        .astype(str)
        .tolist()
    )
    old_list = [{"uv": float(np.random.uniform(2700, 4500, 1)), "pv": 0}]
    for index in range(1, len(dates_list)):
        old_list.append(
            {
                "uv": old_list[index - 1]["uv"] + old_list[index - 1]["pv"],
                "pv": float(np.random.uniform(-500, 500, 1)),
            }
        )
    old_list[len(dates_list) - 1]["pv"] = 0
    df = pd.DataFrame(old_list)
    df["date"] = dates_list
    df = df.round(2)
    df["date"] = df["date"].astype(str)
    return df.to_dict("records")


def _bubblechart_payload_generator():
    bubble_chart_data_path = "https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/4_ThreeNum.csv"
    df = pd.read_csv(bubble_chart_data_path)
    return df.to_dict("records")
