import json
import re
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd

from app.dataset_store import DATA_STORE
from app.llm_factory import get_llm
from app.config import LLM_PROVIDER

router = APIRouter(tags=["qa"])


class QARequest(BaseModel):
    question: str
    dataset_id: Optional[str] = None


@router.post("/qa")
async def qa(payload: QARequest):
    try:
        dataset_id = payload.dataset_id
        if dataset_id is None:
            records = DATA_STORE.list()
            if not records:
                raise HTTPException(status_code=404, detail="No datasets uploaded yet.")
            dataset_id = records[-1].dataset_id

        record = DATA_STORE.get(dataset_id)
        if not record:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        if record.frame is None:
            raise HTTPException(status_code=500, detail="Failed to load dataset.")

        llm = get_llm()
        provider = LLM_PROVIDER.lower()
        
        # Build context from dataset
        context = f"Dataset columns: {list(record.frame.columns)}\nSample data:\n{record.frame.head().to_string()}"
        prompt = f"""{context}

Question: {payload.question}

You must respond with ONLY valid JSON (no markdown, no backticks, no explanations). The JSON must have these exact keys:
- "answer": short, final business answer only
- "reasoning": maximum 1 sentence explaining your approach
- "code": python/pandas code to compute the answer (code only, no comments)

Return ONLY the JSON object:"""
        
        try:
            if hasattr(llm, "invoke"):
                response = llm.invoke(prompt)
                if hasattr(response, "content"):
                    raw_text = str(response.content)
                else:
                    raw_text = str(response)
            elif hasattr(llm, "__call__"):
                raw_text = str(llm(prompt))
            else:
                raw_text = "LLM error: Unsupported LLM type"
        except Exception as e:
            raw_text = f"LLM error: {str(e)}"

        # Parse JSON from response
        parsed_response = {"answer": raw_text, "reasoning": None, "code": None}
        try:
            # Try to extract JSON from the response (handle cases where LLM adds markdown)
            cleaned_text = raw_text.strip()
            # Remove markdown code blocks if present
            cleaned_text = re.sub(r'^```json\s*', '', cleaned_text, flags=re.MULTILINE)
            cleaned_text = re.sub(r'^```\s*', '', cleaned_text, flags=re.MULTILINE)
            cleaned_text = re.sub(r'\s*```$', '', cleaned_text, flags=re.MULTILINE)
            cleaned_text = cleaned_text.strip()
            
            # Try to find JSON object in the text (handle nested objects)
            start_idx = cleaned_text.find('{')
            if start_idx != -1:
                # Find matching closing brace
                brace_count = 0
                end_idx = start_idx
                for i in range(start_idx, len(cleaned_text)):
                    if cleaned_text[i] == '{':
                        brace_count += 1
                    elif cleaned_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                if brace_count == 0:
                    cleaned_text = cleaned_text[start_idx:end_idx]
            
            parsed = json.loads(cleaned_text)
            if isinstance(parsed, dict):
                parsed_response = {
                    "answer": parsed.get("answer", raw_text),
                    "reasoning": parsed.get("reasoning"),
                    "code": parsed.get("code"),
                }
        except (json.JSONDecodeError, AttributeError, KeyError, ValueError):
            # Fallback to default structure if parsing fails
            pass

        return {
            "answer": parsed_response["answer"],
            "reasoning": parsed_response["reasoning"],
            "code": parsed_response["code"],
            "dataset_id": dataset_id,
            "provider": provider
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
