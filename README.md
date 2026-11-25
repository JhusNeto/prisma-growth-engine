# Prisma Growth Engine

Base local para validar o ciclo: produto cadastrado -> página pública -> evento rastreado -> venda confirmada -> entrega registrada.

Este repositório começa como um monólito modular: FastAPI é a fonte de verdade; PostgreSQL guarda o estado; n8n só orquestra ações; Astro publica o site. Tudo roda localmente no Mac, sem serviços pagos.

## Começo rápido no macOS (Apple Silicon)

> Execute somente depois de abrir esta pasta como projeto no PyCharm. Os comandos não exigem conta em nenhum serviço externo.

\`\`\`zsh
# 1. Pré-requisitos (uma única vez)
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12 node@22 git

# Instale e abra o Docker Desktop para Apple silicon uma vez:
# https://www.docker.com/products/docker-desktop/

# 2. Entre na pasta e crie a configuração local
cd /CAMINHO/PARA/prisma-growth-engine
cp .env.example .env

# 3. Backend Python (interpretador do PyCharm: .venv/bin/python)
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e "apps/api[dev]"

# 4. Frontend
cd apps/web && npm install && cd ../..

# 5. Infraestrutura local
docker compose up -d postgres n8n

# 6. Em dois terminais separados
source .venv/bin/activate && uvicorn app.main:app --app-dir apps/api --reload --port 8000
cd apps/web && npm run dev
\`\`\`

Confira: API em \`http://localhost:8000/docs\`, site em \`http://localhost:4321\` e n8n em \`http://localhost:5678\`.

## Estrutura

\`\`\`text
apps/api/       FastAPI: catálogo, eventos e integrações
apps/web/       Astro: páginas públicas SEO-first
docs/           decisão, arquitetura, especificações, workflows e runbooks
infra/          inicialização local do PostgreSQL
docker-compose.yml  PostgreSQL + n8n para desenvolvimento
\`\`\`

## Limites do MVP

- Não armazene senhas, tokens ou dados reais em Git; use \`.env\`.
- Webhooks de venda precisam ser autenticados e idempotentes antes de qualquer entrega.
- Não publique conteúdos automaticamente sem revisão inicial nem faça prospecção não solicitada.
- A entrega inicial pode permanecer nativa na Hotmart; o sistema apenas registra e reconcilia.

## Documentação prioritária

- [Arquitetura N1/N2](docs/architecture/n1-n2.md)
- [Especificação do MVP](docs/specs/mvp.md)
- [ADRs](docs/adr/)
- [Workflows](docs/workflows/)
- [Runbooks locais e operacionais](docs/runbooks/)
- [Migração para a nuvem](docs/runbooks/cloud-migration.md)

## Comandos úteis

\`\`\`zsh
docker compose logs -f postgres n8n
docker compose down                 # para os containers, preserva dados
docker compose down -v              # APAGA os dados locais: use apenas para reiniciar do zero
curl http://localhost:8000/health
\`\`\`
