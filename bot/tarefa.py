import os
from datetime import datetime
from typing import Literal, Optional

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
OPENGTD_API_URL = os.getenv("OPENGTD_API_URL")

gemini_client = genai.Client(api_key=GEMINI_TOKEN)

class TarefaIA(BaseModel):
    titulo: str
    descricao: str
    peso: Literal["tranquila", "complicada", "intensa"]
    status: Literal["espera", "andamento"]
    data_hora: Optional[str] = None
    tags: list[str]


PROMPT = """Você recebe uma mensagem de um usuário e deve transformá-la em uma tarefa.

Regras:
- titulo: curto e direto, começando com um verbo (ex: "Lavar a louça").
- descricao: detalhes da tarefa com base na mensagem.
- peso: classifique o esforço da tarefa:
  - "tranquila": simples e rápida
  - "complicada": exige atenção ou algumas etapas
  - "intensa": longa, difícil ou muito trabalhosa
- status: "andamento" se o usuário disser que já começou, senão "espera".
- data_hora: se a mensagem citar quando a tarefa deve ser feita, devolva no formato
  ISO "AAAA-MM-DDTHH:MM". Se não citar, devolva null.
  Agora é {agora}.
- tags: de 1 a 3 palavras curtas em minúsculo que categorizem a tarefa.

Mensagem: {mensagem}"""

async def gerar_tarefa(mensagem):
    agora = datetime.now().strftime("%Y-%m-%dT%H:%M (%A)")

    resposta = await gemini_client.aio.models.generate_content(
        model="gemini-3.5-flash",
        contents=PROMPT.format(agora=agora, mensagem=mensagem),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TarefaIA,
        ),
    )
    tarefa_ia = resposta.parsed
    timestamp = None
    if tarefa_ia.data_hora:
        timestamp = int(datetime.fromisoformat(tarefa_ia.data_hora).timestamp())

    return {
        "titulo": tarefa_ia.titulo,
        "descricao": tarefa_ia.descricao,
        "peso": tarefa_ia.peso,
        "timestamp": timestamp,
        "status": tarefa_ia.status,
        "tags": tarefa_ia.tags,
    }

async def enviar_tarefa(tarefa):
    async with httpx.AsyncClient() as client:
        resposta = await client.post(f"{OPENGTD_API_URL}/tarefas", json=tarefa)
        resposta.raise_for_status()
        return resposta.json()
