import pandas as pd


def process_coolest_districts_data(data: pd.DataFrame):
    return (
        data[["district", "temperature"]]
        .groupby("district")
        .mean()
        .reset_index()
        .sort_values(by="temperature", ascending=True)
        .head(10)
        .to_dict("records")
    )
