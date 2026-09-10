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

printf '1. global install, shared target, and manager\n'
bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared,codex --global
assert [ -L "$HOME/.agents/skills/ddd" ]
assert [ "$(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" = "$(find "$HOME/.agents/skills" -mindepth 1 -maxdepth 1 -type l | wc -l | tr -d ' ')" ]
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert any(x["agent"] == "shared,codex" and x["path"].endswith("/.agents/skills/ddd") for x in d["links"]); print("ok")' "$HOME/.ddd-workflow-kit/manifest.json")" = ok ]
bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --global
bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --global
assert [ -L "$HOME/.pi/agent/skills/ddd" ]
assert [ -x "$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" ]
assert [ -x "$HOME/.ddd-workflow-kit/bin/install.sh" ]
assert [ "$("$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" version)" = 0.3.0 ]

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
printf '0.3.0\n' > "$SOURCE2/VERSION"
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
assert [ "$(cat "$HOME/.ddd-workflow-kit/VERSION")" = 0.3.0 ]
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
assert [ "$(cat "$HOME/.ddd-workflow-kit/VERSION")" = 0.3.0 ]
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
assert [ "$("$HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" version)" = 0.3.0 ]
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
NOTES_FIXTURE="$TMP/release-notes-fixture.md"
cat > "$NOTES_FIXTURE" <<'EOF'
# Changelog

## [1.2.30] - 2026-01-01
### Added
- wrong adjacent release

## [1.2.3] - 2026-02-02

### Added
- first release bullet

### Fixed
- second release bullet

## [2.0.0]
### Added
- undated release bullet
EOF
NOTES_EXPECTED="$TMP/release-notes-expected.md"
cat > "$NOTES_EXPECTED" <<'EOF'
### Added
- first release bullet

### Fixed
- second release bullet
EOF
bash "$ROOT/scripts/extract-release-notes.sh" 1.2.3 "$NOTES_FIXTURE" > "$TMP/release-notes.md"
assert cmp "$NOTES_EXPECTED" "$TMP/release-notes.md"
cat > "$TMP/undated-expected.md" <<'EOF'
### Added
- undated release bullet
EOF
bash "$ROOT/scripts/extract-release-notes.sh" 2.0.0 "$NOTES_FIXTURE" > "$TMP/undated-release-notes.md"
assert cmp "$TMP/undated-expected.md" "$TMP/undated-release-notes.md"
if bash "$ROOT/scripts/extract-release-notes.sh" 1.2.4 "$NOTES_FIXTURE" >/dev/null 2>&1; then
  printf 'test-installer: missing release-notes section unexpectedly succeeded\n' >&2; exit 1
fi
cat > "$TMP/empty-release-notes.md" <<'EOF'
## [3.0.0] - 2026-03-03

## [2.0.0]
### Added
- later content
EOF
if bash "$ROOT/scripts/extract-release-notes.sh" 3.0.0 "$TMP/empty-release-notes.md" >/dev/null 2>&1; then
  printf 'test-installer: empty release-notes section unexpectedly succeeded\n' >&2; exit 1
fi
cat > "$TMP/malformed-release-notes.md" <<'EOF'
## [4.0.0] - not-a-date
### Added
- malformed date

## [5.0.0] -
### Added
- missing date
EOF
if bash "$ROOT/scripts/extract-release-notes.sh" 4.0.0 "$TMP/malformed-release-notes.md" >/dev/null 2>&1; then
  printf 'test-installer: malformed dated release-notes section unexpectedly succeeded\n' >&2; exit 1
fi
if bash "$ROOT/scripts/extract-release-notes.sh" 5.0.0 "$TMP/malformed-release-notes.md" >/dev/null 2>&1; then
  printf 'test-installer: empty dated release-notes section unexpectedly succeeded\n' >&2; exit 1
fi
cat > "$TMP/missing-delimiter-release-notes.md" <<'EOF'
## [6.0.0]-2026-06-06
### Added
- missing pre-delimiter space

## [7.0.0] -2026-07-07
### Added
- missing post-delimiter space
EOF
if bash "$ROOT/scripts/extract-release-notes.sh" 6.0.0 "$TMP/missing-delimiter-release-notes.md" >/dev/null 2>&1; then
  printf 'test-installer: missing pre-delimiter space unexpectedly succeeded\n' >&2; exit 1
fi
if bash "$ROOT/scripts/extract-release-notes.sh" 7.0.0 "$TMP/missing-delimiter-release-notes.md" >/dev/null 2>&1; then
  printf 'test-installer: missing post-delimiter space unexpectedly succeeded\n' >&2; exit 1
