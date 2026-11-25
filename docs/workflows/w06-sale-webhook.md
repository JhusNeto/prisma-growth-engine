# W06 — Recebimento de venda

**Status:** VALIDATED LOCALLY (`POST /v1/webhooks/hotmart`); operação externa depende de uma API pública configurada

**Gatilho:** checkout envia webhook de alteração de compra (`PURCHASE_APPROVED`, `PURCHASE_COMPLETE`, `PURCHASE_WAITING_PAYMENT`, `PURCHASE_BILLET_PRINTED`, `PURCHASE_REFUNDED`, `PURCHASE_CHARGEBACK`, `PURCHASE_PROTEST`, `PURCHASE_CANCELED`, `PURCHASE_EXPIRED`).

1. Validar assinatura/token (`X-Hotmart-Hottok`) em tempo constante contra `HOTMART_HOTTOK`.
2. Validar schema e rejeitar payloads incompletos ou eventos não suportados (`422`).
3. Sanitizar payload removendo PII do comprador antes da persistência.
4. Inserir `provider_events` usando `provider + event_id` com `ON CONFLICT DO NOTHING`.
5. Se o evento já existir, responder `200 OK` (`{"status": "duplicate"}`) sem efeitos adicionais.
6. Na mesma transação, criar ou atualizar `orders` usando `provider + provider_transaction_id` respeitando precedência de estado, marcar `processed_at` e inserir evento (`order.<status>`) em `outbox_events`.
7. Responder `200 OK` imediatamente após o commit transacional; nunca aguardar e-mail, IA ou entrega.

**Observabilidade:** correlação por `event_id`, `provider_transaction_id` e `order_id`. Payloads sensíveis ficam fora do banco e dos logs.
