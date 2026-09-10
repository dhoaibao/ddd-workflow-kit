#!/usr/bin/env bash
# DDD Workflow Kit installer. Bash 3.2-compatible; no shell-profile changes.
set -eu

REPO_URL_DEFAULT="https://github.com/dhoaibao/ddd-workflow-kit"
RELEASE_URL_DEFAULT="$REPO_URL_DEFAULT/releases/latest/download/ddd-workflow-kit.tar.gz"
CHECKSUM_URL_DEFAULT="$REPO_URL_DEFAULT/releases/latest/download/ddd-workflow-kit.tar.gz.sha256"
STATE_DIR="${HOME}/.ddd-workflow-kit"
CACHE_DIR="$STATE_DIR/skills"
MANIFEST="$STATE_DIR/manifest.json"
VERSION_FILE="$STATE_DIR/VERSION"
MANAGER="$STATE_DIR/bin/ddd-workflow-kit"

say() { printf '%s\n' "$*"; }
fail() { printf 'ddd-workflow-kit: error: %s\n' "$*" >&2; exit 1; }
usage() {
  cat <<'EOF'
Usage: install.sh [options]

Install options:
  --agent NAME[,NAME...]   shared, claude, codex, opencode, antigravity, or pi
  --global                 Register skills in the selected agents' global dirs
  --project [PATH]         Register skills in a project (default: current dir)
  --path PATH              Register one explicit skills directory
  --update                 Refresh every registration in the existing manifest
  --source-dir PATH        Use a local release directory (maintainer/testing)
  --help                   Show this help

With no selection flags, the installer prompts on /dev/tty. The installer
never modifies shell profiles, clones a repository, or installs product code.
EOF
}

need_command() { command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"; }

json_escape() {
  # Quotes and newlines in paths are rejected before this function is called.
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

safe_field() {
  case "$1" in *'"'*) fail "path contains an unsupported quote: $1" ;; esac
  case "$1" in *\\*) fail "path contains an unsupported backslash: $1" ;; esac
  case "$1" in *'|'*) fail "path contains an unsupported delimiter: $1" ;; esac
  case "$1" in *$'\t'*|*$'\n'*|*$'\r'*) fail "path contains an unsupported control character: $1" ;; esac
}

agent_global_path() {
  case "$1" in
    shared|codex) printf '%s/.agents/skills' "$HOME" ;;
    claude) printf '%s/.claude/skills' "$HOME" ;;
    opencode) printf '%s/.config/opencode/skills' "$HOME" ;;
    antigravity) printf '%s/.gemini/config/skills' "$HOME" ;;
    pi) printf '%s/.pi/agent/skills' "$HOME" ;;
    *) fail "unknown agent: $1" ;;
  esac
}

agent_project_path() {
  case "$1" in
    shared|codex) printf '%s/.agents/skills' "$2" ;;
    claude) printf '%s/.claude/skills' "$2" ;;
    antigravity) printf '%s/.agents/skills' "$2" ;;
    opencode) printf '%s/.opencode/skills' "$2" ;;
    pi) printf '%s/.pi/skills' "$2" ;;
    *) fail "unknown agent: $1" ;;
  esac
}

validate_agent() {
  case "$1" in
    shared|claude|codex|opencode|antigravity|pi) : ;;
    *) fail "unknown agent: $1" ;;
  esac
}

add_agent() {
  value=$1
  oldIFS=$IFS; IFS=','
  # shellcheck disable=SC2086
  set -- $value
  IFS=$oldIFS
  for agent in "$@"; do
    [ -n "$agent" ] || continue
    validate_agent "$agent"
    case " $SELECTED_AGENTS " in *" $agent "*) : ;; *) SELECTED_AGENTS="$SELECTED_AGENTS $agent" ;; esac
  done
}

# The selector deliberately uses only Bash builtins and stty. Keeping the
# terminal state in one small helper makes the interactive path safe on both
# Bash 3.2 (macOS) and modern Bash (Linux), including interrupted installs.
selector_restore() {
  if [ "${SELECTOR_ACTIVE:-0}" -eq 1 ]; then
    stty "$SELECTOR_STTY_STATE" <"$SELECTOR_TTY" 2>/dev/null || :
    printf '\033[?25h\033[0m' >"$SELECTOR_TTY" 2>/dev/null || :
    SELECTOR_ACTIVE=0
  fi
  trap - EXIT HUP INT TERM
}

selector_interrupt() {
  selector_restore
  exit 130
}

selector_begin() {
  SELECTOR_TTY=$1
  SELECTOR_STTY_STATE=$(stty -g <"$SELECTOR_TTY") || fail "could not inspect terminal settings"
  SELECTOR_ACTIVE=1
  trap 'selector_restore' EXIT
  trap 'selector_interrupt' HUP INT TERM
  stty -icanon -echo min 1 time 0 <"$SELECTOR_TTY" || fail "could not configure interactive terminal"
  printf '\033[?25l' >"$SELECTOR_TTY"
}

