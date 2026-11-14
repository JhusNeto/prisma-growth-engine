# W07 — Entrega e conciliação

**Gatilho:** evento OrderApproved na outbox.

1. Confirmar que o pedido está approved e que a oferta existe.
2. Quando a Hotmart fizer entrega nativa, registrar confirmação e instruções; não duplicar acesso.
3. Para entrega própria futura, chamar o adaptador uma única vez com chave idempotente order_id.
4. Registrar sucesso/falha da entrega e atualizar métricas.
5. Uma vez ao dia, buscar/consultar relatório do checkout e reconciliar pedidos, reembolsos e chargebacks.
6. Itens divergentes entram em fila de revisão humana.

**Reembolso/chargeback:** retirar apenas direitos que dependam da plataforma própria, preservando evidências e trilha de auditoria.

