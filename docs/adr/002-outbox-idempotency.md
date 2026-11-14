# ADR-002 — Outbox transacional e idempotência

- **Status:** Aceito
- **Contexto:** Webhooks podem repetir e workflows podem falhar no meio.
- **Decisão:** Persistir evento externo e alteração de negócio antes de disparar trabalho assíncrono; usar chaves únicas por provedor/evento e provedor/transação.
- **Consequências:** Não há entrega duplicada; é necessário monitorar eventos pendentes e manter rotina de reprocessamento.

