FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/prisma-growth-engine/apps/api

WORKDIR /opt/prisma-growth-engine

COPY apps/api /opt/prisma-growth-engine/apps/api
COPY alembic.ini /opt/prisma-growth-engine/alembic.ini
RUN pip install --no-cache-dir /opt/prisma-growth-engine/apps/api

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--app-dir", "apps/api", "--host", "0.0.0.0", "--port", "8000"]
