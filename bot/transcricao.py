import os
import httpx
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
GROQ_TOKEN=os.getenv("GROQ_TOKEN")

groq_client = AsyncGroq(api_key=GROQ_TOKEN)

async def baixar_audio_telegram(file_id):
    async with httpx.AsyncClient() as client:

        resposta = await client.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile",
            params={"file_id": file_id},
        )
        file_path = resposta.json()["result"]["file_path"]

        audio = await client.get(
            f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
        )
        return audio.content


async def transcrever_audio(file_id):
    audio_byte = await baixar_audio_telegram(file_id)

    transcricao = await groq_client.audio.transcriptions.create(
        file=("audio.ogg", audio_byte),
        model="whisper-large-v3-turbo",
        language="pt",
    )
    return transcricao.text