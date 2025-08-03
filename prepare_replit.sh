#!/bin/bash

# Script de préparation pour le déploiement Replit
echo "🚀 Préparation des fichiers pour Replit..."

# Créer un répertoire de déploiement
mkdir -p replit_deploy

# Copier tous les fichiers nécessaires
echo "📁 Copie des fichiers..."
cp app.py replit_deploy/
cp config.py replit_deploy/
cp requirements.txt replit_deploy/
cp .replit replit_deploy/
cp replit.nix replit_deploy/
cp README.md replit_deploy/

# Copier les dossiers
cp -r models/ replit_deploy/
cp -r templates/ replit_deploy/
cp -r data/ replit_deploy/

echo "✅ Fichiers prêts dans le dossier replit_deploy/"

# Afficher la structure
echo "📋 Structure du projet :"
cd replit_deploy
find . -type f | head -20

echo ""
echo "🎯 Instructions pour Replit :"
echo "1. Créer un nouveau Repl Python sur replit.com"
echo "2. Uploader tous les fichiers du dossier replit_deploy/"
echo "3. Replit détectera automatiquement le fichier .replit"
echo "4. Cliquer sur Run pour démarrer l'application"
