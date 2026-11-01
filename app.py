from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI, NotFoundError, BadRequestError
from pathlib import Path
import os
import json
import re
import traceback

# --------------------
# Setup
# --------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Loads .env locally; on Render the real environment variables are used
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in environment variables")

# Model is configurable (set GROQ_MODEL in .env or on Render)
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()

client = OpenAI(
    api_key=GROQ_API_KEY.strip(),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Serve frontend
# --------------------
if not STATIC_DIR.exists():
    raise RuntimeError(f"static folder not found at: {STATIC_DIR}")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse(STATIC_DIR / "index.html")


# --------------------
# API logic
# --------------------
class CodeRequest(BaseModel):
    code: str


SYSTEM_PROMPT = """
You are a senior code reviewer.

Tasks:
1. Fix syntax/runtime errors only (do not change logic)
2. Provide corrected full code
3. Give metrics from 0-100:
   - quality
   - complexity
   - security
4. Compute overall as the average of the three

Return ONLY valid JSON in this exact format:
{
  "corrected_code": "...",
  "metrics": {
    "quality": 0,
    "complexity": 0,
    "security": 0,
    "overall": 0
  }
}

The corrected_code value must be a properly escaped JSON string (escape newlines as \\n and quotes as \\").
No markdown. No explanations.
"""


def extract_json(text: str) -> dict:
    """Pull the JSON object out of the model reply, even if it adds extra text."""
    text = re.sub(r"```[a-zA-Z]*", "", text).replace("```", "").strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("Model did not return JSON")
    return json.loads(text[start:end + 1])


def clamp(value) -> int:
    try:
        return max(0, min(100, int(round(float(value)))))
    except (TypeError, ValueError):
        return 0


def call_model(code: str):
    """Call Groq. If JSON mode is rejected, retry once without it."""
    kwargs = dict(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": code}
        ],
        temperature=0.2,
        max_completion_tokens=8000,
        extra_body={"reasoning_effort": "low"}
    )
    try:
        return client.chat.completions.create(
            response_format={"type": "json_object"}, **kwargs
        )
    except BadRequestError as e:
        if "model" in str(e).lower() and "decommission" in str(e).lower():
            raise
        return client.chat.completions.create(**kwargs)


# Plain `def` so FastAPI runs it in a thread and doesn't block the server
@app.post("/analyze")
def analyze_code(req: CodeRequest):

    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    try:
        response = call_model(req.code)

        raw = (response.choices[0].message.content or "").strip()
        parsed = extract_json(raw)

        metrics = parsed.get("metrics", {})
        quality = clamp(metrics.get("quality"))
        complexity = clamp(metrics.get("complexity"))
        security = clamp(metrics.get("security"))
        overall = round((quality + complexity + security) / 3)

        return {
            "success": True,
            "output": parsed.get("corrected_code", ""),
            "metrics": {
                "quality": quality,
                "complexity": complexity,
                "security": security,
                "overall": overall
            }
        }

    except NotFoundError:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=(f"Model '{MODEL_NAME}' is not available on Groq. "
                    "Check https://console.groq.com/docs/models and update GROQ_MODEL.")
        )
    except (json.JSONDecodeError, ValueError):
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="AI returned invalid JSON. Try again or use a shorter code snippet."
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
