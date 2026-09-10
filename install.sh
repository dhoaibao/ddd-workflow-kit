#!/usr/bin/env bash
# DDD_WORKFLOW_KIT_INSTALLER
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
INSTALLER="$STATE_DIR/bin/install.sh"

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
  --skill NAME[,NAME...]   Select packages to link, or 'all'; default is every
                           document-class package (see PACKAGES)
  --update                 Refresh every registration in the existing manifest
  --source-dir PATH        Use a local release directory (maintainer/testing)
  --help                   Show this help

Uninstall options:
  uninstall --full --yes
  uninstall --partial --agent NAME[,NAME...] --global|--project [PATH]|--path PATH --yes

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
  if [ -z "${SELECTOR_FD:-}" ]; then
    exec 3<>"$SELECTOR_TTY" || fail "could not open interactive terminal"
    SELECTOR_FD=3
  fi
  SELECTOR_STTY_STATE=$(stty -g <"$SELECTOR_TTY") || fail "could not inspect terminal settings"
  SELECTOR_ACTIVE=1
  trap 'selector_restore' EXIT
  trap 'selector_interrupt' HUP INT TERM
  stty -icanon -echo min 1 time 0 <"$SELECTOR_TTY" || fail "could not configure interactive terminal"
  printf '\033[?25l' >"$SELECTOR_TTY"
}

selector_reset() {
  SELECTOR_COUNT=0
  SELECTOR_CURSOR=1
  SELECTOR_DRAWN=0
  SELECTOR_MULTI=0
  SELECTOR_LABELS=()
  SELECTOR_VALUES=()
  SELECTOR_SELECTED=()
}

selector_add_option() {
  SELECTOR_COUNT=$((SELECTOR_COUNT + 1))
  SELECTOR_LABELS[SELECTOR_COUNT]=$1
  SELECTOR_VALUES[SELECTOR_COUNT]=$2
  SELECTOR_SELECTED[SELECTOR_COUNT]=0
}

selector_value() {
  printf '%s' "${SELECTOR_VALUES[$1]}"
}

selector_label() {
  printf '%s' "${SELECTOR_LABELS[$1]}"
}

selector_selected() {
  [ "${SELECTOR_SELECTED[$1]:-0}" -eq 1 ]
}

selector_toggle() {
  [ "$SELECTOR_MULTI" -eq 1 ] || return 0
  SELECTOR_SELECTED[$1]=$((1 - ${SELECTOR_SELECTED[$1]:-0}))
}

selector_draw() {
  if [ "${SELECTOR_DRAWN:-0}" -eq 1 ]; then
    printf '\033[%sA' "$SELECTOR_LINES" >"$SELECTOR_TTY"
  fi
  printf '\033[2K\rSelect %s (↑/↓ move, %s, Enter confirm):\n' \
    "$SELECTOR_TITLE" "$SELECTOR_ACTION" >"$SELECTOR_TTY"
  printf '\033[2K\r%s\n' "$SELECTOR_HINT" >"$SELECTOR_TTY"
  index=1
  while [ "$index" -le "$SELECTOR_COUNT" ]; do
    cursor=' '
    [ "$index" -eq "$SELECTOR_CURSOR" ] && cursor='>'
    if [ "$SELECTOR_MULTI" -eq 1 ]; then
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
  IFS= read -r -n 1 -u "$SELECTOR_FD" key || return 1
  case "$key" in
    '') SELECTOR_EVENT=enter ;;
    ' ') SELECTOR_EVENT=space ;;
    q|Q) SELECTOR_EVENT=cancel ;;
    *)
      [ "$key" = "$(printf '\033')" ] || return 0
      next=''
      IFS= read -r -n 1 -t 1 -u "$SELECTOR_FD" next || return 0
      case "$next" in
        '['|'O')
          IFS= read -r -n 1 -t 1 -u "$SELECTOR_FD" next || return 0
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
  selector_reset
  SELECTOR_TITLE='agents'
  SELECTOR_ACTION='Space toggles'
  SELECTOR_HINT='Space toggles targets; Shared agents is the common .agents/skills target.'
  SELECTOR_MULTI=1
  selector_add_option 'Shared agents (.agents/skills)' shared
  selector_add_option 'Claude' claude
  selector_add_option 'Codex' codex
  selector_add_option 'OpenCode' opencode
  selector_add_option 'Antigravity' antigravity
  selector_add_option 'Pi' pi
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
  selector_reset
  SELECTOR_TITLE='scope'
  SELECTOR_ACTION='Arrow keys choose'
  SELECTOR_HINT='Choose one scope; project path is requested after confirmation.'
  selector_add_option 'Global (~/.agents/skills or agent default)' global
  selector_add_option 'Project (a project-local skills directory)' project
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

interactive_line_interrupt() {
  stty "$SELECTOR_STTY_STATE" <"$SELECTOR_TTY" 2>/dev/null || :
  printf '\033[?25h\033[0m' >"$SELECTOR_TTY" 2>/dev/null || :
  exit 130
}

interactive_read_line() {
  variable=$1
  if [ -z "${SELECTOR_FD:-}" ]; then
    case "$variable" in
      PROJECT_ROOT) IFS= read -r PROJECT_ROOT < /dev/tty ;;
      UNINSTALL_FILTER_ROOT) IFS= read -r UNINSTALL_FILTER_ROOT < /dev/tty ;;
      *) return 1 ;;
    esac
    return
  fi
  trap 'interactive_line_interrupt' HUP INT TERM
  stty -icanon echo min 1 time 0 <"$SELECTOR_TTY" || { trap - HUP INT TERM; return 1; }
  value=''
  while :; do
    character=''
    if ! IFS= read -r -n 1 -u "$SELECTOR_FD" character; then
      stty "$SELECTOR_STTY_STATE" <"$SELECTOR_TTY" 2>/dev/null || :
      return 1
    fi
    [ -n "$character" ] || break
    value="$value$character"
  done
  stty "$SELECTOR_STTY_STATE" <"$SELECTOR_TTY" 2>/dev/null || { trap - HUP INT TERM; return 1; }
  trap - HUP INT TERM
  case "$variable" in
    PROJECT_ROOT) PROJECT_ROOT=$value ;;
    UNINSTALL_FILTER_ROOT) UNINSTALL_FILTER_ROOT=$value ;;
    *) return 1 ;;
  esac
}

