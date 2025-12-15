from __future__ import annotations

import io
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.analysis import build_dashboard
from app.config import get_settings
from app.llm_factory import get_llm
from app.models import (
    AgentInsightsResponse,
    DashboardResponse,
    ErrorResponse,
    UploadResponse,
)
from app.agent import generate_insights
from app.dataset_store import DATA_STORE
from app.routers.qa import router as qa_router


app = FastAPI(title="DataPilotX Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa_router)


@app.post(
    "/upload",
    response_model=UploadResponse,
    responses={400: {"model": ErrorResponse}},
)
async def upload_dataset(file: UploadFile = File(...)) -> UploadResponse:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported.")

    content = await file.read()
    try:
        frame = pd.read_csv(io.BytesIO(content))
    except Exception as exc:  # pragma: no cover - pandas parsing
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {exc}") from exc

    record = DATA_STORE.add_dataset(frame, name=file.filename)
    return UploadResponse(
        dataset_id=record.dataset_id,
        name=record.name,
        rows=record.rows,
        columns=record.columns,
    )


@app.get("/dashboard", response_model=DashboardResponse)
async def dashboard() -> DashboardResponse:
    records = DATA_STORE.list()
    datasets = build_dashboard(records)
    total_rows = sum(d.rows for d in records)
    return DashboardResponse(
        total_datasets=len(records),
        total_rows=total_rows,
        datasets=datasets,
    )


@app.get(
    "/agent-insights",
    response_model=AgentInsightsResponse,
    responses={404: {"model": ErrorResponse}},
)
async def agent_insights(dataset_id: str) -> AgentInsightsResponse:
    record = DATA_STORE.get(dataset_id)
    if not record:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    llm = get_llm()
    from app.config import LLM_PROVIDER
    provider = LLM_PROVIDER.lower()
    
    def _invoke_llm(llm: Any, prompt: str) -> str:
        """Invoke LLM and extract text response."""
        if hasattr(llm, "invoke"):
            response = llm.invoke(prompt)
            if hasattr(response, "content"):
                return str(response.content)
            return str(response)
        if hasattr(llm, "__call__"):
            result = llm(prompt)
            return str(result) if result else ""
        raise ValueError(f"LLM object {type(llm)} does not support invoke() or __call__()")
    
    predictor = lambda prompt: _invoke_llm(llm, prompt)
    insights = generate_insights(record.frame, predictor, provider)
    return AgentInsightsResponse(dataset_id=record.dataset_id, provider=provider, insights=insights)


@app.get("/health")
async def health() -> JSONResponse:
    settings = get_settings()
    body: dict[str, Any] = {
        "status": "ok",
        "llm_provider": settings.LLM_PROVIDER,
        "datasets_loaded": len(DATA_STORE.list()),
    }
    return JSONResponse(body)


__all__ = ["app"]
