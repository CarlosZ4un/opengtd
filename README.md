# opengtd

Sistema de tarefas inspirado no método GTD (*Getting Things Done*), com pontuação: concluir uma tarefa dá XP e
fracassar tira.

| Pasta | O que tem |
| --- | --- |
| `backend/` | API em Spring Boot (tarefas, perfil e pontuação) |
| `frontend/` | App de celular em HTML, CSS e JavaScript puros |
| `bot/` | Bot do Telegram, para mandar tarefas por mensagem ou por áudio |

## Como rodar

Com o Docker instalado, abra o terminal na pasta do projeto e rode:

```bash
docker compose up -d --build
```

Ele sobe a API em `http://localhost:8080` e o app em `http://localhost:3000`.

- Para voltar aos dados iniciais: `docker compose restart api` (sem `DATABASE_URL`, a API usa um banco H2 em memória).
- Para parar tudo: `docker compose down`.

O bot tem o seu próprio `docker-compose.yml` e precisa dos tokens do `.env` (veja `bot/.env.example`).
