import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from  transcricao import transcrever_audio
from tarefa import gerar_tarefa, enviar_tarefa


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = FastAPI()

@app.post("/webhook")
async def receber_mensagem(request: Request):

    update = await request.json()

    mensagem = update.get("message")

    if not mensagem:
        return {"ok": True}

    chat_id = mensagem["chat"]["id"]
    usuario = mensagem["from"].get("first_name")

    if "text" in mensagem:
        texto = mensagem["text"]
        print(f"[TEXTO] {usuario} ({chat_id}: {texto})")

    elif "voice" in mensagem:
        file_id = mensagem["voice"]["file_id"]
        duracao = mensagem["voice"]["duration"]
        print(f"[ÁUDIO] {usuario} ({chat_id}: file_id={file_id} {duracao})")
        texto = await transcrever_audio(file_id)
        print(f"[TRANSCRIÇÃO] {texto}")
    else:
        print(f"[OUTRO] Outro tipo de mensagem enviada!")
        return {"ok": True}

    tarefa = await gerar_tarefa(texto)
    print(f"[TAREFA] {tarefa}")
    tarefa_criada = await enviar_tarefa(tarefa)

    return {"ok": True}