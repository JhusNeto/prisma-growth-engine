# W06 — Recebimento de venda

**Gatilho:** checkout envia webhook de alteração de compra.

1. Validar assinatura/token conforme a documentação vigente do checkout.
2. Validar schema e rejeitar payloads incompletos.
3. Inserir provider_event usando provider + event_id como chave única.
4. Na mesma transação, criar/atualizar o pedido usando provider + transaction_id e criar evento na outbox.
5. Responder 2xx após a persistência; nunca aguardar e-mail, IA ou entrega.
6. Se o evento já existir, responder 2xx sem efeitos adicionais.

**Observabilidade:** correlação por event_id, transaction_id e order_id. Payloads sensíveis ficam fora dos logs.

