# ADR-001 — Monólito modular como ponto de partida

- **Status:** Aceito
- **Contexto:** O MVP precisa validar uma venda ponta a ponta com baixa carga operacional.
- **Decisão:** Uma API FastAPI modular e um PostgreSQL. n8n integra e agenda, sem microsserviços ou fila dedicada inicialmente.
- **Consequências:** Deploy, testes e rastreabilidade mais simples. Extrações só acontecerão quando métricas de volume/isolamento justificarem.

