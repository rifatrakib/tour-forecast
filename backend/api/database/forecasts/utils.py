from typing import Any, Dict, List

import pandas as pd


def process_coolest_districts_data(data: pd.DataFrame) -> List[Dict, Any]:
    return (
        data[["district", "temperature"]]
        .groupby("district")
        .mean()
        .reset_index()
        .sort_values(by="temperature", ascending=True)
        .head(10)
        .to_dict("records")
    )


def judge_plan_feasibility(data: pd.DataFrame, start: str, destination: str) -> bool:
    return data[data["district"] == start]["temperature"].values[0] < data[data["district"] == destination]["temperature"].values[0]