fi
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
  # Toggle Shared, move to Codex and toggle it, confirm; then choose project.
  (cd "$PTY_PROJECT" && printf ' \033[B\033[B \n\033[B\n\n' | script -qec "HOME='$PTY_HOME' bash '$ROOT/install.sh' --source-dir '$ROOT'" /dev/null) || { printf 'test-installer: interactive project install failed\n' >&2; exit 1; }
  assert [ -L "$PTY_PROJECT/.agents/skills/ddd" ]
  assert [ "$(find "$PTY_PROJECT/.agents/skills" -mindepth 1 -maxdepth 1 -type l | wc -l | tr -d ' ')" = "$(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" ]
  assert [ -d "$PTY_HOME/.ddd-workflow-kit/skills/ddd" ]
  assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert any(r["scope"] == "project" for r in d["registrations"]); assert any(l["scope"] == "project" and l["agent"] == "shared,codex" for l in d["links"]); print("ok")' "$PTY_HOME/.ddd-workflow-kit/manifest.json")" = ok ]
else
  printf 'test-installer: skipping pseudo-TTY case; util-linux script not available\n'
fi

printf '7. uninstall filtering, rollback, safety, and full cleanup\n'
UN_HOME="$TMP/uninstall-home"
UN_PROJECT="$TMP/uninstall project"
UN_EXPLICIT="$TMP/uninstall-explicit"
mkdir -p "$UN_HOME" "$UN_PROJECT" "$UN_EXPLICIT"
printf 'keep project\n' > "$UN_PROJECT/unrelated.txt"
printf 'keep explicit\n' > "$UN_EXPLICIT/unrelated.txt"
HOME="$UN_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared,codex --global
HOME="$UN_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --project "$UN_PROJECT"
HOME="$UN_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent claude --path "$UN_EXPLICIT"
UN_MANAGER="$UN_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
DDD_RELEASE_URL=file:///missing DDD_CHECKSUM_URL=file:///missing HOME="$UN_HOME" "$UN_MANAGER" uninstall --partial --agent shared --global --yes
assert [ -L "$UN_HOME/.agents/skills/ddd" ]
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert {r["agent"] for r in d["registrations"]} == {"codex","pi","claude"}; assert all(l["agent"] != "shared" for l in d["links"]); print("ok")' "$UN_HOME/.ddd-workflow-kit/manifest.json")" = ok ]
DDD_RELEASE_URL=file:///missing DDD_CHECKSUM_URL=file:///missing HOME="$UN_HOME" "$UN_MANAGER" uninstall --partial --agent claude --path "$UN_EXPLICIT" --yes
assert_not_exists "$UN_EXPLICIT/ddd"
assert [ -f "$UN_EXPLICIT/unrelated.txt" ]
DDD_RELEASE_URL=file:///missing DDD_CHECKSUM_URL=file:///missing HOME="$UN_HOME" "$UN_MANAGER" uninstall --partial --agent codex --global --yes
assert_not_exists "$UN_HOME/.agents/skills/ddd"
assert [ -d "$UN_HOME/.ddd-workflow-kit/skills" ]
assert [ -f "$UN_HOME/.ddd-workflow-kit/bin/install.sh" ]
if DDD_RELEASE_URL=file:///missing DDD_CHECKSUM_URL=file:///missing HOME="$UN_HOME" "$UN_MANAGER" uninstall --full; then
  printf 'test-installer: incomplete full uninstall unexpectedly succeeded\n' >&2; exit 1
fi
if HOME="$UN_HOME" "$UN_MANAGER" uninstall --yes; then
  printf 'test-installer: bare --yes unexpectedly succeeded\n' >&2; exit 1
fi

UN_ROLLBACK_HOME="$TMP/uninstall-rollback-home"
mkdir -p "$UN_ROLLBACK_HOME"
HOME="$UN_ROLLBACK_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared,codex --global
UN_ROLLBACK_MANAGER="$UN_ROLLBACK_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
FAIL_UN_MV="$TMP/failing-uninstall-mv"
mkdir -p "$FAIL_UN_MV"
REAL_MV_UNINSTALL=$(command -v mv)
cat > "$FAIL_UN_MV/mv" <<EOF
#!/usr/bin/env bash
"$REAL_MV_UNINSTALL" "\$@"
case "\$2" in */manifest.json) exit 75 ;; esac
EOF
chmod +x "$FAIL_UN_MV/mv"
if PATH="$FAIL_UN_MV:$PATH" HOME="$UN_ROLLBACK_HOME" "$UN_ROLLBACK_MANAGER" uninstall --partial --agent shared --global --yes; then
  printf 'test-installer: manifest-write rollback unexpectedly succeeded\n' >&2; exit 1
