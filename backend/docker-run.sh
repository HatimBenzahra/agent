#!/bin/bash

# Construction de l'image Docker
echo "🐳 Construction de l'image Docker..."
docker build -t agent-orchestrator .

# Vérifie si des arguments sont fournis
if [ $# -eq 0 ]; then
    echo "❌ Erreur: Aucune tâche spécifiée"
    echo "Usage: ./docker-run.sh \"votre tâche ici\""
    exit 1
fi

# Lancement du container avec workspace
echo "🚀 Lancement du container..."
docker run --rm \
  --name agent-container \
  -v $(pwd)/workspace:/workspace \
  agent-orchestrator "$@"