from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

# Substitua pela sua API Key da OpenAI (pode pegar uma gratuita no site da OpenAI)
openai.api_key = "SUA_API_KEY_AQUI"

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(q: Question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": q.question}]
        )
        return {"answer": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"answer": "Erro ao processar a pergunta."}

