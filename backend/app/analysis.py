"""Utility helpers for computing dashboard data."""

from __future__ import annotations

from typing import List

import pandas as pd

from app.models import DashboardDataset
from app.dataset_store import DatasetRecord


def build_dashboard(records: List[DatasetRecord], preview_rows: int = 3) -> list[DashboardDataset]:
    datasets: list[DashboardDataset] = []
    for record in records:
        preview_frame: pd.DataFrame = record.frame.head(preview_rows)
        datasets.append(
            DashboardDataset(
                dataset_id=record.dataset_id,
                name=record.name,
                rows=record.rows,
                columns=record.columns,
                preview=preview_frame.to_dict(orient="records"),
            )
        )
    return datasets


__all__ = ["build_dashboard"]

