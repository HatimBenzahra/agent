#!/usr/bin/env bash
# open_pdf.sh – Ouvre un fichier PDF pour vérifier visuellement la qualité de la conversion.
#
# Usage : ./open_pdf.sh <chemin_du_fichier.pdf>
#
# Si le fichier n’est pas fourni, le script affiche un message d’aide.

if [ -z "$1" ]; then
    echo "Usage : $0 <chemin_du_fichier.pdf>"
    exit 1
fi

FILE="$1"

# Vérifie que le fichier existe et est bien un PDF
if [ ! -f "$FILE" ]; then
    echo "❌ Le fichier \"$FILE\" n’existe pas."
    exit 1
fi

# Vous pouvez aussi utiliser pdfinfo pour afficher quelques métadonnées
# et ainsi avoir un premier aperçu sans ouvrir l’interface graphique.
echo "=== Métadonnées PDF (via pdfinfo) ==="
pdfinfo "$FILE" | head -n 20

# Ouvre le PDF dans l’application par défaut (Evince, Okular, etc.)
echo "=== Ouverture du PDF dans l’application par défaut ==="
xdg-open "$FILE"  # Sous Linux
# windows
# start "" "$FILE"
# macOS
# open "$FILE"