selector_value() {
  case "$SELECTOR_KIND:$1" in
    agents:1) printf 'shared' ;;
    agents:2) printf 'claude' ;;
    agents:3) printf 'codex' ;;
    agents:4) printf 'opencode' ;;
    agents:5) printf 'antigravity' ;;
    agents:6) printf 'pi' ;;
    scope:1) printf 'global' ;;
    scope:2) printf 'project' ;;
    *) return 1 ;;
  esac
}

selector_label() {
  case "$SELECTOR_KIND:$1" in
    agents:1) printf 'Shared agents (.agents/skills)' ;;
    agents:2) printf 'Claude' ;;
    agents:3) printf 'Codex' ;;
    agents:4) printf 'OpenCode' ;;
    agents:5) printf 'Antigravity' ;;
    agents:6) printf 'Pi' ;;
    scope:1) printf 'Global (~/.agents/skills or agent default)' ;;
    scope:2) printf 'Project (a project-local skills directory)' ;;
    *) return 1 ;;
  esac
}

selector_selected() {
  case "$1" in
    1) [ "${SELECTOR_SELECTED_1:-0}" -eq 1 ] ;;
    2) [ "${SELECTOR_SELECTED_2:-0}" -eq 1 ] ;;
    3) [ "${SELECTOR_SELECTED_3:-0}" -eq 1 ] ;;
    4) [ "${SELECTOR_SELECTED_4:-0}" -eq 1 ] ;;
    5) [ "${SELECTOR_SELECTED_5:-0}" -eq 1 ] ;;
    6) [ "${SELECTOR_SELECTED_6:-0}" -eq 1 ] ;;
    *) return 1 ;;
  esac
}

selector_toggle() {
  case "$1" in
    1) SELECTOR_SELECTED_1=$((1 - SELECTOR_SELECTED_1)) ;;
    2) SELECTOR_SELECTED_2=$((1 - SELECTOR_SELECTED_2)) ;;
    3) SELECTOR_SELECTED_3=$((1 - SELECTOR_SELECTED_3)) ;;
    4) SELECTOR_SELECTED_4=$((1 - SELECTOR_SELECTED_4)) ;;
    5) SELECTOR_SELECTED_5=$((1 - SELECTOR_SELECTED_5)) ;;
    6) SELECTOR_SELECTED_6=$((1 - SELECTOR_SELECTED_6)) ;;
  esac
}

selector_draw() {
  if [ "${SELECTOR_DRAWN:-0}" -eq 1 ]; then
    printf '\033[%sA' "$SELECTOR_LINES" >"$SELECTOR_TTY"
  fi
  printf '\033[2K\rSelect %s (↑/↓ move, %s, Enter confirm):\n' \
    "$SELECTOR_TITLE" "$SELECTOR_ACTION" >"$SELECTOR_TTY"
  if [ "$SELECTOR_KIND" = agents ]; then
    printf '\033[2K\rSpace toggles targets; Shared agents is the common .agents/skills target.\n' >"$SELECTOR_TTY"
  else
    printf '\033[2K\rChoose one scope; project path is requested after confirmation.\n' >"$SELECTOR_TTY"
  fi
  index=1
  while [ "$index" -le "$SELECTOR_COUNT" ]; do
    cursor=' '
    [ "$index" -eq "$SELECTOR_CURSOR" ] && cursor='>'
    if [ "$SELECTOR_KIND" = agents ]; then
      marker=' '
      selector_selected "$index" && marker='x'
      printf '\033[2K\r%s [%s] %s\n' "$cursor" "$marker" "$(selector_label "$index")" >"$SELECTOR_TTY"
    else
      printf '\033[2K\r%s %s\n' "$cursor" "$(selector_label "$index")" >"$SELECTOR_TTY"
    fi
    index=$((index + 1))
  done
  SELECTOR_LINES=$((SELECTOR_COUNT + 2))
  SELECTOR_DRAWN=1
}

selector_read_event() {
  SELECTOR_EVENT=none
  key=''
  IFS= read -r -n 1 key <"$SELECTOR_TTY" || return 1
  case "$key" in
    '') SELECTOR_EVENT=enter ;;
    ' ') SELECTOR_EVENT=space ;;
    q|Q) SELECTOR_EVENT=cancel ;;
    *)
      [ "$key" = "$(printf '\033')" ] || return 0
      next=''
      IFS= read -r -n 1 -t 1 next <"$SELECTOR_TTY" || return 0
      case "$next" in
        '['|'O')
          IFS= read -r -n 1 -t 1 next <"$SELECTOR_TTY" || return 0
          case "$next" in
            A) SELECTOR_EVENT=up ;;
            B) SELECTOR_EVENT=down ;;
          esac
          ;;
      esac
      ;;
  esac
}

