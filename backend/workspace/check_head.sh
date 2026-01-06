#!/usr/bin/env bash
# Script : check_head.sh
# Affiche les premières lignes d’un fichier téléchargé pour vérification

if [[ -z "$1" ]]; then
    echo "Usage : $0 <chemin_du_fichier>"
    exit 1
fi

FICHIER="$1"

if [[ ! -f "$FICHIER" ]]; then
    echo "❌ Fichier introuvable : $FICHIER"
    exit 1
fi

echo "📄 20 premières lignes de \"$FICHIER\" :"
head -n 20 "$FICHIER"

