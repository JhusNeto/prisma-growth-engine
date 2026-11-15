# W07 — Entrega, despacho da outbox e conciliação

**Status:** DISPATCHER VALIDATED LOCALLY (`GET /v1/outbox/pending`, `POST /v1/outbox/{event_id}/ack`)

**Gatilho:** n8n consulta eventos pendentes (`published_at IS NULL`) via API administrativa (`X-Admin-Key`), respeitando o ADR-003 (sem acesso direto ao PostgreSQL).

1. Consultar `GET /v1/outbox/pending` (com filtro opcional `event_type=order.approved`).
2. Quando a Hotmart fizer entrega nativa, registrar confirmação operacional e notificar o administrador se necessário; não duplicar acesso.
3. Para entrega própria futura, chamar o adaptador uma única vez usando `order_id` como chave idempotente.
4. Confirmar o consumo chamando `POST /v1/outbox/{event_id}/ack` (operação idempotente que grava `published_at`).
5. Uma vez ao dia, conciliar relatórios do checkout contra `orders` para identificar divergências de reembolso ou chargeback.

**Reembolso/chargeback:** retirar apenas direitos que dependam da plataforma própria, preservando evidências e trilha de auditoria.
