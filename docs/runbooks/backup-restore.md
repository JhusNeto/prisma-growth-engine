# Runbook — backup e restauração local

## Backup

Com o Postgres local em execução:

~~~zsh
mkdir -p data/backups
docker compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "data/backups/prisma-growth-$(date +%F).sql"
~~~

Guarde o arquivo criptografado fora do computador antes de tratar qualquer base com dados reais.

## Restauração em base de teste

1. Pare os processos que usam o banco.
2. Crie uma base vazia de teste.
3. Restaure primeiro em ambiente isolado.
4. Valide quantidade de produtos, pedidos e eventos antes de substituir qualquer base.

A restauração de produção nunca deve ser o primeiro teste de um backup.

