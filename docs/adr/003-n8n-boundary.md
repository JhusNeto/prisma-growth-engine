# ADR-003 — n8n é orquestrador, não fonte de verdade

- **Status:** Aceito
- **Contexto:** Workflows visuais são ótimos para integração, mas não substituem transações e regras de negócio auditáveis.
- **Decisão:** n8n recebe IDs e chama APIs; PostgreSQL/FastAPI mantêm dados, regras e estados.
- **Consequências:** Workflows podem ser recriados sem perda de dados. Integrações precisam de endpoints explícitos.