prompt_targets() {
  SELECTOR_KIND=agents
  SELECTOR_TITLE='agents'
  SELECTOR_ACTION='Space toggles'
  SELECTOR_COUNT=6
  SELECTOR_CURSOR=1
  SELECTOR_SELECTED_1=0; SELECTOR_SELECTED_2=0; SELECTOR_SELECTED_3=0
  SELECTOR_SELECTED_4=0; SELECTOR_SELECTED_5=0; SELECTOR_SELECTED_6=0
  SELECTOR_DRAWN=0
  selector_begin /dev/tty
  selector_draw
  while :; do
    selector_read_event || { selector_restore; fail 'could not read agent selection'; }
    case "$SELECTOR_EVENT" in
      up) [ "$SELECTOR_CURSOR" -gt 1 ] && SELECTOR_CURSOR=$((SELECTOR_CURSOR - 1)) ;;
      down) [ "$SELECTOR_CURSOR" -lt "$SELECTOR_COUNT" ] && SELECTOR_CURSOR=$((SELECTOR_CURSOR + 1)) ;;
      space) selector_toggle "$SELECTOR_CURSOR" ;;
      enter) break ;;
      cancel) selector_restore; fail 'interactive selection cancelled' ;;
    esac
    selector_draw
  done
  selector_restore
  SELECTED_AGENTS=''
  index=1
  while [ "$index" -le "$SELECTOR_COUNT" ]; do
    if selector_selected "$index"; then
      add_agent "$(selector_value "$index")"
    fi
    index=$((index + 1))
  done
  [ -n "$SELECTED_AGENTS" ] || fail 'select at least one agent'
}

prompt_scope() {
  SELECTOR_KIND=scope
  SELECTOR_TITLE='scope'
  SELECTOR_ACTION='Arrow keys choose'
  SELECTOR_COUNT=2
  SELECTOR_CURSOR=1
  SELECTOR_SELECTED_1=0; SELECTOR_SELECTED_2=0
  SELECTOR_DRAWN=0
  selector_begin /dev/tty
  selector_draw
  while :; do
    selector_read_event || { selector_restore; fail 'could not read scope selection'; }
    case "$SELECTOR_EVENT" in
      up) [ "$SELECTOR_CURSOR" -gt 1 ] && SELECTOR_CURSOR=$((SELECTOR_CURSOR - 1)) ;;
      down) [ "$SELECTOR_CURSOR" -lt "$SELECTOR_COUNT" ] && SELECTOR_CURSOR=$((SELECTOR_CURSOR + 1)) ;;
      enter) break ;;
      space) : ;;
      cancel) selector_restore; fail 'interactive selection cancelled' ;;
    esac
    selector_draw
  done
  selector_restore
  SELECTED_SCOPE=$(selector_value "$SELECTOR_CURSOR")
}

prompt_selection() {
  tty=/dev/tty
  [ -r "$tty" ] && [ -w "$tty" ] || fail 'interactive selection requires /dev/tty; use --agent NAME and --global/--project/--path'
  prompt_targets
  prompt_scope
  case "$SELECTED_SCOPE" in
    global) SCOPE=global ;;
    project)
      SCOPE=project
      printf 'Project path (empty for current directory): ' >"$tty"
      IFS= read -r PROJECT_ROOT <"$tty" || fail 'could not read project path'
      [ -n "$PROJECT_ROOT" ] || PROJECT_ROOT=$PWD
      ;;
    *) fail 'internal: invalid scope' ;;
  esac
}

sha256() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}'; return; fi
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}'; return; fi
  fail "sha256sum or shasum is required for checksum verification"
}

fetch_url() {
  need_command curl
  curl -fsSL "$1" -o "$2" || fail "download failed: $1"
}