fi
assert [ -L "$UN_ROLLBACK_HOME/.agents/skills/ddd" ]
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert {r["agent"] for r in d["registrations"]} == {"shared","codex"}; print("ok")' "$UN_ROLLBACK_HOME/.ddd-workflow-kit/manifest.json")" = ok ]

UN_CROSS_HOME="$TMP/uninstall-cross-scope-home"
mkdir -p "$UN_CROSS_HOME"
HOME="$UN_CROSS_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared --global
HOME="$UN_CROSS_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent claude --path "$UN_CROSS_HOME/.agents/skills"
UN_CROSS_MANAGER="$UN_CROSS_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
HOME="$UN_CROSS_HOME" "$UN_CROSS_MANAGER" uninstall --partial --agent shared --global --yes
assert [ -L "$UN_CROSS_HOME/.agents/skills/ddd" ]
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); r=[r for r in d["registrations"] if r["agent"] == "claude"][0]; l=[l for l in d["links"] if l["path"].endswith("/ddd")][0]; assert r["scope"] == "path" and l["scope"] == "path" and l["agent"] == "claude"; print("ok")' "$UN_CROSS_HOME/.ddd-workflow-kit/manifest.json")" = ok ]
HOME="$UN_CROSS_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --update
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); r=[r for r in d["registrations"] if r["agent"] == "claude"][0]; l=[l for l in d["links"] if l["path"].endswith("/ddd")][0]; assert r["scope"] == "path" and l["scope"] == "path" and l["agent"] == "claude"; print("ok")' "$UN_CROSS_HOME/.ddd-workflow-kit/manifest.json")" = ok ]

UN_SELECT_HOME="$TMP/uninstall-selective-preflight-home"
UN_SELECT_EXPLICIT="$TMP/uninstall-selective-preflight-explicit"
mkdir -p "$UN_SELECT_HOME" "$UN_SELECT_EXPLICIT"
HOME="$UN_SELECT_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared --global
HOME="$UN_SELECT_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent claude --path "$UN_SELECT_EXPLICIT"
printf 'unrelated\n' > "$TMP/selective-unrelated-target"
rm -f "$UN_SELECT_HOME/.agents/skills/ddd"
ln -s "$TMP/selective-unrelated-target" "$UN_SELECT_HOME/.agents/skills/ddd"
HOME="$UN_SELECT_HOME" "$UN_SELECT_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" uninstall --partial --agent claude --path "$UN_SELECT_EXPLICIT" --yes
assert_not_exists "$UN_SELECT_EXPLICIT/ddd"
assert [ "$(readlink "$UN_SELECT_HOME/.agents/skills/ddd")" = "$TMP/selective-unrelated-target" ]

UN_CHANGED_HOME="$TMP/uninstall-changed-home"
mkdir -p "$UN_CHANGED_HOME"
HOME="$UN_CHANGED_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared,codex --global
printf 'unrelated\n' > "$TMP/unrelated-target"
rm -f "$UN_CHANGED_HOME/.agents/skills/ddd"
ln -s "$TMP/unrelated-target" "$UN_CHANGED_HOME/.agents/skills/ddd"
if HOME="$UN_CHANGED_HOME" "$UN_CHANGED_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" uninstall --full --yes; then
  printf 'test-installer: changed-link full uninstall unexpectedly succeeded\n' >&2; exit 1
fi
assert [ "$(readlink "$UN_CHANGED_HOME/.agents/skills/ddd")" = "$TMP/unrelated-target" ]
assert [ -d "$UN_CHANGED_HOME/.ddd-workflow-kit" ]

