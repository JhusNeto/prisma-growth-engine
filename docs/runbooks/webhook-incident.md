# Runbook — incidente de webhook

## Sintomas

Venda aparece no checkout, mas não no banco/painel; ou há entregas duplicadas.

## Resposta

1. Pause somente o workflow de entrega, não o receiver de webhook.
2. Localize o evento por provider, event_id ou transaction_id.
3. Verifique assinatura, status HTTP, registro em provider_events e pedido correspondente.
4. Se o evento existe mas não foi processado, reprocesse o evento persistido. Não reenvie um payload manual alterado.
5. Se houve duplicidade, confirme se a restrição única foi violada ou se o adaptador de entrega ignorou a chave idempotente.
6. Registre causa, impacto, correção e prevenção em um ADR ou incidente.

## Nunca fazer

- Apagar eventos para “limpar” o painel.
- Conceder produto manualmente antes de confirmar o pedido.
- Expor payloads de compradores em chat, logs ou issues.