normalize_explicit_path() {
  [ -n "$EXPLICIT_PATH" ] || fail '--path requires a non-empty path'
  case "$EXPLICIT_PATH" in
    /*) ;;
    *) EXPLICIT_PATH="$PWD/$EXPLICIT_PATH" ;;
  esac
}

interactive_close() {
  if [ -n "${SELECTOR_FD:-}" ]; then
    exec 3>&-
    SELECTOR_FD=''
  fi
}

prompt_skills() {
  previous_extra=$(previous_implementation_selection)
  selector_reset
  SELECTOR_TITLE='optional packages'
  SELECTOR_ACTION='Space toggles'
  SELECTOR_HINT='Space toggles optional implementation packages; document packages install by default.'
  SELECTOR_MULTI=1
  oldIFS=$IFS; IFS=' '
  for name in $IMPLEMENTATION_SKILL_NAMES; do
    [ -n "$name" ] || continue
    selector_add_option "$(package_label "$name")" "$name"
  done
  IFS=$oldIFS
  # Pre-check packages already selected in a prior install/update so that
  # accepting the default does not silently drop them.
  index=1
  while [ "$index" -le "$SELECTOR_COUNT" ]; do
    case " $previous_extra " in *" $(selector_value "$index") "*) selector_toggle "$index" ;; esac
    index=$((index + 1))
  done
  selector_begin /dev/tty
  selector_draw
  while :; do
    selector_read_event || { selector_restore; fail 'could not read package selection'; }
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
  SELECTED_IMPL_FROM_PROMPT=''
  index=1
  while [ "$index" -le "$SELECTOR_COUNT" ]; do
    if selector_selected "$index"; then
      SELECTED_IMPL_FROM_PROMPT="$SELECTED_IMPL_FROM_PROMPT $(selector_value "$index")"
    fi
    index=$((index + 1))
  done
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
      interactive_read_line PROJECT_ROOT || fail 'could not read project path'
      [ -n "$PROJECT_ROOT" ] || PROJECT_ROOT=$PWD
      ;;
    *) fail 'internal: invalid scope' ;;
  esac
  SELECTED_IMPL_FROM_PROMPT=''
  PROMPT_SKILLS_RAN=0
  if [ -n "$IMPLEMENTATION_SKILL_NAMES" ]; then
    prompt_skills
    PROMPT_SKILLS_RAN=1
  fi
  interactive_close
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
      install.sh|VERSION|PACKAGES|skills|skills/*) : ;;
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
  [ -f "$extract/install.sh" ] && [ -f "$extract/VERSION" ] && [ -f "$extract/PACKAGES" ] && [ -d "$extract/skills" ] || fail "release archive is missing required files"
  SOURCE_DIR=$extract
}

# Parses the release's PACKAGES manifest (name<TAB>class<TAB>label) into
# PACKAGE_LINES plus the DOCUMENT_SKILL_NAMES/IMPLEMENTATION_SKILL_NAMES
# selection groups. Rows naming a package with no matching skills/ directory
# are ignored here; scripts/validate-skills.py enforces the exact 1:1 match.
load_package_classes() {
  packages_file="$1/PACKAGES"
  PACKAGE_LINES=""
  DOCUMENT_SKILL_NAMES=""
  IMPLEMENTATION_SKILL_NAMES=""
  while IFS= read -r line || [ -n "$line" ]; do
    [ -n "$line" ] || continue
    name=$(printf '%s' "$line" | awk -F '\t' '{print $1}')
    class=$(printf '%s' "$line" | awk -F '\t' '{print $2}')
    label=$(printf '%s' "$line" | awk -F '\t' '{print $3}')
    [ -n "$name" ] && [ -n "$class" ] || fail "PACKAGES manifest has an invalid row: $line"
    case " $SKILL_NAMES " in *" $name "*) : ;; *) continue ;; esac
    PACKAGE_LINES="$PACKAGE_LINES$(printf '%s\t%s\t%s' "$name" "$class" "$label")
"
    case "$class" in
      document) DOCUMENT_SKILL_NAMES="$DOCUMENT_SKILL_NAMES $name" ;;
      implementation) IMPLEMENTATION_SKILL_NAMES="$IMPLEMENTATION_SKILL_NAMES $name" ;;
      *) fail "PACKAGES manifest has an unknown class for $name: $class" ;;
    esac
  done < "$packages_file"
  [ -n "$DOCUMENT_SKILL_NAMES" ] || fail "PACKAGES manifest names no document-class package"
}

package_label() {
  wanted=$1
  oldIFS=$IFS; IFS=$'\n'
  for line in $PACKAGE_LINES; do
    [ -n "$line" ] || continue
    name=$(printf '%s' "$line" | awk -F '\t' '{print $1}')
    [ "$name" = "$wanted" ] || continue
    printf '%s' "$line" | awk -F '\t' '{print $3}'
    IFS=$oldIFS
    return 0
  done
  IFS=$oldIFS
  printf '%s' "$wanted"
}

# Names the implementation-class packages selected by an existing manifest,
# if any. Used so a fresh, non-interactive install that only names an agent
# (no --skill) does not silently drop a previously opted-in optional
# package from unrelated destinations, and so the interactive prompt starts
# with previously-selected optional packages pre-checked.
previous_implementation_selection() {
  result=""
  if [ -f "$MANIFEST" ]; then
    previous=$(manifest_header_field skills)
    if [ -n "$previous" ]; then
      oldIFS=$IFS; IFS=','
      # shellcheck disable=SC2086
      set -- $previous
      IFS=$oldIFS
      for name in "$@"; do
        [ -n "$name" ] || continue
        case " $IMPLEMENTATION_SKILL_NAMES " in *" $name "*) : ;; *) continue ;; esac
        case " $result " in *" $name "*) continue ;; esac
        result="$result $name"
      done
    fi
  fi
  printf '%s' "$result"
}

validate_source() {
  [ -d "$1/skills" ] || fail "source has no skills directory: $1"
  [ -f "$1/VERSION" ] || fail "source has no VERSION file: $1"
  [ -f "$1/install.sh" ] || fail "source has no install.sh: $1"
  [ -f "$1/PACKAGES" ] || fail "source has no PACKAGES manifest: $1"
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
  load_package_classes "$1"
}

# Read one compact manifest object. The manifest is generated by this script;
# fields deliberately disallow quotes/backslashes so this remains Bash 3.2-safe.
field() {
  line=$1; key=$2
  printf '%s\n' "$line" | sed -n "s/.*\"$key\":\"\([^\"]*\)\".*/\1/p"
}