UN_FULL_HOME="$TMP/uninstall-full-home"
UN_FULL_PROJECT="$TMP/uninstall-full-project"
UN_FULL_EXPLICIT="$TMP/uninstall-full-explicit"
mkdir -p "$UN_FULL_HOME" "$UN_FULL_PROJECT" "$UN_FULL_EXPLICIT"
printf 'preserve\n' > "$UN_FULL_PROJECT/keep.txt"
printf 'preserve\n' > "$UN_FULL_EXPLICIT/keep.txt"
HOME="$UN_FULL_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --global
HOME="$UN_FULL_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent codex --project "$UN_FULL_PROJECT"
HOME="$UN_FULL_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared --path "$UN_FULL_EXPLICIT"
rm -f "$UN_FULL_HOME/.pi/agent/skills/ddd"
HOME="$UN_FULL_HOME" "$UN_FULL_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" uninstall --full --yes
assert_not_exists "$UN_FULL_HOME/.ddd-workflow-kit"
assert_not_exists "$UN_FULL_HOME/.pi/agent/skills/ddd"
assert_not_exists "$UN_FULL_PROJECT/.agents/skills/ddd"
assert_not_exists "$UN_FULL_EXPLICIT/ddd"
assert [ -f "$UN_FULL_PROJECT/keep.txt" ]
assert [ -f "$UN_FULL_EXPLICIT/keep.txt" ]
assert [ -d "$UN_FULL_PROJECT/.agents/skills" ]
assert [ -d "$UN_FULL_EXPLICIT" ]

UN_FULL_ROLLBACK_HOME="$TMP/uninstall-full-rollback-home"
mkdir -p "$UN_FULL_ROLLBACK_HOME"
HOME="$UN_FULL_ROLLBACK_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --global
FAIL_FULL_RM_BIN="$TMP/failing-full-rm"
mkdir -p "$FAIL_FULL_RM_BIN"
cat > "$FAIL_FULL_RM_BIN/rm" <<EOF
#!/usr/bin/env bash
for arg in "\$@"; do
  case "\$arg" in
    */.ddd-workflow-kit.uninstall-backup.*)
      if [ -f "\$arg/manifest.json" ]; then
        "$REAL_RM" "\$arg/manifest.json"
        exit 74
      fi
      ;;
  esac
done
"$REAL_RM" "\$@"
EOF
chmod +x "$FAIL_FULL_RM_BIN/rm"
if PATH="$FAIL_FULL_RM_BIN:$PATH" HOME="$UN_FULL_ROLLBACK_HOME" "$UN_FULL_ROLLBACK_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" uninstall --full --yes; then
  printf 'test-installer: partial full-backup deletion unexpectedly succeeded\n' >&2; exit 1
fi
assert [ -f "$UN_FULL_ROLLBACK_HOME/.ddd-workflow-kit/manifest.json" ]
assert [ -x "$UN_FULL_ROLLBACK_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" ]
assert [ -L "$UN_FULL_ROLLBACK_HOME/.pi/agent/skills/ddd" ]

