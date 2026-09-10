#!/usr/bin/env bash
# Temp-HOME integration checks for the installer and its safety contract.
set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
TMP=$(mktemp -d "${TMPDIR:-/tmp}/ddd-workflow-kit-test.XXXXXX")
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
export HOME="$TMP/home"
mkdir -p "$HOME"

assert() { "$@" || { printf 'test-installer: assertion failed: %s\n' "$*" >&2; exit 1; }; }
assert_not_exists() { [ ! -e "$1" ] && [ ! -L "$1" ]; }

printf '1. global install and manager\n'
bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --global
assert [ -L "$HOME/.pi/agent/skills/ddd" ]
assert [ -x "$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" ]
assert [ "$("$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" version)" = 0.1.1 ]

printf '2. project path with spaces, multi-agent selection, and deduplication\n'
PROJECT="$TMP/project with spaces"
mkdir -p "$PROJECT"
bash "$ROOT/install.sh" --source-dir "$ROOT" --agent codex,antigravity --project "$PROJECT"
assert [ -L "$PROJECT/.agents/skills/ddd" ]
assert [ ! -e "$PROJECT/.gemini/config/skills/ddd" ]
# Both agents share .agents/skills; the link exists once and both registrations are recorded.
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert len(d["registrations"]) >= 3; assert len(d["links"]) == len({x["path"] for x in d["links"]}); assert any(x["agent"] == "codex,antigravity" for x in d["links"]); print("ok")' "$HOME/.ddd-workflow-kit/manifest.json")" = ok ]
CURRENT="$TMP/current project"
mkdir -p "$CURRENT"
(cd "$CURRENT" && HOME="$HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --project)
assert [ -L "$CURRENT/.pi/skills/ddd" ]
if HOME="$HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent not-an-agent --path "$TMP/invalid"; then
  printf 'test-installer: invalid agent unexpectedly succeeded\n' >&2; exit 1
fi

printf '3. unmanaged collision preservation\n'
COLLISION="$TMP/collision"
mkdir -p "$COLLISION"
printf 'keep me\n' > "$COLLISION/ddd"
if bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --path "$COLLISION"; then
  printf 'test-installer: collision unexpectedly succeeded\n' >&2; exit 1
fi
assert [ "$(cat "$COLLISION/ddd")" = 'keep me' ]

printf '4. update reconciliation and deleted-link safety\n'
SOURCE2="$TMP/source-v2"
cp -R "$ROOT" "$SOURCE2"
rm -rf "$SOURCE2/skills/ddd-tactical"
printf '0.2.0\n' > "$SOURCE2/VERSION"
REAL_CP=$(command -v cp)
FAIL_BIN="$TMP/failing-cp"
mkdir -p "$FAIL_BIN"
cat > "$FAIL_BIN/cp" <<EOF
#!/usr/bin/env bash
last=""
for arg in "\$@"; do last="\$arg"; done
case "\$last" in *.version-backup.*) exit 1 ;; esac
exec "$REAL_CP" "\$@"
EOF
chmod +x "$FAIL_BIN/cp"
if PATH="$FAIL_BIN:$PATH" bash "$ROOT/install.sh" --source-dir "$SOURCE2" --update; then
  printf 'test-installer: injected backup failure unexpectedly succeeded\n' >&2; exit 1
fi
assert [ -d "$HOME/.ddd-workflow-kit/skills/ddd" ]
assert [ -f "$HOME/.ddd-workflow-kit/manifest.json" ]
assert [ -f "$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" ]
assert [ "$(cat "$HOME/.ddd-workflow-kit/VERSION")" = 0.1.1 ]
assert [ "$(readlink "$HOME/.pi/agent/skills/ddd")" = "$HOME/.ddd-workflow-kit/skills/ddd" ]
SIGNAL_BIN="$TMP/signal-mv"
mkdir -p "$SIGNAL_BIN"
REAL_MV=$(command -v mv)
cat > "$SIGNAL_BIN/mv" <<EOF
#!/usr/bin/env bash
"$REAL_MV" "\$@"
case "\$2" in */.backup.*) kill -TERM "\$PPID" ;; esac
EOF
chmod +x "$SIGNAL_BIN/mv"
PATH="$SIGNAL_BIN:$PATH" bash "$ROOT/install.sh" --source-dir "$SOURCE2" --update
assert [ "$(cat "$HOME/.ddd-workflow-kit/VERSION")" = 0.2.0 ]
assert [ -d "$HOME/.ddd-workflow-kit/skills/ddd" ]
assert [ -L "$HOME/.pi/agent/skills/ddd" ]
FAIL_RM_BIN="$TMP/failing-rm"
mkdir -p "$FAIL_RM_BIN"
REAL_RM=$(command -v rm)
cat > "$FAIL_RM_BIN/rm" <<EOF
#!/usr/bin/env bash
"$REAL_RM" "\$@"
for arg in "\$@"; do
  case "\$arg" in *.journal.*) exit 74 ;; esac
