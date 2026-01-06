#!/usr/bin/env bash
# Vérifie si curl est installé et affiche sa version

# Vérifier si curl est présent dans le PATH
if ! command -v curl >/dev/null 2>&1; then
  echo "Erreur : curl n'est pas installé ou pas dans le PATH."
  exit 1
fi

# Récupérer la version de curl
CURL_VERSION=$(curl --version | head -n1)

echo "curl est correctement installé."
echo "Version : ${CURL_VERSION}"