validate_archive_listing() {
  archive=$1
  need_command tar
  listing=$(tar -tzf "$archive") || fail "cannot read release archive"
  [ -n "$listing" ] || fail "release archive is empty"
  while IFS= read -r entry; do
    case "$entry" in
      /*|../*|*/../*|*/..|.*|*/./*|*/.|*/.*|*'\n'*|*'\r'*) fail "unsafe release archive entry: $entry" ;;
      install.sh|VERSION|skills|skills/*) : ;;
      *) fail "unexpected release archive entry: $entry" ;;
    esac
  done <<EOF
$listing
EOF
  verbose=$(tar -tvzf "$archive") || fail "cannot inspect release archive members"
  while IFS= read -r entry; do
    case "$entry" in -*|d*) : ;; *) fail "release archive contains a non-file/non-directory member" ;; esac
  done <<EOF
$verbose
EOF
}

prepare_download_source() {
  # Sets SOURCE_DIR and owns DOWNLOAD_TMP until cleanup at process exit.
  release_url=${DDD_RELEASE_URL:-$RELEASE_URL_DEFAULT}
  checksum_url=${DDD_CHECKSUM_URL:-$CHECKSUM_URL_DEFAULT}
  need_command mktemp
  DOWNLOAD_TMP=$(mktemp -d "${TMPDIR:-/tmp}/ddd-workflow-kit.XXXXXX")
  trap 'rm -rf "$DOWNLOAD_TMP"' EXIT HUP INT TERM
  archive="$DOWNLOAD_TMP/release.tar.gz"
  checksum="$DOWNLOAD_TMP/release.sha256"
  fetch_url "$release_url" "$archive"
  fetch_url "$checksum_url" "$checksum"
  expected=$(awk 'NF {print $1; exit}' "$checksum")
  case "$expected" in
    ''|*[!0123456789abcdefABCDEF]*) fail "checksum file does not contain a SHA-256 digest" ;;
  esac
  [ "${#expected}" -eq 64 ] || fail "checksum file does not contain a 64-character SHA-256 digest"
  actual=$(sha256 "$archive")
  [ "$actual" = "$expected" ] || fail "release checksum mismatch"
  validate_archive_listing "$archive"
  extract="$DOWNLOAD_TMP/extracted"
  mkdir "$extract"
  tar -xzf "$archive" -C "$extract" || fail "cannot extract release archive"
  bad_member=$(find "$extract" -type l -print -quit)
  [ -z "$bad_member" ] || fail "release archive contains a symlink: $bad_member"
  [ -f "$extract/install.sh" ] && [ -f "$extract/VERSION" ] && [ -d "$extract/skills" ] || fail "release archive is missing required files"
  SOURCE_DIR=$extract
}

validate_source() {
  [ -d "$1/skills" ] || fail "source has no skills directory: $1"
  [ -f "$1/VERSION" ] || fail "source has no VERSION file: $1"
  bad_member=$(find "$1/skills" -type l -print -quit)
  [ -z "$bad_member" ] || fail "source contains a symlink: $bad_member"
  VERSION=$(awk 'NF {print $1; exit}' "$1/VERSION")
  [ -n "$VERSION" ] || fail "source VERSION is empty"
  SKILL_NAMES=""
  for skill_dir in "$1/skills"/*; do
    [ -d "$skill_dir" ] || continue
    skill=$(basename "$skill_dir")
    case "$skill" in *[!A-Za-z0-9_-]*) fail "unsafe skill name: $skill" ;; esac
    SKILL_NAMES="$SKILL_NAMES $skill"
  done
  [ -n "$SKILL_NAMES" ] || fail "source contains no skills"
}

# Read one compact manifest object. The manifest is generated by this script;
# fields deliberately disallow quotes/backslashes so this remains Bash 3.2-safe.
field() {
  line=$1; key=$2
  printf '%s\n' "$line" | sed -n "s/.*\"$key\":\"\([^\"]*\)\".*/\1/p"
}

load_old_links() {
  OLD_LINK_LINES=""
  [ -f "$MANIFEST" ] || return 0
  while IFS= read -r line; do
    case "$line" in *'"skill":"'*) OLD_LINK_LINES="$OLD_LINK_LINES$line
" ;; esac
  done < "$MANIFEST"
}

add_registration() {
  agent=$1; scope=$2; root=$3; dest=$4
  REG_LINES="$REG_LINES$(printf '%s\t%s\t%s\t%s' "$agent" "$scope" "$root" "$dest")
"
}

