# Métricas do storefront

## Objetivo

Registrar o mínimo necessário para medir o início do funil comercial sem
depender de serviço pago ou armazenar dados pessoais.

## Eventos

O endpoint público `POST /v1/events` aceita somente:

- `page_view`
- `checkout_click`

Cada evento possui `event_id` único, `product_slug`, timestamp e indicação de
consentimento. Reenvios do mesmo `event_id` são aceitos como duplicados sem
criar novo registro.

## Segurança e privacidade

- Não são armazenados IP, user-agent, cookies ou identificadores do visitante.
- O endpoint não exige chave administrativa, pois é chamado pelo storefront.
- A tabela possui chave única para idempotência.
- CORS é configurado por `CORS_ORIGINS`.
- A página só ativa o envio quando `PUBLIC_API_URL` existe no build.
- O catálogo de preview nunca envia eventos.

## Consulta

`GET /v1/analytics/overview` continua administrativo e expõe:

- `page_views`
- `checkout_clicks`

## Ativação

## Estado atual

O endpoint e a migration estão implementados e validados localmente. A coleta
no site público permanece desativada porque a API atualmente só está disponível
em `localhost:8000`; não existe ainda um deploy HTTPS do backend.

Para ativar a medição pública é necessário:

1. Publicar a API em uma URL HTTPS.
2. Definir `PUBLIC_API_URL` no ambiente de build do Astro.
3. Configurar `CORS_ORIGINS` com a origem do storefront.
4. Executar novo deploy do frontend.

O backend e a migration podem ser usados localmente antes da ativação
externa.
