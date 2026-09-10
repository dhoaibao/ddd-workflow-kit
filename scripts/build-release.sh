#!/usr/bin/env bash
# Build the skills-only GitHub release bundle.
set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
OUT_DIR=${1:-"$ROOT/dist"}
VERSION_FILE="$ROOT/VERSION"
[ -f "$VERSION_FILE" ] || { printf 'build-release: missing VERSION\n' >&2; exit 1; }
VERSION=$(awk 'NF {print $1; exit}' "$VERSION_FILE")
[ -n "$VERSION" ] || { printf 'build-release: VERSION is empty\n' >&2; exit 1; }
[ -f "$ROOT/install.sh" ] || { printf 'build-release: missing install.sh\n' >&2; exit 1; }
[ -f "$ROOT/PACKAGES" ] || { printf 'build-release: missing PACKAGES\n' >&2; exit 1; }
[ -d "$ROOT/skills" ] || { printf 'build-release: missing skills directory\n' >&2; exit 1; }
bad_member=$(find "$ROOT/skills" -type l -print -quit)
[ -z "$bad_member" ] || { printf 'build-release: skills tree contains a symlink: %s\n' "$bad_member" >&2; exit 1; }

mkdir -p "$OUT_DIR"
archive="$OUT_DIR/ddd-workflow-kit.tar.gz"
checksum="$OUT_DIR/ddd-workflow-kit.tar.gz.sha256"
tmp="$OUT_DIR/.ddd-workflow-kit-build.$$"
rm -rf "$tmp"
mkdir "$tmp"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

# Copy only the release contract; no docs, .git metadata, evaluations, or scripts.
cp "$ROOT/install.sh" "$tmp/install.sh"
cp "$VERSION_FILE" "$tmp/VERSION"
cp "$ROOT/PACKAGES" "$tmp/PACKAGES"
cp -R "$ROOT/skills" "$tmp/skills"

tar -czf "$archive" -C "$tmp" install.sh VERSION PACKAGES skills
if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$archive" | awk '{print $1 "  ddd-workflow-kit.tar.gz"}' > "$checksum"
elif command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$archive" | awk '{print $1 "  ddd-workflow-kit.tar.gz"}' > "$checksum"
else
  printf 'build-release: sha256sum or shasum is required\n' >&2
  exit 1
fi
printf 'Built %s (version %s)\n' "$archive" "$VERSION"
