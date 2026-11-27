#!/usr/bin/env bash
# NoCap installer — macOS / Linux / WSL / Git Bash
#
#   curl -fsSL https://raw.githubusercontent.com/sanket-manohar/nocap/main/install.sh | bash   # nocap-ignore IAC003
#   curl -fsSL .../install.sh | bash -s -- --ci   # adds the CI workflow  nocap-ignore IAC003
#   ./install.sh /path/to/project --tools cursor,claude     # from a local clone, only some tools
#
# Options:
#   [dir]            project directory (default: current directory)
#   --tools LIST     comma list: generic,claude,cursor,copilot,windsurf,cline,roo,continue,gemini,junie,aider (default: all)
#   --ci             add .github/workflows/nocap.yml
#   --uninstall      remove NoCap files and blocks
#   -y, --yes        no prompts
set -euo pipefail

REPO="${NOCAP_REPO:-sanket-manohar/nocap}"
REF="${NOCAP_REF:-main}"
TARGET="."; TOOLS="all"; CI=0; UNINSTALL=0
START="<!-- nocap:start -->"; END="<!-- nocap:end -->"

while [ $# -gt 0 ]; do
  case "$1" in
    --tools) TOOLS="$2"; shift 2 ;;
    --ci) CI=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -y|--yes) shift ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *) TARGET="$1"; shift ;;
  esac
done

c() { if [ -t 1 ]; then printf "\033[%sm%s\033[0m" "$1" "$2"; else printf "%s" "$2"; fi; }
say() { printf "  %s %s\n" "$(c '1;35' '▸')" "$1"; }
TARGET="$(cd "$TARGET" && pwd)"

# ---- locate source (local clone or download) ----
SRC=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/adapters/MANIFEST" ]; then
  SRC="$SCRIPT_DIR"
else
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  say "Downloading NoCap ($REPO@$REF)…"
  if command -v git >/dev/null 2>&1; then
    git clone --quiet --depth 1 --branch "$REF" "https://github.com/$REPO.git" "$TMP/vp"
  else
    curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/heads/$REF" | tar -xz -C "$TMP"
    mv "$TMP"/nocap-* "$TMP/vp"
  fi
  SRC="$TMP/vp"
fi

tool_of() {  # map destination path -> tool name
  case "$1" in
    AGENTS.md) echo generic ;; CLAUDE.md|.claude/*) echo claude ;; .cursor/*) echo cursor ;;
    .github/copilot-instructions.md|.github/prompts/*) echo copilot ;; .windsurf/*) echo windsurf ;;
    .clinerules/*) echo cline ;; .roo/*) echo roo ;; .continue/*) echo continue ;; GEMINI.md) echo gemini ;;
    .junie/*) echo junie ;; .aider.conf.yml) echo aider ;; *) echo other ;;
  esac
}
wanted() { [ "$TOOLS" = "all" ] || [[ ",$TOOLS," == *",$1,"* ]]; }

strip_block() {  # remove existing nocap block from file
  awk -v s="$START" -v e="$END" '$0==s{skip=1;next} $0==e{skip=0;next} !skip' "$1" > "$1.vptmp" && mv "$1.vptmp" "$1"
}

if [ "$UNINSTALL" = 1 ]; then
  say "Uninstalling from $TARGET"
  rm -rf "$TARGET/.nocap"
  while read -r mode src dest; do
    [ -z "${mode:-}" ] || [ "${mode#\#}" != "$mode" ] && continue
    f="$TARGET/$dest"; [ -f "$f" ] || continue
    case "$mode" in
      merge) strip_block "$f"; [ -n "$(tr -d '[:space:]' < "$f")" ] || rm -f "$f" ;;
      copy-if-missing) grep -q "NoCap" "$f" && rm -f "$f" ;;
      *) rm -f "$f" ;;
    esac
    d="$(dirname "$dest")"
    while [ "$d" != "." ] && rmdir "$TARGET/$d" 2>/dev/null; do d="$(dirname "$d")"; done
  done < "$SRC/adapters/MANIFEST"
  rm -f "$TARGET/.github/workflows/nocap.yml"
  rmdir "$TARGET/.github/workflows" "$TARGET/.github" 2>/dev/null || true
  say "Done."; exit 0
fi

printf "\n  %s  installing into %s\n\n" "$(c '1;35' 'NoCap')" "$TARGET"

# ---- 1. toolkit ----
VP="$TARGET/.nocap"
rm -rf "$VP"; mkdir -p "$VP/scanner"
cp -R "$SRC/prompts" "$SRC/templates" "$SRC/checklists" "$VP/"
cp "$SRC/AGENTS.md" "$SRC/MASTER_PROMPT.md" "$SRC/TERMS.md" "$SRC/LICENSE" "$VP/"
cp "$SRC/scanner/nocap.py" "$VP/scanner/"
touch "$VP/.nocap-toolkit"
cat > "$VP/vp" <<'EOF'
#!/usr/bin/env sh
# NoCap scanner shortcut:  .nocap/vp [path] [options]
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="$(command -v python3 || command -v python)"
[ -z "$PY" ] && { echo "NoCap needs Python 3.8+ (https://python.org) — or ask your AI: 'nocap score'"; exit 2; }
exec "$PY" "$DIR/scanner/nocap.py" "${@:-.}"
EOF
chmod +x "$VP/vp"
printf '@echo off\r\nwhere py >nul 2>nul && (py -3 "%%~dp0scanner\\nocap.py" %%*) || (python "%%~dp0scanner\\nocap.py" %%*)\r\n' > "$VP/vp.cmd"
say "Toolkit      → .nocap/"

# ---- 2. adapters ----
while read -r mode src dest; do
  [ -z "${mode:-}" ] && continue; [ "${mode#\#}" != "$mode" ] && continue
  t="$(tool_of "$dest")"; wanted "$t" || continue
  f="$TARGET/$dest"; mkdir -p "$(dirname "$f")"
  case "$mode" in
    copy) cp "$SRC/$src" "$f" ;;
    copy-if-missing) [ -e "$f" ] || cp "$SRC/$src" "$f" ;;
    merge)
      [ -f "$f" ] && strip_block "$f"
      { [ -s "$f" ] && printf "\n"; echo "$START"; cat "$SRC/$src"; echo "$END"; } >> "$f" ;;
  esac
  printf "  %s %-12s → %s\n" "$(c '32' '✓')" "$t" "$dest"
done < "$SRC/adapters/MANIFEST"

# ---- 3. CI (optional) ----
if [ "$CI" = 1 ]; then
  mkdir -p "$TARGET/.github/workflows"
  sed "s#sanket-manohar/nocap#$REPO#g" "$SRC/adapters/ci/nocap.yml" > "$TARGET/.github/workflows/nocap.yml"
  say "CI workflow  → .github/workflows/nocap.yml"
fi

# ---- 4. gitignore ----
GI="$TARGET/.gitignore"
grep -qs "nocap-results.json" "$GI" || printf "\n# NoCap\n.nocap-results.json\n" >> "$GI"

cat <<EOF

  $(c '1;32' '✔ NoCap installed!')

  $(c '1' 'Next — pick one:')
   1. Open your AI assistant (Cursor, Claude Code, Copilot, Windsurf…) and type:
        $(c '1;36' 'nocap docs')     → full documentation
        $(c '1;36' 'nocap audit')    → security audit with fixes
        $(c '1;36' 'nocap ship')     → am I ready to launch?
   2. Run the scanner:  $(c '1;36' '.nocap/vp')   (Windows: .nocap\\vp)

  ⚠  NoCap is a development aid. Final checks are your responsibility. See .nocap/TERMS.md

EOF
