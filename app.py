from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in .env")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
4. Compute overall as average

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

No markdown. No explanations.
"""


@app.post("/analyze")
async def analyze_code(req: CodeRequest):

    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    try:
        response = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": req.code}
            ],
            temperature=0.2,
            max_tokens=2000
        )

        raw = response.choices[0].message.content.strip()

        # Clean accidental fences
        raw = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "").strip()

        parsed = json.loads(raw)

        return {
            "success": True,
            "output": parsed["corrected_code"],
            "metrics": parsed["metrics"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