UN_REL_HOME="$TMP/uninstall-relative-home"
UN_REL_ORIGIN="$TMP/uninstall-relative-origin"
UN_REL_OTHER="$TMP/uninstall-relative-other"
mkdir -p "$UN_REL_HOME" "$UN_REL_ORIGIN" "$UN_REL_OTHER"
(cd "$UN_REL_ORIGIN" && HOME="$UN_REL_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --path relative-skills)
assert [ -L "$UN_REL_ORIGIN/relative-skills/ddd" ]
UN_REL_MANAGER="$UN_REL_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
(cd "$UN_REL_OTHER" && HOME="$UN_REL_HOME" "$UN_REL_MANAGER" uninstall --partial --agent pi --path "$UN_REL_ORIGIN/relative-skills" --yes)
assert_not_exists "$UN_REL_ORIGIN/relative-skills/ddd"
assert [ -f "$UN_REL_HOME/.ddd-workflow-kit/manifest.json" ]
(cd "$UN_REL_OTHER" && HOME="$UN_REL_HOME" "$UN_REL_MANAGER" uninstall --full --yes)
assert_not_exists "$UN_REL_HOME/.ddd-workflow-kit"

UN_LEGACY_HOME="$TMP/uninstall-legacy-relative-home"
mkdir -p "$UN_LEGACY_HOME"
HOME="$UN_LEGACY_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --global
python3 - "$UN_LEGACY_HOME/.ddd-workflow-kit/manifest.json" <<'PY'
import json, sys
path = sys.argv[1]
with open(path) as stream:
    manifest = json.load(stream)
for item in manifest["registrations"]:
    item["path"] = "legacy-skills"
for item in manifest["links"]:
    item["path"] = "legacy-skills/ddd"
with open(path, "w") as stream:
    json.dump(manifest, stream, indent=2, separators=(",", ":"))
PY
if (cd "$UN_REL_OTHER" && HOME="$UN_LEGACY_HOME" "$UN_LEGACY_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit" uninstall --full --yes); then
  printf 'test-installer: legacy relative manifest unexpectedly succeeded\n' >&2; exit 1
fi
assert [ -d "$UN_LEGACY_HOME/.ddd-workflow-kit" ]
assert [ -L "$UN_LEGACY_HOME/.pi/agent/skills/ddd" ]

printf '8. interactive uninstall multi-select, confirmation, and terminal restoration\n'
if command -v script >/dev/null 2>&1 && script -qec true /dev/null >/dev/null 2>&1; then
UN_PTY_HOME="$TMP/uninstall-pty-home"
mkdir -p "$UN_PTY_HOME"
HOME="$UN_PTY_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared,codex --global
UN_PTY_MANAGER="$UN_PTY_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
UN_PTY_BEFORE="$TMP/uninstall-pty-before"
UN_PTY_AFTER="$TMP/uninstall-pty-after"
# Partial, Global, toggle Shared, confirm, then choose Yes.
(printf '\033[B\n\n \n\033[B\n' | script -qec "stty -g >'$UN_PTY_BEFORE'; HOME='$UN_PTY_HOME' '$UN_PTY_MANAGER' uninstall; stty -g >'$UN_PTY_AFTER'" /dev/null) || { printf 'test-installer: interactive uninstall failed\n' >&2; exit 1; }
assert [ "$(cat "$UN_PTY_BEFORE")" = "$(cat "$UN_PTY_AFTER")" ]
assert [ -L "$UN_PTY_HOME/.agents/skills/ddd" ]
assert [ "$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert [r["agent"] for r in d["registrations"]] == ["codex"]; print("ok")' "$UN_PTY_HOME/.ddd-workflow-kit/manifest.json")" = ok ]

UN_PTY_EMPTY_HOME="$TMP/uninstall-pty-empty-home"
mkdir -p "$UN_PTY_EMPTY_HOME"
HOME="$UN_PTY_EMPTY_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent shared --global
UN_PTY_EMPTY_MANAGER="$UN_PTY_EMPTY_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
if (printf '\033[B\n\n\n' | script -qec "HOME='$UN_PTY_EMPTY_HOME' '$UN_PTY_EMPTY_MANAGER' uninstall" /dev/null >/dev/null 2>&1); then
  printf 'test-installer: empty interactive uninstall unexpectedly succeeded\n' >&2; exit 1
fi
assert [ -L "$UN_PTY_EMPTY_HOME/.agents/skills/ddd" ]

UN_PTY_PROJECT_HOME="$TMP/uninstall-pty-project-home"
UN_PTY_PROJECT="$TMP/uninstall-pty-project"
UN_PTY_EXPLICIT="$TMP/uninstall-pty-explicit"
mkdir -p "$UN_PTY_PROJECT_HOME" "$UN_PTY_PROJECT" "$UN_PTY_EXPLICIT"
HOME="$UN_PTY_PROJECT_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent pi --project "$UN_PTY_PROJECT"
HOME="$UN_PTY_PROJECT_HOME" bash "$ROOT/install.sh" --source-dir "$ROOT" --agent claude --path "$UN_PTY_EXPLICIT"
UN_PTY_PROJECT_MANAGER="$UN_PTY_PROJECT_HOME/.ddd-workflow-kit/bin/ddd-workflow-kit"
UN_PTY_PROJECT_BEFORE="$TMP/uninstall-pty-project-before"
UN_PTY_PROJECT_AFTER="$TMP/uninstall-pty-project-after"
# Partial, Project, toggle the explicit-path row, confirm Yes.
(cd "$UN_PTY_PROJECT" && printf '\033[B\n\033[B\n\033[B \n\033[B\n' | script -qec "stty -g >'$UN_PTY_PROJECT_BEFORE'; HOME='$UN_PTY_PROJECT_HOME' '$UN_PTY_PROJECT_MANAGER' uninstall; stty -g >'$UN_PTY_PROJECT_AFTER'" /dev/null) || { printf 'test-installer: interactive explicit-path uninstall failed\n' >&2; exit 1; }
assert [ "$(cat "$UN_PTY_PROJECT_BEFORE")" = "$(cat "$UN_PTY_PROJECT_AFTER")" ]
assert [ -L "$UN_PTY_PROJECT/.pi/skills/ddd" ]
assert_not_exists "$UN_PTY_EXPLICIT/ddd"
else
  printf 'test-installer: skipping interactive uninstall cases; compatible script is not available\n'
fi

printf 'installer integration tests passed\n'
