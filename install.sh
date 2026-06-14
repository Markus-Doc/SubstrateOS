#!/usr/bin/env sh
# SubstrateOS installer for Linux and macOS (ADR-026).
#
# Installs the `labctl` + `subos` console scripts so `subos claude` works from
# any directory in a fresh shell. Idempotent: re-running upgrades in place.
#
# Usage (from a clone of the repo):
#   ./install.sh                     # install / upgrade
#   ./install.sh --full-auto-default # also opt in to the full-auto posture (user-scope)
#   ./install.sh --help
#
# Design: pipx-first (isolated, user-scope, on PATH via `pipx ensurepath`); falls
# back to a managed virtualenv + PATH shim when pipx is unavailable. Pins no model
# and adds no API billing — it just installs the launcher.
set -eu

FULL_AUTO_DEFAULT=0
for arg in "$@"; do
    case "$arg" in
        --full-auto-default) FULL_AUTO_DEFAULT=1 ;;
        -h|--help)
            sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "install.sh: unknown option '$arg' (try --help)" >&2
            exit 2
            ;;
    esac
done

info() { printf '\033[1;34m==>\033[0m %s\n' "$1"; }
warn() { printf '\033[1;33m[!]\033[0m %s\n' "$1" >&2; }
die() { printf '\033[1;31m[x]\033[0m %s\n' "$1" >&2; exit 1; }

# Resolve the repo root (this script lives at the repo root) and the package dir.
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
PKG_DIR="$SCRIPT_DIR/scripts"
[ -d "$PKG_DIR" ] || die "package directory not found at $PKG_DIR — run this from a SubstrateOS clone"

# 1. Python >= 3.11
PY=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then PY="$candidate"; break; fi
done
[ -n "$PY" ] || die "Python 3 not found. Install Python >= 3.11 (https://www.python.org/downloads/)."
if ! "$PY" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
    ver=$("$PY" -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])')
    die "Python >= 3.11 required, found $ver. Please upgrade Python."
fi
info "Python OK ($("$PY" -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])'))"

# 2. Install via pipx (preferred) or a managed venv fallback.
PIPX=""
if command -v pipx >/dev/null 2>&1; then
    PIPX="pipx"
elif "$PY" -m pipx --version >/dev/null 2>&1; then
    PIPX="$PY -m pipx"
fi

if [ -z "$PIPX" ]; then
    info "pipx not found — installing it (user scope)"
    if "$PY" -m pip install --user pipx >/dev/null 2>&1; then
        "$PY" -m pipx ensurepath >/dev/null 2>&1 || true
        PIPX="$PY -m pipx"
    else
        warn "could not install pipx; falling back to a managed virtualenv"
    fi
fi

if [ -n "$PIPX" ]; then
    info "Installing SubstrateOS with pipx (idempotent)"
    # shellcheck disable=SC2086
    $PIPX install --force "$PKG_DIR"
    # shellcheck disable=SC2086
    $PIPX ensurepath >/dev/null 2>&1 || true
    BIN_HINT="$HOME/.local/bin"
else
    VENV="$HOME/.local/share/substrateos/venv"
    info "Installing SubstrateOS into a managed virtualenv ($VENV)"
    "$PY" -m venv "$VENV"
    "$VENV/bin/python" -m pip install --upgrade pip >/dev/null 2>&1 || true
    "$VENV/bin/python" -m pip install "$PKG_DIR"
    mkdir -p "$HOME/.local/bin"
    for tool in subos labctl; do
        ln -sf "$VENV/bin/$tool" "$HOME/.local/bin/$tool"
    done
    BIN_HINT="$HOME/.local/bin"
fi

# 3. Optional opt-in to the full-auto posture (user-scope; never the public Base).
if [ "$FULL_AUTO_DEFAULT" -eq 1 ]; then
    OVERLAY_DIR="$HOME/.config/substrateos"
    OVERLAY_ENV="$OVERLAY_DIR/overlay.env"
    mkdir -p "$OVERLAY_DIR"
    if ! grep -qs '^export SUBSTRATEOS_FULL_AUTO=' "$OVERLAY_ENV" 2>/dev/null; then
        echo 'export SUBSTRATEOS_FULL_AUTO=1' >>"$OVERLAY_ENV"
    fi
    # The $HOME refs must stay literal so they expand when the shell rc is sourced.
    # shellcheck disable=SC2016
    SOURCE_LINE='[ -f "$HOME/.config/substrateos/overlay.env" ] && . "$HOME/.config/substrateos/overlay.env"'
    for rc in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.zshrc"; do
        [ -e "$rc" ] || continue
        if ! grep -qsF 'substrateos/overlay.env' "$rc"; then
            printf '\n# SubstrateOS full-auto opt-in (ADR-026)\n%s\n' "$SOURCE_LINE" >>"$rc"
        fi
    done
    warn "Full-auto posture enabled for new shells (SUBSTRATEOS_FULL_AUTO=1 in $OVERLAY_ENV)."
fi

# 4. Verify.
info "Verifying the installation"
if command -v subos >/dev/null 2>&1; then
    subos --version || true
    labctl doctor || true
    info "Done. Try:  subos claude --dry-run"
else
    warn "subos is installed but not on PATH yet."
    warn "Open a NEW terminal (so PATH picks up $BIN_HINT), or run:  export PATH=\"$BIN_HINT:\$PATH\""
fi
