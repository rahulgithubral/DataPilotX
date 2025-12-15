import os
from typing import Any

try:
    from langchain_groq import ChatGroq
except:
    ChatGroq = None

class DummyLLM:
    def __call__(self, prompt: str) -> str:
        return "Dummy answer (no Groq key). SUGGESTED_CHARTS: [{\"type\":\"bar\",\"x\":\"category\",\"y\":\"sales\"}]"

def get_llm() -> Any:
    groq_key = os.getenv("GROQ_API_KEY")
    # Try current models in order of preference
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if groq_key and ChatGroq:
        try:
            return ChatGroq(model=model, api_key=groq_key)
        except Exception as e:
            # Fallback to mixtral if llama-3.3 fails
            try:
                fallback_model = "mixtral-8x7b-32768"
                print(f"Primary model failed, trying fallback {fallback_model}: {e}")
                return ChatGroq(model=fallback_model, api_key=groq_key)
            except Exception as e2:
                print("Groq model failed, using DummyLLM:", e2)
                return DummyLLM()

    print("Using DummyLLM (no GROQ_API_KEY or ChatGroq not installed)")
    return DummyLLM()
