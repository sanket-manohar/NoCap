#!/usr/bin/env bash
# One-time publish helper for the NoCap maintainer.
#   ./tools/publish.sh <github-username> <email>
# Fills in placeholders, creates the git repo with the right author, tags v1.0.0 + v1,
# and pushes to GitHub (uses the GitHub CLI `gh` if installed, otherwise prints the commands).
set -euo pipefail
cd "$(dirname "$0")/.."
USER_NAME="${1:-}"; EMAIL="${2:-}"
[ -n "$USER_NAME" ] || read -rp "GitHub username: " USER_NAME
[ -n "$EMAIL" ] || read -rp "Email (for git commits & security contact): " EMAIL
AUTHOR="Sanket Santosh Vidya Manohar"
SLUG="$USER_NAME/nocap"
VERSION="v$(sed -n 's/^VERSION = "\(.*\)"/\1/p' scanner/nocap.py)"

echo "▸ Filling placeholders → $SLUG / $EMAIL"
grep -rlI --exclude-dir=.git -e "YOUR_GITHUB_USERNAME" -e "YOUR_EMAIL" . | grep -v "tools/publish" | while read -r f; do
  sed -i.bak -e "s#YOUR_GITHUB_USERNAME#$USER_NAME#g" -e "s#YOUR_EMAIL#$EMAIL#g" "$f" && rm -f "$f.bak"
done

echo "▸ Creating git repository"
[ -d .git ] || git init -q -b main
git config user.name "$AUTHOR"
git config user.email "$EMAIL"
git add -A
git commit -q -m "feat: NoCap $VERSION — docs, security & compliance for AI-built apps" || true
git tag -a "$VERSION" -m "NoCap $VERSION" 2>/dev/null || true
git tag -f v1 >/dev/null

manual() {
  cat <<MSG

✔ Repo ready. Create an EMPTY public repo named 'nocap' at https://github.com/new, then run:

   git remote add origin https://github.com/$SLUG.git
   git push -u origin main
   git push origin --tags

The Release workflow will publish $VERSION automatically when the tags are pushed.
MSG
}

if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo "▸ Creating GitHub repo $SLUG and pushing"
  if gh repo create "$SLUG" --public --source . --remote origin \
       --description "Your AI wrote the code. NoCap documents it, audits its security & checks compliance. Any AI, any IDE, any stack." --push \
     && git push origin --tags; then
    gh repo edit "$SLUG" --add-topic vibe-coding,security,documentation,owasp,ai,cursor,claude-code,copilot,compliance,devsecops || true
    echo "✔ Live: https://github.com/$SLUG  (the Release workflow publishes $VERSION automatically)"
  else
    echo "⚠ GitHub CLI could not create/push the repo — do it manually:"; manual
  fi
else
  manual
fi
