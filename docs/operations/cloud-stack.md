# Stack cloud da Prisma Dados

## Decisões

- **Cloudflare Pages:** storefront Astro, já publicado.
- **Heroku:** API FastAPI e PostgreSQL, condicionado ao crédito estudantil.
- **Doppler:** secrets separados em `dev`, `stg` e `prd`.
- **GitHub Actions:** testes, migrations e validações de build.
- **Sentry:** erros da API e webhooks, ativado somente com `SENTRY_DSN`.
- **Cloudflare R2:** arquivos comerciais, assets originais e backups externos,
  sempre em buckets privados.
- **n8n:** hospedagem separada com persistência própria; não usar Heroku para
  n8n por causa do filesystem efêmero.

## Secrets por ambiente

### API

- `DATABASE_URL`
- `ADMIN_API_KEY`
- `HOTMART_HOTTOK`
- `CORS_ORIGINS`
- `SENTRY_DSN`
- `SENTRY_ENVIRONMENT=prd`

### Storefront

- `PUBLIC_API_URL`

### n8n

- `N8N_ENCRYPTION_KEY`
- `N8N_API_KEY`
- `DATABASE_URL` exclusivo do n8n, se auto-hospedado

O n8n deve chamar a API com uma credencial limitada e nunca acessar as tabelas
comerciais diretamente.

## Ordem de ativação

1. Resgatar Doppler e criar os três ambientes.
2. Criar Sentry e registrar o DSN apenas em `prd`.
3. Preparar o app Heroku e o PostgreSQL para dezembro, sem migrar produção
   antes do cutover documentado.
4. Criar buckets privados no R2.
5. Configurar GitHub Actions com deploy protegido por aprovação.
6. Escolher hospedagem persistente para n8n e separar seu banco.
7. Configurar `PUBLIC_API_URL` no build do Pages depois que a API estiver
   disponível em HTTPS.

Nenhum crédito estudantil deve ser tratado como disponibilidade garantida antes
da aprovação do benefício e da confirmação dos termos comerciais.
