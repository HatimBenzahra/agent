#!/usr/bin/env bash
# Vérifie la présence et l’intégrité d’un PDF, puis affiche un aperçu

PDF_FILE="${1:-output.pdf}"

if [ ! -f "$PDF_FILE" ]; then
    echo "❌ Erreur : le fichier \"$PDF_FILE\" n'existe pas."
    exit 1
fi

if [ ! -s "$PDF_FILE" ]; then
    echo "❌ Erreur : le fichier \"$PDF_FILE\" est vide."
    exit 1
fi

echo "✅ Le fichier \"$PDF_FILE\" a bien été généré."
echo "📄 Infos du PDF :"
pdfinfo "$PDF_FILE" | head -n 10

echo "🔍 Affichage de l’aperçu…"
xdg-open "$PDF_FILE" 2>/dev/null || \
open "$PDF_FILE"      2>/dev/null || \
evince "$PDF_FILE"   2>/dev/null
