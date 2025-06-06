from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

JUDGE0_URL = os.getenv("JUDGE0_API_URL")
JUDGE0_KEY = os.getenv("JUDGE0_API_KEY")

HEADERS = {
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": "06d8f0b530mshcb77422fad3e123p114a4ajsndecb73c6f3ee'",
    "content-type": "application/json"
}

class CodeRequest(BaseModel):
    source_code: str
    language_id: int  # Ejemplo: 71 = Python 3

@app.post("/run-code")
async def run_code(code: CodeRequest):
    payload = {
        "source_code": code.source_code,
        "language_id": code.language_id,
        "stdin": ""
    }

    async with httpx.AsyncClient() as client:
        # Crear la ejecución
        response = await client.post(f"{JUDGE0_URL}/submissions?base64_encoded=false&wait=true",
                                     json=payload, headers=HEADERS)
        if response.status_code != 201:
            raise HTTPException(status_code=500, detail="Error al enviar código a Judge0")

        result = response.json()
        return {
            "stdout": result.get("stdout"),
            "stderr": result.get("stderr"),
            "compile_output": result.get("compile_output"),
            "status": result.get("status", {}).get("description")
        }