done
EOF
chmod +x "$FAIL_RM_BIN/rm"
PATH="$FAIL_RM_BIN:$PATH" bash "$ROOT/install.sh" --source-dir "$SOURCE2" --update
assert [ -d "$HOME/.ddd-workflow-kit/skills/ddd" ]
assert [ -L "$HOME/.pi/agent/skills/ddd" ]
assert [ -e "$HOME/.pi/agent/skills/ddd/SKILL.md" ]
assert_not_exists "$HOME/.pi/agent/skills/ddd-tactical"
assert [ "$("$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" version)" = 0.2.0 ]
# A repointed deleted-skill link must block an update rather than remove it.
SOURCE3="$TMP/source-v3"
cp -R "$SOURCE2" "$SOURCE3"
rm -rf "$SOURCE3/skills/ddd-review"
rm -f "$HOME/.pi/agent/skills/ddd-review"
ln -s "$TMP/unrelated" "$HOME/.pi/agent/skills/ddd-review"
if bash "$ROOT/install.sh" --source-dir "$SOURCE3" --update; then
  printf 'test-installer: repointed deleted link unexpectedly succeeded\n' >&2; exit 1
fi
assert [ "$(readlink "$HOME/.pi/agent/skills/ddd-review")" = "$TMP/unrelated" ]
rm -f "$HOME/.pi/agent/skills/ddd-review"

printf '5. release archive contents and checksum failure\n'
DIST="$TMP/dist"
bash "$ROOT/scripts/build-release.sh" "$DIST"
BOOT_HOME="$TMP/bootstrap-home"
DDD_RELEASE_URL="file://$DIST/ddd-workflow-kit.tar.gz" DDD_CHECKSUM_URL="file://$DIST/ddd-workflow-kit.tar.gz.sha256" HOME="$BOOT_HOME" bash "$ROOT/install.sh" --agent pi --global
assert [ -L "$BOOT_HOME/.pi/agent/skills/ddd" ]
DDD_RELEASE_URL="file://$DIST/ddd-workflow-kit.tar.gz" DDD_CHECKSUM_URL="file://$DIST/ddd-workflow-kit.tar.gz.sha256" HOME="$BOOT_HOME" "$BOOT_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" update
assert [ -L "$BOOT_HOME/.pi/agent/skills/ddd" ]
EVIL="$TMP/evil-release"
mkdir -p "$EVIL/skills/ddd"
cp "$ROOT/install.sh" "$ROOT/VERSION" "$EVIL/"
ln -s "$TMP/outside" "$EVIL/skills/ddd/escape"
tar -czf "$TMP/evil.tar.gz" -C "$EVIL" install.sh VERSION skills
if command -v sha256sum >/dev/null 2>&1; then sha256sum "$TMP/evil.tar.gz" | awk '{print $1 "  evil.tar.gz"}' > "$TMP/evil.sha256"; else shasum -a 256 "$TMP/evil.tar.gz" | awk '{print $1 "  evil.tar.gz"}' > "$TMP/evil.sha256"; fi
if DDD_RELEASE_URL="file://$TMP/evil.tar.gz" DDD_CHECKSUM_URL="file://$TMP/evil.sha256" HOME="$TMP/evil-home" bash "$ROOT/install.sh" --agent pi --global; then
  printf 'test-installer: unsafe bootstrap archive unexpectedly succeeded\n' >&2; exit 1
