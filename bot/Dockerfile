FROM python:3.11-slim

# Evita arquivos .pyc e garante logs (print) sem buffer no "docker logs"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instala as dependências primeiro (melhor cache de camadas)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código-fonte
COPY . .

# Executa como usuário sem privilégios
RUN useradd --system --uid 1001 bot
USER bot

# As variáveis de ambiente (TELEGRAM_TOKEN, GROQ_TOKEN, GEMINI_TOKEN,
# OPENGTD_API_URL) são injetadas em tempo de execução — nunca embutidas na imagem.
# Plataformas como o Render injetam PORT; localmente cai no 8000.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
