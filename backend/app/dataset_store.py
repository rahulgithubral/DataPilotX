"""Persistent storage for uploaded datasets."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from threading import RLock
from typing import Dict, List, Optional
from uuid import uuid4

import pandas as pd


@dataclass
class DatasetRecord:
    dataset_id: str
    name: str
    rows: int
    columns: int
    path: str
    frame: Optional[pd.DataFrame] = None

    @classmethod
    def from_dict(cls, data: dict) -> "DatasetRecord":
        """Create DatasetRecord from dict (without frame)."""
        return cls(
            dataset_id=data["dataset_id"],
            name=data["name"],
            rows=data["rows"],
            columns=data["columns"],
            path=data["path"],
            frame=None,
        )

    def to_dict(self) -> dict:
        """Convert to dict (excluding frame)."""
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "rows": self.rows,
            "columns": self.columns,
            "path": self.path,
        }


class DataStore:
    """Thread-safe persistent data store."""

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self._lock = RLock()
        if data_dir is None:
            data_dir = Path(__file__).resolve().parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_path = self.data_dir / "datasets.json"
        self._metadata: Dict[str, dict] = {}
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load metadata from datasets.json if it exists."""
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self._metadata = data
                    elif isinstance(data, list):
                        # Handle legacy list format
                        self._metadata = {item["dataset_id"]: item for item in data}
            except Exception:
                self._metadata = {}
        else:
            self._metadata = {}

    def _save_metadata(self) -> None:
        """Save metadata to datasets.json."""
        with open(self.metadata_path, "w") as f:
            json.dump(self._metadata, f, indent=2)

    def add_dataset(self, frame: pd.DataFrame, name: Optional[str] = None) -> DatasetRecord:
        """Add a dataset and save it to disk."""
        dataset_id = str(uuid4())
        csv_path = self.data_dir / f"{dataset_id}.csv"
        
        # Save CSV
        frame.to_csv(csv_path, index=False)
        
        # Create record
        record = DatasetRecord(
            dataset_id=dataset_id,
            name=name or f"dataset-{dataset_id[:8]}",
            rows=int(frame.shape[0]),
            columns=int(frame.shape[1]),
            path=str(csv_path),
            frame=frame.copy(),
        )
        
        # Update metadata
        with self._lock:
            self._metadata[dataset_id] = record.to_dict()
            self._save_metadata()
        
        return record

    def get(self, dataset_id: str) -> Optional[DatasetRecord]:
        """Get a dataset by ID, loading the CSV if needed."""
        with self._lock:
            if dataset_id not in self._metadata:
                return None
            
            meta = self._metadata[dataset_id]
            csv_path = Path(meta["path"])
            
            if not csv_path.exists():
                return None
            
            # Load DataFrame
            try:
                frame = pd.read_csv(csv_path)
            except Exception:
                return None
            
            return DatasetRecord(
                dataset_id=meta["dataset_id"],
                name=meta["name"],
                rows=meta["rows"],
                columns=meta["columns"],
                path=meta["path"],
                frame=frame,
            )

    def list(self) -> List[DatasetRecord]:
        """List all datasets, loading DataFrames."""
        with self._lock:
            records = []
            for dataset_id, meta in self._metadata.items():
                csv_path = Path(meta["path"])
                if csv_path.exists():
                    try:
                        frame = pd.read_csv(csv_path)
                        records.append(
                            DatasetRecord(
                                dataset_id=meta["dataset_id"],
                                name=meta["name"],
                                rows=meta["rows"],
                                columns=meta["columns"],
                                path=meta["path"],
                                frame=frame,
                            )
                        )
                    except Exception:
                        # Skip corrupted files
                        continue
            return records


DATA_STORE = DataStore()


__all__ = ["DATA_STORE", "DataStore", "DatasetRecord"]