# Keep this loop in the parent shell so registration state survives on Bash 3.2.
build_registrations_from_old_links() {
  REG_LINES=""; SEEN_REG_KEYS=""
  [ -n "$OLD_LINK_LINES" ] || return 0
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    agents=$(field "$line" agent); scope=$(field "$line" scope); root=$(field "$line" project_root); path=$(field "$line" path)
    dest=${path%/*}
    oldAgentIFS=$IFS; IFS=','
    set -f
    # shellcheck disable=SC2086
    set -- $agents
    set +f
    IFS=$oldAgentIFS
    for agent in "$@"; do
      [ -n "$agent" ] || continue
      key="$agent|$scope|$root|$dest"
      case " $SEEN_REG_KEYS " in *" $key "*) continue ;; esac
      SEEN_REG_KEYS="$SEEN_REG_KEYS $key"
      add_registration "$agent" "$scope" "$root" "$dest"
    done
  done
  IFS=$oldIFS
}

build_fresh_registrations() {
  build_registrations_from_old_links
  SEEN_DEST_KEYS="$SEEN_REG_KEYS"
  for agent in $SELECTED_AGENTS; do
    [ -n "$agent" ] || continue
    case "$SCOPE" in
      global) dest=$(agent_global_path "$agent"); root="" ;;
      project) root=$(cd "$PROJECT_ROOT" 2>/dev/null && pwd -P) || fail "project path does not exist: $PROJECT_ROOT"; dest=$(agent_project_path "$agent" "$root") ;;
      path) root=""; dest=$EXPLICIT_PATH ;;
      *) fail "internal: invalid scope" ;;
    esac
    safe_field "$root"; safe_field "$dest"
    key="$dest"
    # Keep one registration per agent even when physical destinations overlap.
    regkey="$agent|$SCOPE|$root|$dest"
    case " $SEEN_DEST_KEYS " in *" $regkey "*) continue ;; esac
    SEEN_DEST_KEYS="$SEEN_DEST_KEYS $regkey"
    add_registration "$agent" "$SCOPE" "$root" "$dest"
  done
}

read_registrations() {
  DEST_LINES=""; SEEN_DESTS=""
  oldIFS=$IFS; IFS=$'\n'
  for record in $REG_LINES; do
    [ -n "$record" ] || continue
    agent=$(printf '%s' "$record" | awk -F '\t' '{print $1}')
    scope=$(printf '%s' "$record" | awk -F '\t' '{print $2}')
    root=$(printf '%s' "$record" | awk -F '\t' '{print $3}')
    dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
    key="$dest"
    case " $SEEN_DESTS " in *" $key "*) continue ;; esac
    SEEN_DESTS="$SEEN_DESTS $key"
    DEST_LINES="$DEST_LINES$(printf '%s\t%s\t%s' "$dest" "$scope" "$root")
"
  done
  IFS=$oldIFS
}

old_link_for_path() {
  wanted=$1
  result=""
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    path=$(field "$line" path)
    [ "$path" = "$wanted" ] || continue
    result=$line; break
  done
  IFS=$oldIFS
  printf '%s' "$result"
}

preflight_links() {
  # Validate deleted links before touching cache or registrations.
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    skill=$(field "$line" skill); path=$(field "$line" path); target=$(field "$line" target)
    case " $SKILL_NAMES " in *" $skill "*) continue ;; esac
    if [ -e "$path" ] || [ -L "$path" ]; then
      [ -L "$path" ] || fail "deleted skill collision is not a symlink: $path"
      actual=$(readlink "$path") || fail "cannot inspect deleted skill link: $path"
      [ "$actual" = "$target" ] || fail "deleted skill link was repointed; refusing removal: $path"
    fi
  done
  IFS=$oldIFS

  oldIFS=$IFS; IFS=$'\n'
  for record in $DEST_LINES; do
    [ -n "$record" ] || continue
    dest=$(printf '%s' "$record" | awk -F '\t' '{print $1}')
    for skill_dir in "$SOURCE_DIR/skills"/*; do
      [ -d "$skill_dir" ] || continue
      skill=$(basename "$skill_dir"); path="$dest/$skill"
      if [ -e "$path" ] || [ -L "$path" ]; then
        [ -L "$path" ] || fail "refusing to overwrite unmanaged path: $path"
        actual=$(readlink "$path") || fail "cannot inspect existing link: $path"
        oldline=$(old_link_for_path "$path")
        oldtarget=$(field "$oldline" target)
        [ -n "$oldline" ] && [ "$actual" = "$oldtarget" ] || fail "refusing to repoint unmanaged or repointed link: $path"
      fi
    done
  done
  IFS=$oldIFS
}

registered_agents_for_dest() {
  wanted=$1; result=""; oldIFS=$IFS; IFS=$'\n'
  for registration in $REG_LINES; do
    [ -n "$registration" ] || continue
    agent=$(printf '%s' "$registration" | awk -F '\t' '{print $1}')
    dest=$(printf '%s' "$registration" | awk -F '\t' '{print $4}')
    [ "$dest" = "$wanted" ] || continue
    [ -n "$result" ] && result="$result,$agent" || result=$agent
  done
  IFS=$oldIFS
  printf '%s' "$result"
}

write_manifest() {
  destination=$1
  tmp="$destination.tmp.$$"
  {
    printf '{\n  "schema": 1,\n  "version": "%s",\n  "source": "%s",\n  "registrations": [\n' "$(json_escape "$VERSION")" "$(json_escape "$SOURCE_URL")"
    first=1
    oldIFS=$IFS; IFS=$'\n'
    for record in $REG_LINES; do
      [ -n "$record" ] || continue
      agent=$(printf '%s' "$record" | awk -F '\t' '{print $1}'); scope=$(printf '%s' "$record" | awk -F '\t' '{print $2}'); root=$(printf '%s' "$record" | awk -F '\t' '{print $3}'); dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
      [ "$first" -eq 1 ] || printf ',\n'; first=0
      printf '    {"agent":"%s","scope":"%s","project_root":"%s","path":"%s"}' "$(json_escape "$agent")" "$(json_escape "$scope")" "$(json_escape "$root")" "$(json_escape "$dest")"
    done
    IFS=$oldIFS
    printf '\n  ],\n  "links": [\n'
    first=1
    oldIFS=$IFS; IFS=$'\n'
    for destination_record in $DEST_LINES; do
      [ -n "$destination_record" ] || continue
      dest=$(printf '%s' "$destination_record" | awk -F '\t' '{print $1}'); scope=$(printf '%s' "$destination_record" | awk -F '\t' '{print $2}'); root=$(printf '%s' "$destination_record" | awk -F '\t' '{print $3}')
      agents=$(registered_agents_for_dest "$dest")
      for skill_dir in "$SOURCE_DIR/skills"/*; do
        [ -d "$skill_dir" ] || continue
        skill=$(basename "$skill_dir"); path="$dest/$skill"; target="$CACHE_DIR/$skill"
        [ "$first" -eq 1 ] || printf ',\n'; first=0
        printf '    {"agent":"%s","scope":"%s","project_root":"%s","skill":"%s","path":"%s","target":"%s"}' "$(json_escape "$agents")" "$(json_escape "$scope")" "$(json_escape "$root")" "$(json_escape "$skill")" "$(json_escape "$path")" "$(json_escape "$target")"
      done
    done
    IFS=$oldIFS
    printf '\n  ]\n}\n'
  } > "$tmp" || { rm -f "$tmp"; fail "cannot write manifest"; }
  mv "$tmp" "$destination" || fail "cannot install manifest"
}

write_manager() {
  tmp="$MANAGER.tmp.$$"
  mkdir -p "$(dirname "$MANAGER")"
  cat > "$tmp" <<EOF
#!/usr/bin/env bash
# DDD_WORKFLOW_KIT_MANAGER

set -eu
STATE_DIR="\${HOME}/.ddd-workflow-kit"
RELEASE_URL="${RELEASE_URL_DEFAULT}"
CHECKSUM_URL="${CHECKSUM_URL_DEFAULT}"
fetch() { command -v curl >/dev/null 2>&1 || { echo "ddd-workflow-kit: curl is required" >&2; exit 1; }; curl -fsSL "\$1" -o "\$2" || exit 1; }
sha256() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "\$1" | awk '{print \$1}'; else shasum -a 256 "\$1" | awk '{print \$1}'; fi; }
validate_archive() {
  listing=\$(tar -tzf "\$1") || exit 1
  while IFS= read -r entry; do
    case "\$entry" in
      /*|../*|*/../*|*/..|.*|*/./*|*/.|*/.*) echo "ddd-workflow-kit: unsafe release archive entry: \$entry" >&2; exit 1 ;;
      install.sh|VERSION|skills|skills/*) : ;;
      *) echo "ddd-workflow-kit: unsafe release archive entry: \$entry" >&2; exit 1 ;;
    esac
  done <<LISTING
\$listing
LISTING
  verbose=\$(tar -tvzf "\$1") || exit 1
  while IFS= read -r entry; do
    case "\$entry" in -*|d*) : ;; *) echo "ddd-workflow-kit: release archive contains a non-file/non-directory member" >&2; exit 1 ;; esac
  done <<VERBOSE
\$verbose
VERBOSE
}
download() {
  t=\$(mktemp -d "\${TMPDIR:-/tmp}/ddd-workflow-kit-manager.XXXXXX"); trap 'rm -rf "\$t"' EXIT HUP INT TERM
  fetch "\${DDD_RELEASE_URL:-\$RELEASE_URL}" "\$t/release.tar.gz"; fetch "\${DDD_CHECKSUM_URL:-\$CHECKSUM_URL}" "\$t/release.sha256"
  expected=\$(awk 'NF {print \$1; exit}' "\$t/release.sha256"); actual=\$(sha256 "\$t/release.tar.gz")
  [ "\$expected" = "\$actual" ] || { echo "ddd-workflow-kit: release checksum mismatch" >&2; exit 1; }
  validate_archive "\$t/release.tar.gz"
  mkdir "\$t/release"; tar -xzf "\$t/release.tar.gz" -C "\$t/release" || exit 1
  bash "\$t/release/install.sh" --source-dir "\$t/release" "\$@"
}
case "\${1:-}" in
  update) shift; download --update "\$@" ;;
  install) shift; download "\$@" ;;
  version|--version) cat "\$STATE_DIR/VERSION" ;;
  *) echo "Usage: ddd-workflow-kit {install|update|version}" >&2; exit 2 ;;
esac
EOF
  chmod 755 "$tmp" || fail "cannot chmod manager"
  mv "$tmp" "$MANAGER" || fail "cannot install manager"
}

install_release() {
  validate_source "$SOURCE_DIR"
  mkdir -p "$STATE_DIR/bin"
  safe_field "$STATE_DIR"; safe_field "$CACHE_DIR"; safe_field "$MANIFEST"
  if [ -e "$MANAGER" ] || [ -L "$MANAGER" ]; then
    if [ ! -f "$MANAGER" ] || ! awk 'NR == 2 { found=($0 == "# DDD_WORKFLOW_KIT_MANAGER") } END { exit (found ? 0 : 1) }' "$MANAGER"; then
      fail "refusing to overwrite unmanaged manager: $MANAGER"
    fi
  fi
  if [ -d "$CACHE_DIR" ] && [ ! -f "$MANIFEST" ]; then
    fail "refusing to overwrite unmanaged cache: $CACHE_DIR"
  fi
  SOURCE_URL=${DDD_SOURCE_URL:-${DDD_RELEASE_URL:-$RELEASE_URL_DEFAULT}}
  load_old_links
  if [ "$UPDATE" -eq 1 ]; then
    [ -f "$MANIFEST" ] || fail "cannot update before an install"
    build_registrations_from_old_links
    [ -n "$REG_LINES" ] || fail "manifest has no registrations"
  else
    build_fresh_registrations
  fi
  read_registrations
  preflight_links

  stage="$STATE_DIR/.stage.$$"; backup="$STATE_DIR/.backup.$$"
  rm -rf "$stage" "$backup"
  mkdir -p "$stage/skills"
  cp -R "$SOURCE_DIR/skills/." "$stage/skills/" || fail "cannot stage skills"

  CREATED_LINKS=""; REMOVED_LINKS=""; ROLLED_BACK=0
  JOURNAL="$STATE_DIR/.journal.$$"
  VERSION_BACKUP="$STATE_DIR/.version-backup.$$"
  MANAGER_BACKUP="$STATE_DIR/.manager-backup.$$"
  MANIFEST_BACKUP="$STATE_DIR/.manifest-backup.$$"
  OLD_VERSION_EXISTS=0; OLD_MANAGER_EXISTS=0; OLD_MANIFEST_EXISTS=0
  CACHE_MOVED=0; CACHE_ACTIVATED=0
  rollback() {
    [ "$ROLLED_BACK" -eq 0 ] || return 0
    ROLLED_BACK=1
    oldIFS=$IFS; IFS=$'\n'
    for path in $CREATED_LINKS; do [ -L "$path" ] && rm -f "$path"; done
    for record in $REMOVED_LINKS; do
      oldpath=$(printf '%s' "$record" | awk -F '\t' '{print $1}'); oldtarget=$(printf '%s' "$record" | awk -F '\t' '{print $2}')
      [ -e "$oldpath" ] || [ -L "$oldpath" ] || ln -s "$oldtarget" "$oldpath"
    done
    IFS=$oldIFS
    if [ "$CACHE_ACTIVATED" -eq 1 ]; then rm -rf "$CACHE_DIR"; fi
    if [ "$CACHE_MOVED" -eq 1 ] && [ -d "$backup" ]; then mv "$backup" "$CACHE_DIR"; fi
    if [ "$OLD_VERSION_EXISTS" -eq 1 ]; then
      if [ -f "$VERSION_BACKUP" ]; then cp "$VERSION_BACKUP" "$VERSION_FILE"; fi
    else rm -f "$VERSION_FILE"; fi
    if [ "$OLD_MANAGER_EXISTS" -eq 1 ]; then
      if [ -f "$MANAGER_BACKUP" ]; then cp "$MANAGER_BACKUP" "$MANAGER"; fi
    else rm -f "$MANAGER"; fi
    if [ "$OLD_MANIFEST_EXISTS" -eq 1 ]; then
      if [ -f "$MANIFEST_BACKUP" ]; then cp "$MANIFEST_BACKUP" "$MANIFEST"; fi
    else rm -f "$MANIFEST"; fi
    rm -rf "$stage" "$VERSION_BACKUP" "$MANAGER_BACKUP" "$MANIFEST_BACKUP" "$JOURNAL"
  }
  trap 'rollback; exit 1' EXIT HUP INT TERM
  # Keep the reversible transaction indivisible; EXIT still invokes rollback on errors.
  trap '' HUP INT TERM
  printf '%s\n' 'prepared' > "$JOURNAL"
  [ -f "$VERSION_FILE" ] && OLD_VERSION_EXISTS=1
  [ -f "$MANAGER" ] && OLD_MANAGER_EXISTS=1
  [ -f "$MANIFEST" ] && OLD_MANIFEST_EXISTS=1
  if [ "$OLD_VERSION_EXISTS" -eq 1 ]; then cp "$VERSION_FILE" "$VERSION_BACKUP" || fail "cannot journal VERSION"; fi
  if [ "$OLD_MANAGER_EXISTS" -eq 1 ]; then cp "$MANAGER" "$MANAGER_BACKUP" || fail "cannot journal manager"; fi
  if [ "$OLD_MANIFEST_EXISTS" -eq 1 ]; then cp "$MANIFEST" "$MANIFEST_BACKUP" || fail "cannot journal manifest"; fi
  if [ -d "$CACHE_DIR" ]; then
    mv "$CACHE_DIR" "$backup" || fail "cannot move existing cache"
    CACHE_MOVED=1
  fi
  [ -d "$CACHE_DIR" ] && fail "cannot move existing cache"
  mv "$stage/skills" "$CACHE_DIR" || fail "cannot activate skill cache"
  CACHE_ACTIVATED=1
  printf '%s\n' 'cache-activated' >> "$JOURNAL"

  # Remove only exact, recorded links for skills deleted from the release.
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    skill=$(field "$line" skill); path=$(field "$line" path); target=$(field "$line" target)
    case " $SKILL_NAMES " in *" $skill "*) continue ;; esac
    if [ -L "$path" ]; then rm -f "$path"; REMOVED_LINKS="$REMOVED_LINKS$(printf '%s\t%s' "$path" "$target")
"; fi
  done
  IFS=$oldIFS

  oldIFS=$IFS; IFS=$'\n'
  for record in $REG_LINES; do
    [ -n "$record" ] || continue
    dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
    mkdir -p "$dest" || fail "cannot create skills directory: $dest"
    for skill_dir in "$SOURCE_DIR/skills"/*; do
      [ -d "$skill_dir" ] || continue
      skill=$(basename "$skill_dir"); path="$dest/$skill"; target="$CACHE_DIR/$skill"
      if [ -L "$path" ]; then
        actual=$(readlink "$path")
        [ "$actual" = "$target" ] || { oldline=$(old_link_for_path "$path"); oldtarget=$(field "$oldline" target); [ -n "$oldline" ] && [ "$actual" = "$oldtarget" ] || fail "refusing to repoint unmanaged link: $path"; }
      elif [ ! -e "$path" ]; then
        ln -s "$target" "$path" || fail "cannot create link: $path"
        CREATED_LINKS="$CREATED_LINKS$path
"
      else
        fail "refusing to overwrite unmanaged path: $path"
      fi
    done
  done
  IFS=$oldIFS
  printf '%s\n' 'links-updated' >> "$JOURNAL"

  cp "$SOURCE_DIR/VERSION" "$VERSION_FILE.tmp.$$" || fail "cannot stage VERSION"
  mv "$VERSION_FILE.tmp.$$" "$VERSION_FILE" || fail "cannot install VERSION"
  write_manager
  printf '%s\n' 'manager-updated' >> "$JOURNAL"
  write_manifest "$MANIFEST"
  printf '%s\n' 'manifest-updated' >> "$JOURNAL"
  # All live state is committed; cleanup must never re-enter rollback.
  ROLLED_BACK=1
  trap - EXIT HUP INT TERM
  if ! rm -rf "$backup" "$stage" "$VERSION_BACKUP" "$MANAGER_BACKUP" "$MANIFEST_BACKUP" "$JOURNAL"; then
    printf 'ddd-workflow-kit: warning: cleanup left temporary transaction files behind\n' >&2
  fi
  say "Installed DDD Workflow Kit $VERSION."
  say "Manager: $MANAGER"
}

ORIGINAL_ARGS=( "$@" )
SOURCE_DIR=""; UPDATE=0; SELECTED_AGENTS=""; SCOPE=""; PROJECT_ROOT=""; EXPLICIT_PATH=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent) [ "$#" -ge 2 ] || fail "--agent requires a value"; add_agent "$2"; shift 2 ;;
    --global) [ -z "$SCOPE" ] || fail "choose only one scope"; SCOPE=global; shift ;;
    --project) [ -z "$SCOPE" ] || fail "choose only one scope"; SCOPE=project; if [ "$#" -ge 2 ] && [ "${2#--}" = "$2" ]; then PROJECT_ROOT=$2; shift 2; else PROJECT_ROOT=$PWD; shift; fi ;;
    --path) [ "$#" -ge 2 ] || fail "--path requires a path"; [ -z "$SCOPE" ] || fail "choose only one scope"; SCOPE=path; EXPLICIT_PATH=$2; shift 2 ;;
    --update) UPDATE=1; shift ;;
    --source-dir) [ "$#" -ge 2 ] || fail "--source-dir requires a path"; SOURCE_DIR=$2; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) fail "unknown option: $1" ;;
  esac
done

if [ -z "$SOURCE_DIR" ]; then
  # The raw curl entry point is only a bootstrap; all state changes run through
  # the versioned installer shipped in the checksum-verified release bundle.
  prepare_download_source
  if bash "$SOURCE_DIR/install.sh" --source-dir "$SOURCE_DIR" "${ORIGINAL_ARGS[@]}"; then
    exit 0
  else
    exit $?
  fi
fi

[ -d "$SOURCE_DIR" ] || fail "source directory does not exist: $SOURCE_DIR"
if [ -z "$SELECTED_AGENTS" ] || [ -z "$SCOPE" ]; then
  if [ "$UPDATE" -eq 1 ]; then :; else prompt_selection; fi
fi
install_release
