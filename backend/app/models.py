"""Pydantic models for API requests and responses."""

from typing import List, Optional

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    dataset_id: str
    name: str
    rows: int
    columns: int


class DashboardDataset(BaseModel):
    dataset_id: str
    name: str
    rows: int
    columns: int
    preview: list[dict] = Field(default_factory=list)


class DashboardResponse(BaseModel):
    total_datasets: int
    total_rows: int
    datasets: List[DashboardDataset]


class QARequest(BaseModel):
    dataset_id: Optional[str] = None
    question: str


class QAResponse(BaseModel):
    dataset_id: str
    provider: str
    answer: str


class AgentInsightsResponse(BaseModel):
    dataset_id: str
    provider: str
    insights: str


class ErrorResponse(BaseModel):
    detail: str
    hint: Optional[str] = None


__all__ = [
    "UploadResponse",
    "DashboardDataset",
    "DashboardResponse",
    "QARequest",
    "QAResponse",
    "AgentInsightsResponse",
    "ErrorResponse",
]

