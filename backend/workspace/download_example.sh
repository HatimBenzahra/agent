   #!/usr/bin/env bash
   # download_example.sh – récupère la page d’un site Web et la sauvegarde dans output.html
   # Usage : ./download_example.sh

   URL="https://www.example.com"
   OUTPUT="output.html"

   # Utilise curl pour télécharger la page en suivant les redirections HTTP (option -L)
   # Le résultat est redirigé vers le fichier local OUTPUT
   curl -L "$URL" -o "$OUTPUT"

   echo "Téléchargement terminé : $OUTPUT"
   EOF