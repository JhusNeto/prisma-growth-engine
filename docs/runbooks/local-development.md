# Runbook — ambiente local Apple Silicon

## Início

1. Abra a pasta prisma-growth-engine no PyCharm.
2. Configure o interpretador para .venv/bin/python.
3. Copie .env.example para .env e troque todos os valores demonstrativos.
4. Execute docker compose up -d postgres n8n.
5. Inicie FastAPI e Astro pelos comandos no README.

## Verificação

~~~zsh
docker compose ps
curl -fsS http://localhost:8000/health
curl -I http://localhost:4321
~~~

O n8n abre em http://localhost:5678. No primeiro uso, crie a conta de proprietário localmente.

## Parada segura

~~~zsh
docker compose down
~~~

Isso mantém os volumes. Não use docker compose down -v a menos que queira eliminar todo dado local.

