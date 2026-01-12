FROM python:3.11-slim

# Define o diretório de trabalho como /app
WORKDIR /app

# Instala dependências de sistema para o PostgreSQL/SQLAlchemy
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements.txt que está na mesma pasta do Dockerfile
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo de agent-service para dentro de /app
COPY . .

# Garante que o Python consiga importar de /app/app
ENV PYTHONPATH=/app

# O comando aponta para app.main porque o main.py está em /app/app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]