fi
if DDD_RELEASE_URL="file://$TMP/evil.tar.gz" DDD_CHECKSUM_URL="file://$TMP/evil.sha256" HOME="$BOOT_HOME" "$BOOT_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" update; then
  printf 'test-installer: unsafe manager archive unexpectedly succeeded\n' >&2; exit 1
fi
assert [ -L "$BOOT_HOME/.pi/agent/skills/ddd" ]
TRAVERSAL="$TMP/traversal.tar.gz"
python3 - "$ROOT" "$TRAVERSAL" <<'PY'
import io, sys, tarfile
root, output = sys.argv[1:]
with tarfile.open(output, "w:gz") as archive:
    archive.add(root + "/install.sh", "install.sh")
    archive.add(root + "/VERSION", "VERSION")
    archive.add(root + "/skills", "skills")
    payload = b"escape"
    member = tarfile.TarInfo("skills/../escape")
    member.size = len(payload)
    archive.addfile(member, io.BytesIO(payload))
PY
if command -v sha256sum >/dev/null 2>&1; then sha256sum "$TRAVERSAL" | awk '{print $1 "  traversal.tar.gz"}' > "$TMP/traversal.sha256"; else shasum -a 256 "$TRAVERSAL" | awk '{print $1 "  traversal.tar.gz"}' > "$TMP/traversal.sha256"; fi
if DDD_RELEASE_URL="file://$TRAVERSAL" DDD_CHECKSUM_URL="file://$TMP/traversal.sha256" HOME="$TMP/traversal-home" bash "$ROOT/install.sh" --agent pi --global; then
  printf 'test-installer: unsafe traversal bootstrap archive unexpectedly succeeded\n' >&2; exit 1
fi
if DDD_RELEASE_URL="file://$TRAVERSAL" DDD_CHECKSUM_URL="file://$TMP/traversal.sha256" HOME="$BOOT_HOME" "$BOOT_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" update; then
  printf 'test-installer: unsafe traversal manager archive unexpectedly succeeded\n' >&2; exit 1
fi
tar -tzf "$DIST/ddd-workflow-kit.tar.gz" | while IFS= read -r entry; do
  case "$entry" in
    install.sh|VERSION|skills|skills/*) : ;;
    *) printf 'test-installer: unexpected archive entry: %s\n' "$entry" >&2; exit 1 ;;
  esac
done
BAD="$TMP/bad.sha256"
printf '%064d  ddd-workflow-kit.tar.gz\n' 0 > "$BAD"
if DDD_RELEASE_URL="file://$DIST/ddd-workflow-kit.tar.gz" DDD_CHECKSUM_URL="file://$BAD" HOME="$TMP/checksum-home" bash "$ROOT/install.sh" --agent pi --global; then
  printf 'test-installer: checksum failure unexpectedly succeeded\n' >&2; exit 1
fi
assert_not_exists "$TMP/checksum-home/.ddd-workflow-kit"

printf '6. interactive project selection through a pseudo-TTY\n'
if command -v script >/dev/null 2>&1 && script -qec true /dev/null >/dev/null 2>&1; then
  PTY_PROJECT="$TMP/pty project"
  PTY_HOME="$TMP/pty-home"
  mkdir -p "$PTY_PROJECT" "$PTY_HOME"
  (cd "$PTY_PROJECT" && printf 'pi\nproject\n\n' | script -qec "HOME='$PTY_HOME' bash '$ROOT/install.sh' --source-dir '$ROOT'" /dev/null) || { printf 'test-installer: interactive project install failed\n' >&2; exit 1; }
  assert [ -L "$PTY_PROJECT/.pi/skills/ddd" ]
  assert [ -d "$PTY_HOME/.ddd-workflow-kit/skills/ddd" ]
  assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert any(r["scope"] == "project" for r in d["registrations"]); assert any(l["scope"] == "project" for l in d["links"]); print("ok")' "$PTY_HOME/.ddd-workflow-kit/manifest.json")" = ok ]
else
  printf 'test-installer: skipping pseudo-TTY case; util-linux script not available\n'
fi

printf 'installer integration tests passed\n'
