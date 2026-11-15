# Especificação do MVP

## Marco de sucesso

Um produto de teste é cadastrado, tem uma landing page publicada, recebe evento de navegação, uma venda aprovada é recebida por webhook, e o pedido/entrega aparecem no painel analítico.

## Escopo

| Inclui | Não inclui nesta fase |
|---|---|
| Catálogo de produto e oferta | Múltiplos checkouts reais |
| Uma landing Astro | Painel administrativo completo |
| Receiver de webhook idempotente | Publicação irrestrita em redes |
| Outbox e workflow n8n | IA autônoma que decide preço/campanha |
| Eventos básicos e dados para BI | Atribuição perfeita multi-dispositivo |

## Contratos iniciais

- GET /health retorna disponibilidade do processo.
- GET /v1/products será expandido para CRUD autenticado.
- POST /v1/webhooks/hotmart será criado após validar o contrato de webhook e o mecanismo de autenticação no ambiente de teste.
- Eventos de navegação devem carregar product_id, campaign_code, tipo, data e consentimento quando aplicável.

## Critérios de aceite

1. Reenviar o mesmo evento de venda não cria um segundo pedido.
2. Falha depois de persistir o evento não perde o evento.
3. Produto pausado impede novas campanhas, não apaga pedidos nem entregas devidas.
4. Cada ação automatizada deixa rastro de auditoria.


## Implementação concluída (Backend & Vitrine)

- `GET /health`: disponibilidade da API.
- `POST/GET /v1/products`, `POST/GET/PATCH /v1/offers`, `POST /v1/products/{id}/transitions`, `PUT/GET/POST /v1/products/{id}/page`: gestão completa do catálogo com travas comerciais e aprovação humana.
- `POST /v1/webhooks/hotmart`: receiver autenticado (`X-Hotmart-Hottok`) e idempotente para vendas e reembolsos.
- `GET /v1/outbox/pending` e `POST /v1/outbox/{id}/ack`: dispatcher transacional para consumo assíncrono via n8n.
- `GET /v1/orders` e `GET /v1/analytics/overview`: consulta administrativa de pedidos e métricas financeiras consolidadas.
