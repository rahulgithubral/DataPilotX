"""Agent-style insights using LLM."""

from __future__ import annotations

from typing import Callable

import pandas as pd


def generate_insights(
    frame: pd.DataFrame, predict: Callable[[str], str], provider: str
) -> str:
    if provider == "local":
        desc = frame.describe(include="all", datetime_is_numeric=True).to_csv()
        return f"Local insights generated.\nSummary statistics:\n{desc}"

    prompt = (
        "You are a senior data analyst. Provide 3-5 concise insights about the dataset. "
        "Highlight potential quality issues and interesting patterns. "
        "Return bullet points.\n\n"
        "DATA PREVIEW:\n"
        f"{frame.head(5).to_markdown(index=False)}\n"
        "COLUMN INFO:\n"
        f"{', '.join(frame.columns.tolist())}"
    )
    return predict(prompt)


__all__ = ["generate_insights"]