load_old_links() {
  OLD_LINK_LINES=""
  OLD_LINK_COUNT=0
  [ -f "$MANIFEST" ] || return 0
  while IFS= read -r line; do
    case "$line" in
      *'"skill":"'*)
        path=$(field "$line" path)
        case "$path" in
          /*) ;;
          *) fail "manifest contains a relative link path; refusing cleanup: $path" ;;
        esac
        OLD_LINK_LINES="$OLD_LINK_LINES$line
"
        OLD_LINK_COUNT=$((OLD_LINK_COUNT + 1))
        ;;
    esac
  done < "$MANIFEST"
}

load_old_registrations() {
  OLD_REGISTRATION_LINES=""
  [ -f "$MANIFEST" ] || return 0
  while IFS= read -r line; do
    case "$line" in
      *'"agent":"'*)
        case "$line" in *'"skill":"'*) continue ;; esac
        agent=$(field "$line" agent)
        scope=$(field "$line" scope)
        root=$(field "$line" project_root)
        dest=$(field "$line" path)
        [ -n "$agent" ] && [ -n "$scope" ] && [ -n "$dest" ] || fail 'manifest contains an invalid registration'
        case "$dest" in
          /*) ;;
          *) fail "manifest contains a relative registration path; refusing cleanup: $dest" ;;
        esac
        OLD_REGISTRATION_LINES="$OLD_REGISTRATION_LINES$(printf '%s\t%s\t%s\t%s' "$agent" "$scope" "$root" "$dest")
"
        ;;
    esac
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
  if [ -n "${OLD_REGISTRATION_LINES:-}" ]; then
    oldIFS=$IFS; IFS=$'\n'
    for record in $OLD_REGISTRATION_LINES; do
      [ -n "$record" ] || continue
      agent=$(printf '%s' "$record" | awk -F '\t' '{print $1}')
      scope=$(printf '%s' "$record" | awk -F '\t' '{print $2}')
      root=$(printf '%s' "$record" | awk -F '\t' '{print $3}')
      dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
      key="$agent|$scope|$root|$dest"
      case " $SEEN_REG_KEYS " in *" $key "*) continue ;; esac
      SEEN_REG_KEYS="$SEEN_REG_KEYS $key"
      add_registration "$agent" "$scope" "$root" "$dest"
    done
    IFS=$oldIFS
    return 0
  fi
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
    case " $SELECTED_SKILLS " in *" $skill "*) continue ;; esac
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
    skillIFS=$IFS; IFS=' '
    for skill in $SELECTED_SKILLS; do
      [ -n "$skill" ] || continue
      path="$dest/$skill"
      if [ -e "$path" ] || [ -L "$path" ]; then
        [ -L "$path" ] || fail "refusing to overwrite unmanaged path: $path"
        actual=$(readlink "$path") || fail "cannot inspect existing link: $path"
        oldline=$(old_link_for_path "$path")
        oldtarget=$(field "$oldline" target)
        [ -n "$oldline" ] && [ "$actual" = "$oldtarget" ] || fail "refusing to repoint unmanaged or repointed link: $path"
      fi
    done
    IFS=$skillIFS
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

join_comma() {
  result=""
  for item in $1; do
    [ -n "$item" ] || continue
    [ -n "$result" ] && result="$result,$item" || result=$item
  done
  printf '%s' "$result"
}

write_manifest() {
  destination=$1
  tmp="$destination.tmp.$$"
  skills_csv=$(join_comma "$SELECTED_SKILLS")
  {
    printf '{\n  "schema": 1,\n  "version": "%s",\n  "source": "%s",\n  "skills": "%s",\n  "registrations": [\n' "$(json_escape "$VERSION")" "$(json_escape "$SOURCE_URL")" "$(json_escape "$skills_csv")"
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
      skillIFS=$IFS; IFS=' '
      for skill in $SELECTED_SKILLS; do
        [ -n "$skill" ] || continue
        path="$dest/$skill"; target="$CACHE_DIR/$skill"
        [ "$first" -eq 1 ] || printf ',\n'; first=0
        printf '    {"agent":"%s","scope":"%s","project_root":"%s","skill":"%s","path":"%s","target":"%s"}' "$(json_escape "$agents")" "$(json_escape "$scope")" "$(json_escape "$root")" "$(json_escape "$skill")" "$(json_escape "$path")" "$(json_escape "$target")"
      done
      IFS=$skillIFS
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
INSTALLER="\${STATE_DIR}/bin/install.sh"
RELEASE_URL="${RELEASE_URL_DEFAULT}"
CHECKSUM_URL="${CHECKSUM_URL_DEFAULT}"
fetch() { command -v curl >/dev/null 2>&1 || { echo "ddd-workflow-kit: curl is required" >&2; exit 1; }; curl -fsSL "\$1" -o "\$2" || exit 1; }
sha256() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "\$1" | awk '{print \$1}'; else shasum -a 256 "\$1" | awk '{print \$1}'; fi; }
validate_archive() {
  listing=\$(tar -tzf "\$1") || exit 1
  while IFS= read -r entry; do
    case "\$entry" in
      /*|../*|*/../*|*/..|.*|*/./*|*/.|*/.*) echo "ddd-workflow-kit: unsafe release archive entry: \$entry" >&2; exit 1 ;;
      install.sh|VERSION|PACKAGES|skills|skills/*) : ;;
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
  uninstall) shift; [ -f "\$INSTALLER" ] || { echo "ddd-workflow-kit: cached installer is missing; run update first" >&2; exit 1; }; exec bash "\$INSTALLER" uninstall "\$@" ;;
  version|--version) cat "\$STATE_DIR/VERSION" ;;
  *) echo "Usage: ddd-workflow-kit {install|update|uninstall|version}" >&2; exit 2 ;;
esac
EOF
  chmod 755 "$tmp" || fail "cannot chmod manager"
  mv "$tmp" "$MANAGER" || fail "cannot install manager"
}

write_cached_installer() {
  tmp="$INSTALLER.tmp.$$"
  cp "$SOURCE_DIR/install.sh" "$tmp" || fail "cannot stage cached installer"
  chmod 755 "$tmp" || fail "cannot chmod cached installer"
  mv "$tmp" "$INSTALLER" || fail "cannot install cached installer"
}

build_selected_skills_from_arg() {
  SELECTED_SKILLS=""
  if [ "$SKILL_ARG" = all ]; then
    SELECTED_SKILLS=$SKILL_NAMES
    return
  fi
  oldIFS=$IFS; IFS=','
  # shellcheck disable=SC2086
  set -- $SKILL_ARG
  IFS=$oldIFS
  for name in "$@"; do
    [ -n "$name" ] || continue
    case " $SKILL_NAMES " in *" $name "*) : ;; *) fail "unknown --skill package: $name" ;; esac
    case " $SELECTED_SKILLS " in *" $name "*) continue ;; esac
    SELECTED_SKILLS="$SELECTED_SKILLS $name"
  done
}

# Every document-class package is always part of the selection; --skill and
# the interactive prompt only add or remove optional implementation-class
# packages on top of that baseline.
ensure_document_baseline() {
  for name in $DOCUMENT_SKILL_NAMES; do
    [ -n "$name" ] || continue
    case " $SELECTED_SKILLS " in *" $name "*) continue ;; esac
    SELECTED_SKILLS="$SELECTED_SKILLS $name"
  done
}

# Resolves which skills get symlinked this run. Explicit --skill always wins
# and replaces any previously-selected optional packages; otherwise an
# update preserves the manifest's prior selection (falling back to every
# previously-linked skill for a manifest written before package classes
# existed); a fresh interactive install adds any optional implementation
# packages chosen in the prompt; anything else defaults to every
# document-class package. Document-class packages are never deselectable.
resolve_selected_skills() {
  if [ -n "$SKILL_ARG" ]; then
    build_selected_skills_from_arg
    ensure_document_baseline
    return
  fi
  if [ "$UPDATE" -eq 1 ]; then
    [ -f "$MANIFEST" ] || fail "cannot update before an install"
    previous=$(manifest_header_field skills)
    SELECTED_SKILLS=""
    if [ -n "$previous" ]; then
      oldIFS=$IFS; IFS=','
      # shellcheck disable=SC2086
      set -- $previous
      IFS=$oldIFS
      for name in "$@"; do
        [ -n "$name" ] || continue
        case " $SKILL_NAMES " in *" $name "*) : ;; *) continue ;; esac
        case " $SELECTED_SKILLS " in *" $name "*) continue ;; esac
        SELECTED_SKILLS="$SELECTED_SKILLS $name"
      done
    else
      oldIFS=$IFS; IFS=$'\n'
      for line in $OLD_LINK_LINES; do
        [ -n "$line" ] || continue
        skill=$(field "$line" skill)
        case " $SKILL_NAMES " in *" $skill "*) : ;; *) continue ;; esac
        case " $SELECTED_SKILLS " in *" $skill "*) continue ;; esac
        SELECTED_SKILLS="$SELECTED_SKILLS $skill"
      done
      IFS=$oldIFS
    fi
    ensure_document_baseline
    return
  fi
  SELECTED_SKILLS="$DOCUMENT_SKILL_NAMES"
  if [ "$PROMPT_SKILLS_RAN" -eq 1 ]; then
    SELECTED_SKILLS="$SELECTED_SKILLS${SELECTED_IMPL_FROM_PROMPT:-}"
  else
    previous_extra=$(previous_implementation_selection)
    [ -z "$previous_extra" ] || SELECTED_SKILLS="$SELECTED_SKILLS $previous_extra"
  fi
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
  if [ -e "$INSTALLER" ] || [ -L "$INSTALLER" ]; then
    if [ ! -f "$INSTALLER" ] || ! awk 'NR == 2 { found=($0 == "# DDD_WORKFLOW_KIT_INSTALLER") } END { exit (found ? 0 : 1) }' "$INSTALLER"; then
      fail "refusing to overwrite unmanaged installer: $INSTALLER"
    fi
  fi
  if [ -d "$CACHE_DIR" ] && [ ! -f "$MANIFEST" ]; then
    fail "refusing to overwrite unmanaged cache: $CACHE_DIR"
  fi
  SOURCE_URL=${DDD_SOURCE_URL:-${DDD_RELEASE_URL:-$RELEASE_URL_DEFAULT}}
  load_old_links
  load_old_registrations
  resolve_selected_skills
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
  INSTALLER_BACKUP="$STATE_DIR/.installer-backup.$$"
  MANIFEST_BACKUP="$STATE_DIR/.manifest-backup.$$"
  OLD_VERSION_EXISTS=0; OLD_MANAGER_EXISTS=0; OLD_INSTALLER_EXISTS=0; OLD_MANIFEST_EXISTS=0
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
    if [ "$OLD_INSTALLER_EXISTS" -eq 1 ]; then
      if [ -f "$INSTALLER_BACKUP" ]; then cp "$INSTALLER_BACKUP" "$INSTALLER"; fi
    else rm -f "$INSTALLER"; fi
    if [ "$OLD_MANIFEST_EXISTS" -eq 1 ]; then
      if [ -f "$MANIFEST_BACKUP" ]; then cp "$MANIFEST_BACKUP" "$MANIFEST"; fi
    else rm -f "$MANIFEST"; fi
    rm -rf "$stage" "$VERSION_BACKUP" "$MANAGER_BACKUP" "$INSTALLER_BACKUP" "$MANIFEST_BACKUP" "$JOURNAL"
  }
  trap 'rollback; exit 1' EXIT HUP INT TERM
  # Keep the reversible transaction indivisible; EXIT still invokes rollback on errors.
  trap '' HUP INT TERM
  printf '%s\n' 'prepared' > "$JOURNAL"
  [ -f "$VERSION_FILE" ] && OLD_VERSION_EXISTS=1
  [ -f "$MANAGER" ] && OLD_MANAGER_EXISTS=1
  [ -f "$INSTALLER" ] && OLD_INSTALLER_EXISTS=1
  [ -f "$MANIFEST" ] && OLD_MANIFEST_EXISTS=1
  if [ "$OLD_VERSION_EXISTS" -eq 1 ]; then cp "$VERSION_FILE" "$VERSION_BACKUP" || fail "cannot journal VERSION"; fi
  if [ "$OLD_MANAGER_EXISTS" -eq 1 ]; then cp "$MANAGER" "$MANAGER_BACKUP" || fail "cannot journal manager"; fi
  if [ "$OLD_INSTALLER_EXISTS" -eq 1 ]; then cp "$INSTALLER" "$INSTALLER_BACKUP" || fail "cannot journal installer"; fi
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
    case " $SELECTED_SKILLS " in *" $skill "*) continue ;; esac
    if [ -L "$path" ]; then rm -f "$path"; REMOVED_LINKS="$REMOVED_LINKS$(printf '%s\t%s' "$path" "$target")
"; fi
  done
  IFS=$oldIFS

  oldIFS=$IFS; IFS=$'\n'
  for record in $REG_LINES; do
    [ -n "$record" ] || continue
    dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
    mkdir -p "$dest" || fail "cannot create skills directory: $dest"
    skillIFS=$IFS; IFS=' '
    for skill in $SELECTED_SKILLS; do
      [ -n "$skill" ] || continue
      path="$dest/$skill"; target="$CACHE_DIR/$skill"
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
    IFS=$skillIFS
  done
  IFS=$oldIFS
  printf '%s\n' 'links-updated' >> "$JOURNAL"

  cp "$SOURCE_DIR/VERSION" "$VERSION_FILE.tmp.$$" || fail "cannot stage VERSION"
  mv "$VERSION_FILE.tmp.$$" "$VERSION_FILE" || fail "cannot install VERSION"
  write_cached_installer
  printf '%s\n' 'installer-updated' >> "$JOURNAL"
  write_manager
  printf '%s\n' 'manager-updated' >> "$JOURNAL"
  write_manifest "$MANIFEST"
  printf '%s\n' 'manifest-updated' >> "$JOURNAL"
  # All live state is committed; cleanup must never re-enter rollback.
  ROLLED_BACK=1
  trap - EXIT HUP INT TERM
  if ! rm -rf "$backup" "$stage" "$VERSION_BACKUP" "$MANAGER_BACKUP" "$INSTALLER_BACKUP" "$MANIFEST_BACKUP" "$JOURNAL"; then
    printf 'ddd-workflow-kit: warning: cleanup left temporary transaction files behind\n' >&2
  fi
  say "Installed DDD Workflow Kit $VERSION."
  say "Manager: $MANAGER"
}

manifest_header_field() {
  key=$1
  sed -n "s/.*\"$key\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" "$MANIFEST" | awk 'NR == 1 { print; exit }'
}

load_uninstall_registrations() {
  [ -f "$MANIFEST" ] || fail "nothing to uninstall: manifest is missing"
  UNINSTALL_REG_COUNT=0
  UNINSTALL_REG_AGENT=()
  UNINSTALL_REG_SCOPE=()
  UNINSTALL_REG_ROOT=()
  UNINSTALL_REG_DEST=()
  while IFS= read -r line; do
    case "$line" in
      *'"agent":"'*)
        case "$line" in *'"skill":"'*) continue ;; esac
        agent=$(field "$line" agent)
        scope=$(field "$line" scope)
        root=$(field "$line" project_root)
        dest=$(field "$line" path)
        [ -n "$agent" ] && [ -n "$scope" ] && [ -n "$dest" ] || fail "manifest contains an invalid registration"
        case "$dest" in
          /*) ;;
          *) fail "manifest contains a relative registration path; refusing cleanup: $dest" ;;
        esac
        UNINSTALL_REG_COUNT=$((UNINSTALL_REG_COUNT + 1))
        UNINSTALL_REG_AGENT[UNINSTALL_REG_COUNT]=$agent
        UNINSTALL_REG_SCOPE[UNINSTALL_REG_COUNT]=$scope
        UNINSTALL_REG_ROOT[UNINSTALL_REG_COUNT]=$root
        UNINSTALL_REG_DEST[UNINSTALL_REG_COUNT]=$dest
        ;;
    esac
  done < "$MANIFEST"
  UNINSTALL_SELECTED=()
  UNINSTALL_REMAINING_REG_LINES=''
  index=1
  while [ "$index" -le "$UNINSTALL_REG_COUNT" ]; do
    UNINSTALL_SELECTED[index]=0
    index=$((index + 1))
  done
}

uninstall_registration_matches() {
  index=$1
  agent=${UNINSTALL_REG_AGENT[$index]}
  scope=${UNINSTALL_REG_SCOPE[$index]}
  root=${UNINSTALL_REG_ROOT[$index]}
  dest=${UNINSTALL_REG_DEST[$index]}
  if [ -n "$UNINSTALL_AGENTS" ]; then
    case " $UNINSTALL_AGENTS " in *" $agent "*) : ;; *) return 1 ;; esac
  fi
  case "$UNINSTALL_FILTER_SCOPE" in
    '') ;;
    global) [ "$scope" = global ] || return 1 ;;
    project)
      if [ "$scope" = project ]; then
        if [ "${UNINSTALL_FILTER_ALL_PROJECT:-0}" -eq 1 ]; then :; else
          [ "$root" = "$UNINSTALL_FILTER_ROOT" ] || return 1
        fi
      elif [ "$scope" = path ] && [ "${UNINSTALL_FILTER_INCLUDE_PATH:-0}" -eq 1 ]; then
        :
      else
        return 1
      fi
      ;;
    path) [ "$scope" = path ] && [ "$dest" = "$UNINSTALL_FILTER_DEST" ] || return 1 ;;
    *) return 1 ;;
  esac
}

uninstall_registration_label() {
  index=$1
  agent=${UNINSTALL_REG_AGENT[$index]}
  scope=${UNINSTALL_REG_SCOPE[$index]}
  root=${UNINSTALL_REG_ROOT[$index]}
  dest=${UNINSTALL_REG_DEST[$index]}
  case "$scope" in
    global) printf '%s - global: %s' "$agent" "$dest" ;;
    project) printf '%s - project: %s' "$agent" "$root" ;;
    path) printf '%s - explicit path: %s' "$agent" "$dest" ;;
    *) printf '%s - %s: %s' "$agent" "$scope" "$dest" ;;
  esac
}

selector_run_single() {
  selector_begin /dev/tty
  selector_draw
  while :; do
    selector_read_event || { selector_restore; fail 'could not read interactive selection'; }
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
  SELECTOR_RESULT=$(selector_value "$SELECTOR_CURSOR")
}

prompt_uninstall_mode() {
  selector_reset
  SELECTOR_TITLE='uninstall mode'
  SELECTOR_ACTION='Arrow keys choose'
  SELECTOR_HINT='Full removes all registrations; Partial removes selected registrations.'
  selector_add_option 'Full uninstall' full
  selector_add_option 'Partial uninstall' partial
  selector_run_single
  UNINSTALL_MODE=$SELECTOR_RESULT
}

prompt_uninstall_scope() {
  selector_reset
  SELECTOR_TITLE='registration scope'
  SELECTOR_ACTION='Arrow keys choose'
  SELECTOR_HINT='Project includes all project and explicit-path registrations.'
  selector_add_option 'Global registrations' global
  selector_add_option 'Project registrations' project
  selector_run_single
  UNINSTALL_FILTER_SCOPE=$SELECTOR_RESULT
  if [ "$UNINSTALL_FILTER_SCOPE" = project ]; then
    UNINSTALL_FILTER_INCLUDE_PATH=1
    UNINSTALL_FILTER_ALL_PROJECT=1
  fi
}

prompt_uninstall_registrations() {
  selector_reset
  SELECTOR_TITLE='registrations'
  SELECTOR_ACTION='Space toggles'
  SELECTOR_HINT='Space toggles registrations; Enter confirms the selection.'
  SELECTOR_MULTI=1
  index=1
  while [ "$index" -le "$UNINSTALL_REG_COUNT" ]; do
    if uninstall_registration_matches "$index"; then
      selector_add_option "$(uninstall_registration_label "$index")" "$index"
    fi
    index=$((index + 1))
  done
  [ "$SELECTOR_COUNT" -gt 0 ] || fail 'no registrations match the selected scope'
  selector_begin /dev/tty
  selector_draw
  while :; do
    selector_read_event || { selector_restore; fail 'could not read registration selection'; }
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
  selected_count=0
  index=1
  while [ "$index" -le "$SELECTOR_COUNT" ]; do
    if selector_selected "$index"; then
      registration_index=$(selector_value "$index")
      UNINSTALL_SELECTED[registration_index]=1
      selected_count=$((selected_count + 1))
    fi
    index=$((index + 1))
  done
  [ "$selected_count" -gt 0 ] || fail 'select at least one registration'
}

uninstall_build_selected_from_filter() {
  UNINSTALL_SELECTED_COUNT=0
  index=1
  while [ "$index" -le "$UNINSTALL_REG_COUNT" ]; do
    if uninstall_registration_matches "$index"; then
      UNINSTALL_SELECTED[index]=1
      UNINSTALL_SELECTED_COUNT=$((UNINSTALL_SELECTED_COUNT + 1))
    fi
    index=$((index + 1))
  done
  [ "$UNINSTALL_SELECTED_COUNT" -gt 0 ] || fail 'no registrations match the requested selection'
}

uninstall_build_remaining() {
  UNINSTALL_REMAINING_REG_LINES=''
  index=1
  while [ "$index" -le "$UNINSTALL_REG_COUNT" ]; do
    if [ "${UNINSTALL_SELECTED[$index]:-0}" -eq 0 ]; then
      line=$(printf '%s\t%s\t%s\t%s' "${UNINSTALL_REG_AGENT[$index]}" "${UNINSTALL_REG_SCOPE[$index]}" "${UNINSTALL_REG_ROOT[$index]}" "${UNINSTALL_REG_DEST[$index]}")
      UNINSTALL_REMAINING_REG_LINES="$UNINSTALL_REMAINING_REG_LINES$line
"
    fi
    index=$((index + 1))
  done
}

uninstall_remaining_scope_root() {
  wanted=$1
  oldIFS=$IFS; IFS=$'\n'
  for record in $UNINSTALL_REMAINING_REG_LINES; do
    [ -n "$record" ] || continue
    dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
    [ "$dest" = "$wanted" ] || continue
    scope=$(printf '%s' "$record" | awk -F '\t' '{print $2}')
    root=$(printf '%s' "$record" | awk -F '\t' '{print $3}')
    printf '%s\t%s' "$scope" "$root"
    IFS=$oldIFS
    return 0
  done
  IFS=$oldIFS
  return 1
}

uninstall_remaining_agents() {
  wanted=$1
  result=''
  oldIFS=$IFS; IFS=$'\n'
  for record in $UNINSTALL_REMAINING_REG_LINES; do
    [ -n "$record" ] || continue
    dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
    [ "$dest" = "$wanted" ] || continue
    agent=$(printf '%s' "$record" | awk -F '\t' '{print $1}')
    [ -n "$result" ] && result="$result,$agent" || result=$agent
  done
  IFS=$oldIFS
  printf '%s' "$result"
}

uninstall_has_remaining_destination() {
  [ -n "$(uninstall_remaining_agents "$1")" ]
}

uninstall_preflight_links() {
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    path=$(field "$line" path)
    target=$(field "$line" target)
    dest=${path%/*}
    uninstall_has_remaining_destination "$dest" && continue
    if [ -e "$path" ] || [ -L "$path" ]; then
      [ -L "$path" ] || fail "refusing to remove unmanaged path: $path"
      actual=$(readlink "$path") || fail "cannot inspect recorded link: $path"
      [ "$actual" = "$target" ] || fail "recorded link was repointed; refusing uninstall: $path"
    fi
  done
  IFS=$oldIFS
}

uninstall_manifest_setup() {
  UNINSTALL_MANIFEST_VERSION=$(manifest_header_field version)
  UNINSTALL_MANIFEST_SOURCE=$(manifest_header_field source)
  UNINSTALL_MANIFEST_SKILLS=$(manifest_header_field skills)
  [ -n "$UNINSTALL_MANIFEST_VERSION" ] || fail 'manifest has no version'
  [ -n "$UNINSTALL_MANIFEST_SOURCE" ] || fail 'manifest has no source'
}

write_uninstall_manifest() {
  UNINSTALL_MANIFEST_TMP="$MANIFEST.tmp.$$"
  {
    printf '{\n  "schema": 1,\n  "version": "%s",\n  "source": "%s",\n  "skills": "%s",\n  "registrations": [\n' "$(json_escape "$UNINSTALL_MANIFEST_VERSION")" "$(json_escape "$UNINSTALL_MANIFEST_SOURCE")" "$(json_escape "$UNINSTALL_MANIFEST_SKILLS")"
    first=1
    oldIFS=$IFS; IFS=$'\n'
    for record in $UNINSTALL_REMAINING_REG_LINES; do
      [ -n "$record" ] || continue
      agent=$(printf '%s' "$record" | awk -F '\t' '{print $1}'); scope=$(printf '%s' "$record" | awk -F '\t' '{print $2}'); root=$(printf '%s' "$record" | awk -F '\t' '{print $3}'); dest=$(printf '%s' "$record" | awk -F '\t' '{print $4}')
      [ "$first" -eq 1 ] || printf ',\n'; first=0
      printf '    {"agent":"%s","scope":"%s","project_root":"%s","path":"%s"}' "$(json_escape "$agent")" "$(json_escape "$scope")" "$(json_escape "$root")" "$(json_escape "$dest")"
    done
    IFS=$oldIFS
    printf '\n  ],\n  "links": [\n'
    first=1
    oldIFS=$IFS; IFS=$'\n'
    for line in $OLD_LINK_LINES; do
      [ -n "$line" ] || continue
      path=$(field "$line" path); dest=${path%/*}
      agents=$(uninstall_remaining_agents "$dest")
      [ -n "$agents" ] || continue
      metadata=$(uninstall_remaining_scope_root "$dest") || continue
      scope=$(printf '%s' "$metadata" | awk -F '\t' '{print $1}')
      root=$(printf '%s' "$metadata" | awk -F '\t' '{print $2}')
      skill=$(field "$line" skill); target=$(field "$line" target)
      [ "$first" -eq 1 ] || printf ',\n'; first=0
      printf '    {"agent":"%s","scope":"%s","project_root":"%s","skill":"%s","path":"%s","target":"%s"}' "$(json_escape "$agents")" "$(json_escape "$scope")" "$(json_escape "$root")" "$(json_escape "$skill")" "$(json_escape "$path")" "$(json_escape "$target")"
    done
    IFS=$oldIFS
    printf '\n  ]\n}\n'
  } > "$UNINSTALL_MANIFEST_TMP" || { rm -f "$UNINSTALL_MANIFEST_TMP"; fail 'cannot write manifest'; }
  mv "$UNINSTALL_MANIFEST_TMP" "$MANIFEST" || { rm -f "$UNINSTALL_MANIFEST_TMP"; fail 'cannot install manifest'; }
  UNINSTALL_MANIFEST_TMP=''
}

uninstall_partial_rollback() {
  [ "${UNINSTALL_ROLLED_BACK:-0}" -eq 0 ] || return 0
  UNINSTALL_ROLLED_BACK=1
  oldIFS=$IFS; IFS=$'\n'
  for record in $UNINSTALL_REMOVED_LINKS; do
    [ -n "$record" ] || continue
    path=$(printf '%s' "$record" | awk -F '\t' '{print $1}'); target=$(printf '%s' "$record" | awk -F '\t' '{print $2}')
    [ -e "$path" ] || [ -L "$path" ] || ln -s "$target" "$path"
  done
  IFS=$oldIFS
  if [ -f "$UNINSTALL_MANIFEST_BACKUP" ]; then cp "$UNINSTALL_MANIFEST_BACKUP" "$MANIFEST"; fi
  [ -n "${UNINSTALL_MANIFEST_TMP:-}" ] && rm -f "$UNINSTALL_MANIFEST_TMP"
  rm -f "$UNINSTALL_MANIFEST_BACKUP"
}

uninstall_apply_partial() {
  uninstall_preflight_links
  UNINSTALL_MANIFEST_BACKUP="$STATE_DIR/.manifest-uninstall-backup.$$"
  cp "$MANIFEST" "$UNINSTALL_MANIFEST_BACKUP" || fail 'cannot backup manifest'
  UNINSTALL_REMOVED_LINKS=''
  UNINSTALL_ROLLED_BACK=0
  trap 'uninstall_partial_rollback; exit 1' EXIT HUP INT TERM
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    path=$(field "$line" path); target=$(field "$line" target); dest=${path%/*}
    uninstall_has_remaining_destination "$dest" && continue
    if [ -L "$path" ]; then
      rm -f "$path" || fail "cannot remove recorded link: $path"
      UNINSTALL_REMOVED_LINKS="$UNINSTALL_REMOVED_LINKS$(printf '%s\t%s' "$path" "$target")
"
    fi
  done
  IFS=$oldIFS
  write_uninstall_manifest
  UNINSTALL_ROLLED_BACK=1
  trap - EXIT HUP INT TERM
  rm -f "$UNINSTALL_MANIFEST_BACKUP"
  say 'Partial uninstall complete.'
}

uninstall_full_rollback() {
  [ "${UNINSTALL_ROLLED_BACK:-0}" -eq 0 ] || return 0
  UNINSTALL_ROLLED_BACK=1
  if [ "${UNINSTALL_FULL_SNAPSHOT_READY:-0}" -eq 1 ] && [ -d "${UNINSTALL_FULL_SNAPSHOT:-}" ]; then
    rm -rf "$STATE_DIR"
    cp -R "$UNINSTALL_FULL_SNAPSHOT" "$STATE_DIR"
  elif [ -e "${UNINSTALL_FULL_BACKUP:-}" ] || [ -L "${UNINSTALL_FULL_BACKUP:-}" ]; then
    rm -rf "$STATE_DIR"
    mv "$UNINSTALL_FULL_BACKUP" "$STATE_DIR"
  fi
  rm -rf "${UNINSTALL_FULL_BACKUP:-}" "${UNINSTALL_FULL_SNAPSHOT:-}" 2>/dev/null || :
  oldIFS=$IFS; IFS=$'\n'
  for record in $UNINSTALL_REMOVED_LINKS; do
    [ -n "$record" ] || continue
    path=$(printf '%s' "$record" | awk -F '\t' '{print $1}'); target=$(printf '%s' "$record" | awk -F '\t' '{print $2}')
    [ -e "$path" ] || [ -L "$path" ] || ln -s "$target" "$path"
  done
  IFS=$oldIFS
}

uninstall_apply_full() {
  uninstall_preflight_links
  [ ! -L "$STATE_DIR" ] || fail "refusing to remove symlinked state directory: $STATE_DIR"
  UNINSTALL_FULL_BACKUP="$STATE_DIR.uninstall-backup.$$"
  UNINSTALL_FULL_SNAPSHOT="$STATE_DIR.uninstall-snapshot.$$"
  [ ! -e "$UNINSTALL_FULL_BACKUP" ] && [ ! -L "$UNINSTALL_FULL_BACKUP" ] || fail "uninstall backup already exists: $UNINSTALL_FULL_BACKUP"
  [ ! -e "$UNINSTALL_FULL_SNAPSHOT" ] && [ ! -L "$UNINSTALL_FULL_SNAPSHOT" ] || fail "uninstall snapshot already exists: $UNINSTALL_FULL_SNAPSHOT"
  UNINSTALL_FULL_SNAPSHOT_READY=0
  UNINSTALL_REMOVED_LINKS=''
  UNINSTALL_ROLLED_BACK=0
  trap 'uninstall_full_rollback; exit 1' EXIT HUP INT TERM
  mv "$STATE_DIR" "$UNINSTALL_FULL_BACKUP" || fail 'cannot stage state removal'
  cp -R "$UNINSTALL_FULL_BACKUP" "$UNINSTALL_FULL_SNAPSHOT" || fail 'cannot snapshot installer state'
  UNINSTALL_FULL_SNAPSHOT_READY=1
  oldIFS=$IFS; IFS=$'\n'
  for line in $OLD_LINK_LINES; do
    [ -n "$line" ] || continue
    path=$(field "$line" path); target=$(field "$line" target)
    if [ -L "$path" ]; then
      rm -f "$path" || fail "cannot remove recorded link: $path"
      UNINSTALL_REMOVED_LINKS="$UNINSTALL_REMOVED_LINKS$(printf '%s\t%s' "$path" "$target")
"
    fi
  done
  IFS=$oldIFS
  rm -rf "$UNINSTALL_FULL_BACKUP" || fail 'cannot remove installer state'
  UNINSTALL_ROLLED_BACK=1
  trap - EXIT HUP INT TERM
  rm -rf "$UNINSTALL_FULL_SNAPSHOT" 2>/dev/null || say "warning: cleanup left uninstall snapshot behind: $UNINSTALL_FULL_SNAPSHOT"
  say 'Full uninstall complete.'
}

uninstall_print_summary() {
  tty=/dev/tty
  if [ "$UNINSTALL_MODE" = full ]; then
    printf '\nFull uninstall will remove %s registration(s), %s recorded link(s), and %s.\n' "$UNINSTALL_REG_COUNT" "$OLD_LINK_COUNT" "$STATE_DIR" >"$tty"
  else
    uninstall_build_remaining
    remove_count=0
    oldIFS=$IFS; IFS=$'\n'
    for line in $OLD_LINK_LINES; do
      [ -n "$line" ] || continue
      path=$(field "$line" path); dest=${path%/*}
      uninstall_has_remaining_destination "$dest" || remove_count=$((remove_count + 1))
    done
    IFS=$oldIFS
    printf '\nPartial uninstall will remove %s registration(s) and %s physical link(s).\n' "$UNINSTALL_SELECTED_COUNT" "$remove_count" >"$tty"
  fi
}

prompt_uninstall_confirmation() {
  selector_reset
  SELECTOR_TITLE='confirm uninstall'
  SELECTOR_ACTION='Arrow keys choose'
  SELECTOR_HINT='Default is No; choose Yes to continue.'
  selector_add_option 'No' no
  selector_add_option 'Yes' yes
  selector_run_single
  [ "$SELECTOR_RESULT" = yes ] || fail 'uninstall cancelled'
}

run_uninstall() {
  [ -f "$MANIFEST" ] || fail 'nothing to uninstall: manifest is missing'
  load_old_links
  load_uninstall_registrations
  uninstall_manifest_setup
  if [ -z "$UNINSTALL_MODE" ]; then
    tty=/dev/tty
    [ -r "$tty" ] && [ -w "$tty" ] || fail 'interactive uninstall requires /dev/tty; use uninstall --full --yes or partial CLI flags'
    prompt_uninstall_mode
    if [ "$UNINSTALL_MODE" = partial ]; then
      UNINSTALL_FILTER_SCOPE=''
      UNINSTALL_FILTER_ROOT=''
      UNINSTALL_FILTER_DEST=''
      UNINSTALL_FILTER_INCLUDE_PATH=0
      UNINSTALL_FILTER_ALL_PROJECT=0
      prompt_uninstall_scope
      UNINSTALL_AGENTS=''
      prompt_uninstall_registrations
      UNINSTALL_SELECTED_COUNT=0
      index=1
      while [ "$index" -le "$UNINSTALL_REG_COUNT" ]; do
        [ "${UNINSTALL_SELECTED[$index]:-0}" -eq 1 ] && UNINSTALL_SELECTED_COUNT=$((UNINSTALL_SELECTED_COUNT + 1))
        index=$((index + 1))
      done
    fi
    uninstall_print_summary
    prompt_uninstall_confirmation
    interactive_close
  elif [ "$UNINSTALL_MODE" = partial ]; then
    uninstall_build_selected_from_filter
  fi
  if [ "$UNINSTALL_MODE" = full ]; then
    uninstall_apply_full
  else
    uninstall_build_remaining
    uninstall_apply_partial
  fi
}

COMMAND=install
if [ "${1:-}" = uninstall ]; then
  COMMAND=uninstall
  shift
fi
ORIGINAL_ARGS=( "$@" )
SOURCE_DIR=""; UPDATE=0; SELECTED_AGENTS=""; SCOPE=""; PROJECT_ROOT=""; EXPLICIT_PATH=""
SKILL_ARG=""; SELECTED_IMPL_FROM_PROMPT=""; PROMPT_SKILLS_RAN=0
UNINSTALL_MODE=""; FULL_FLAG=0; PARTIAL_FLAG=0; YES_FLAG=0
UNINSTALL_AGENTS=""; UNINSTALL_FILTER_SCOPE=""; UNINSTALL_FILTER_ROOT=""; UNINSTALL_FILTER_DEST=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent) [ "$#" -ge 2 ] || fail "--agent requires a value"; add_agent "$2"; shift 2 ;;
    --global) [ -z "$SCOPE" ] || fail "choose only one scope"; SCOPE=global; shift ;;
    --project) [ -z "$SCOPE" ] || fail "choose only one scope"; SCOPE=project; if [ "$#" -ge 2 ] && [ "${2#--}" = "$2" ]; then PROJECT_ROOT=$2; shift 2; else PROJECT_ROOT=$PWD; shift; fi ;;
    --path) [ "$#" -ge 2 ] || fail "--path requires a path"; [ -z "$SCOPE" ] || fail "choose only one scope"; SCOPE=path; EXPLICIT_PATH=$2; shift 2 ;;
    --full) FULL_FLAG=1; shift ;;
    --partial) PARTIAL_FLAG=1; shift ;;
    --yes) YES_FLAG=1; shift ;;
    --update) UPDATE=1; shift ;;
    --source-dir) [ "$#" -ge 2 ] || fail "--source-dir requires a path"; SOURCE_DIR=$2; shift 2 ;;
    --skill) [ "$#" -ge 2 ] || fail "--skill requires a value"; SKILL_ARG=$2; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) fail "unknown option: $1" ;;
  esac
done

if [ "$SCOPE" = path ]; then
  normalize_explicit_path
fi

if [ "$COMMAND" = uninstall ]; then
  [ -z "$SOURCE_DIR" ] || fail '--source-dir is only valid for install or update'
  [ "$UPDATE" -eq 0 ] || fail '--update is incompatible with uninstall'
  [ -z "$SKILL_ARG" ] || fail '--skill is only valid for install or update'
  UNINSTALL_AGENTS=$SELECTED_AGENTS
  if [ "$FULL_FLAG" -eq 1 ] || [ "$PARTIAL_FLAG" -eq 1 ]; then
    [ "$FULL_FLAG" -eq 0 ] || [ "$PARTIAL_FLAG" -eq 0 ] || fail 'choose only one uninstall mode'
    [ "$YES_FLAG" -eq 1 ] || fail 'uninstall automation requires --yes'
    if [ "$FULL_FLAG" -eq 1 ]; then
      [ -z "$UNINSTALL_AGENTS" ] && [ -z "$SCOPE" ] || fail '--full cannot be combined with agent or scope filters'
      UNINSTALL_MODE=full
    else
      [ -n "$UNINSTALL_AGENTS" ] || fail '--partial requires --agent'
      [ -n "$SCOPE" ] || fail '--partial requires exactly one scope'
      UNINSTALL_MODE=partial
      case "$SCOPE" in
        global) UNINSTALL_FILTER_SCOPE=global; UNINSTALL_FILTER_INCLUDE_PATH=0 ;;
        project)
          UNINSTALL_FILTER_INCLUDE_PATH=0
          UNINSTALL_FILTER_SCOPE=project
          PROJECT_ROOT=${PROJECT_ROOT:-$PWD}
          UNINSTALL_FILTER_ROOT=$(cd "$PROJECT_ROOT" 2>/dev/null && pwd -P) || fail "project path does not exist: $PROJECT_ROOT"
          ;;
        path) UNINSTALL_FILTER_SCOPE=path; UNINSTALL_FILTER_DEST=$EXPLICIT_PATH; UNINSTALL_FILTER_INCLUDE_PATH=0 ;;
        *) fail 'invalid uninstall scope' ;;
      esac
    fi
  else
    [ "$YES_FLAG" -eq 0 ] && [ -z "$UNINSTALL_AGENTS" ] && [ -z "$SCOPE" ] || fail 'uninstall flags require --full or --partial'
  fi
  run_uninstall
  exit 0
fi

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
  if [ "$UPDATE" -eq 1 ]; then :; else
    # Populates SKILL_NAMES/PACKAGE_LINES for the prompt below; install_release
    # calls validate_source again, which is idempotent (pure re-parse, no writes).
    validate_source "$SOURCE_DIR"
    prompt_selection
  fi
fi
install_release
