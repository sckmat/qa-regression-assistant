from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="llm_service_stub", version="0.1.0")


class GenerationRequest(BaseModel):
    prompt: str
    context: list[str] | None = None


@app.get("/health/live")
def health_live():
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready():
    return {"status": "ok"}


@app.post("/v1/generate")
def generate(_: GenerationRequest):
    raise HTTPException(
        status_code=501,
        detail="LLM service is disabled in this environment",
    )