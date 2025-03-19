from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import openai
import os

# Inicializa o FastAPI
app = FastAPI()

# Configuração da API Key da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rota inicial para testar se o backend está rodando corretamente
@app.get("/")
def home():
    return {"message": "API rodando corretamente!"}

# Modelo para perguntas jurídicas
class Pergunta(BaseModel):
    pergunta: str

# Rota para responder perguntas jurídicas com IA
@app.post("/pergunta")
def responder_pergunta(data: Pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Você é um advogado especializado em direito empresarial e civil."},
            {"role": "user", "content": data.pergunta}
        ]
    )
    return {"resposta": resposta["choices"][0]["message"]["content"]}

# Rota para editar documentos jurídicos
@app.post("/editar_documento")
async def editar_documento(arquivo: UploadFile = File(...)):
    conteudo = await arquivo.read()
    prompt = f"Edite e melhore este documento jurídico:\n\n{conteudo.decode()}"

    resposta = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Você é um advogado especialista na revisão e edição de contratos."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"documento_editado": resposta["choices"][0]["message"]["content"]}
