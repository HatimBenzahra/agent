FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# L'agent peut être root dans son container isolé (sécurisé)
# USER root  # Par défaut, c'est déjà root

# Point d'entrée par défaut
ENTRYPOINT ["python", "run.py"]