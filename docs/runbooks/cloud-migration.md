# Runbook — migração para a nuvem

Este runbook remove a dependência operacional do Mac sem assumir um provedor
específico. O storefront já está no Cloudflare Pages; a API e o PostgreSQL
precisam ser publicados antes de ativar tracking e webhooks externos.

## Componentes

- **API:** imagem `Dockerfile`, exposta na porta `8000`.
- **PostgreSQL:** serviço gerenciado com acesso HTTPS/TLS e backups.
- **Storefront:** Cloudflare Pages.
- **n8n:** serviço gerenciado ou container com volume persistente.
- **Secrets:** mecanismo de secrets do provedor, nunca Git ou imagem Docker.

## Pré-requisitos

Defina, fora do repositório:

- `DATABASE_URL` do PostgreSQL cloud.
- `ADMIN_API_KEY` nova e forte.
- `HOTMART_HOTTOK`.
- `CORS_ORIGINS=https://prismadados.pages.dev`.
- `PUBLIC_API_URL=https://api.<dominio>`.

Não reutilize senha demonstrativa do `.env.example`.

## Preparar o banco cloud

1. Criar uma instância PostgreSQL vazia.
2. Confirmar que o provedor exige TLS.
3. Executar as migrations:

```zsh
DATABASE_URL='postgresql+psycopg://...' \
  .venv/bin/alembic upgrade head
```

4. Validar `GET /health` depois de subir a API.

Para migrar dados locais existentes, faça primeiro um backup e restaure em uma
base temporária. Só depois de comparar produtos, ofertas, pedidos, eventos e
outbox substitua a base de destino:

```zsh
docker compose exec -T postgres \
  pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" \
  > data/backups/prisma-growth-cloud-cutover.sql

psql "$CLOUD_DATABASE_URL" < data/backups/prisma-growth-cloud-cutover.sql
```

O arquivo de backup deve permanecer fora do Git e ser criptografado quando
contiver dados reais.

## Publicar a API

O serviço deve:

1. Construir a imagem a partir do `Dockerfile`.
2. Injetar os secrets no runtime.
3. Executar `alembic upgrade head` como etapa de release, antes de receber
   tráfego.
4. Iniciar o container na porta `8000`.
5. Expor HTTPS.
6. Configurar healthcheck em `/health`.
7. Restringir acesso administrativo e logs sem payloads de compradores.

Não execute migration automaticamente a cada reinício do container.

## Ativar o storefront

Depois de confirmar a API:

```zsh
PUBLIC_API_URL=https://api.<dominio> npm run build
npm run deploy
```

O build deve usar o mesmo catálogo validado contra o PostgreSQL cloud. Só então
o frontend enviará `page_view` e `checkout_click` para a API.

## Cutover

1. Fazer backup local.
2. Criar e migrar o PostgreSQL cloud.
3. Comparar contagens e registros essenciais.
4. Publicar a API e confirmar `/health`.
5. Configurar webhook da Hotmart para a URL pública.
6. Configurar n8n para chamar somente a API.
7. Fazer build do Astro com `PUBLIC_API_URL`.
8. Revalidar a página pública e o endpoint de tracking.
9. Manter o Mac desligado da operação por um período de observação.

O Mac deixa de ser runtime quando API, PostgreSQL, n8n, secrets, backups e
deploy estiverem ativos na nuvem.
