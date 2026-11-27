#!/usr/bin/env bash
# Replace the sanket-manohar placeholder everywhere after you fork/create the repo.
#   ./tools/set-repo.sh yourname            → yourname/nocap
#   ./tools/set-repo.sh yourname/my-repo
set -euo pipefail
[ $# -eq 1 ] || { echo "usage: $0 <github-user>[/<repo>]"; exit 1; }
SLUG="$1"; [[ "$SLUG" == */* ]] || SLUG="$SLUG/nocap"
grep -rl --exclude-dir=.git "sanket-manohar/nocap" . | while read -r f; do
  sed -i.bak "s#sanket-manohar/nocap#$SLUG#g" "$f" && rm -f "$f.bak"
done
echo "✔ Repo set to $SLUG"
