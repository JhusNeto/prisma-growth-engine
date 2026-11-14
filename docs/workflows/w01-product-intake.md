# W01 — Cadastro e preparação de produto

**Gatilho:** administrador cria produto em estado draft.

1. Validar slug, público, tipo de produto, preço e URL de checkout.
2. Gravar produto e oferta na mesma transação.
3. Criar evento ProductPreparedRequested na outbox.
4. n8n consome somente o ID do produto e gera um pacote de lançamento: briefing, hipóteses de palavras-chave, copy e tarefas.
5. O administrador revisa. A automação não publica enquanto o produto não estiver approved.
6. Aprovado: publicar a landing e mudar para live.

**Falha:** registrar tentativa e erro; não mudar estado para live. Nunca recriar produto para repetir o workflow.

