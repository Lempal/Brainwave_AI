from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Carrega o .env
load_dotenv()

app = FastAPI()

# Carrega a API KEY do arquivo .env
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("🚨 ERRO: A variável GOOGLE_API_KEY não foi encontrada no .env")
    print("Crie um arquivo .env contendo: GOOGLE_API_KEY=SUA_CHAVE_AQUI")

# URL da API do Gemini
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-pro:generateContent?key={API_KEY}"
)

# Habilitar CORS para permitir seu HTML local chamar o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Pode restringir depois se quiser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados do POST
class Prompt(BaseModel):
    prompt: str
    max_length: int

# Rota principal
@app.post("/api/generate")
def generate(data: Prompt):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": data.prompt}
                ]
            }
        ]
    }

    # Envia requisição para a API do Gemini
    res = requests.post(API_URL, json=payload)
    response_data = res.json()

    # Tenta ler o texto retornado pelo modelo
    try:
        result = response_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Erro ao processar resposta:", e)
        result = "Erro: não foi possível gerar texto."

    return {"result": result}


# Mensagem quando acessar http://localhost:8000/
@app.get("/")
def home():
    return {"status": "API OK", "message": "Use POST /api/generate"}
