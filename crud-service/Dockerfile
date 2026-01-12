FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o serviço
COPY . .

# Garante imports corretos
ENV PYTHONPATH=/app

# Sobe a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
