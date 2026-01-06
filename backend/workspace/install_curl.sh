#!/usr/bin/env bash
# install_curl.sh – Install curl non‑interactively

# Update package lists
apt-get update -qq

# Install curl without prompting the user
apt-get install -y -qq --no-install-recommends curl

# Verify installation
if command -v curl >/dev/null 2>&1; then
    echo "✔ curl has been installed successfully."
else
    echo "✘ Failed to install curl." >&2
    exit 1
fi
