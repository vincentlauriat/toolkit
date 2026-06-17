#!/usr/bin/env bash
# setup.sh — initialise la structure du repo vincentlauriat/toolkit
set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "→ Création de la structure toolkit dans : $REPO_ROOT"

# Répertoire du catalogue marketplace
mkdir -p "$REPO_ROOT/.claude-plugin"

# Supprime le dossier plugins/ s'il existe (plugins hébergés en externe)
if [ -d "$REPO_ROOT/plugins" ]; then
  echo "  ⚠ Suppression de plugins/ (les plugins sont désormais référencés en externe)"
  rm -rf "$REPO_ROOT/plugins"
fi

echo "  ✓ .claude-plugin/"
echo "  ✓ marketplace.json en place"
echo ""
echo "Structure finale :"
find "$REPO_ROOT" -not -path '*/.git/*' | sort | sed "s|$REPO_ROOT/||"
echo ""
echo "✓ Toolkit prêt. Pour initialiser le repo git :"
echo ""
echo "  cd $REPO_ROOT"
echo "  git init"
echo "  git add ."
echo "  git commit -m 'feat: initial marketplace — audit-report (external source)'"
echo "  git remote add origin git@github.com:vincentlauriat/toolkit.git"
echo "  git push -u origin main"
