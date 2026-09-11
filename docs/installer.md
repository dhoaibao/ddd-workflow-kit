# Installer and manager reference

Detail behind `README.md`'s Install section: the manager's commands, uninstall
prompts and automation, interactive Project-uninstall listing, and how
optional-package selection is recorded and inherited across registrations.

## Interactive install

The base `curl | bash` command prompts interactively: use ↑/↓ and Space to
choose one or more agent targets (multi-select — pressing Enter without
pressing Space on any other row selects only the first highlighted target),
then Enter to confirm; scope (global vs. project) is a separate single-select
menu, one choice only.

`shared` (one of the target names) registers the common `.agents/skills`
directory rather than an agent-specific one: `~/.agents/skills` globally, or
`<project>/.agents/skills` for a project scope.

## Manager commands

Installed at `~/.ddd-workflow-kit/bin/ddd-workflow-kit`, the manager accepts:

- `install` — record a new selection (agent, scope, and optional `--skill`
  packages) alongside any existing registrations.
- `update` — refresh every existing registration from the latest release,
  preserving the prior package selection unless a narrower `--skill` is
  passed.
- `uninstall` — remove registrations. `--full` removes every managed
  registration plus the local installer state, including the versioned skills
  cache at `~/.ddd-workflow-kit/skills` (`~/.ddd-workflow-kit`);
  `--partial` removes one registration (`--agent` plus `--global`, `--project
  [path]`, or `--path`) while preserving physical links still shared by other
  registrations.
- `version` — print the installed release version.

```bash
# Refresh every registration, preserving the prior package selection
~/.ddd-workflow-kit/bin/ddd-workflow-kit update

# Remove every managed registration and the local installer state
~/.ddd-workflow-kit/bin/ddd-workflow-kit uninstall --full --yes

# Remove one registration while preserving shared physical links when needed
~/.ddd-workflow-kit/bin/ddd-workflow-kit uninstall --partial --agent shared --global --yes
```

Uninstall prompts default to **No**; automation (non-interactive shells,
scripts, CI) must pass `--yes` to proceed without confirmation.

## Interactive Project uninstall

When uninstalling interactively with `--agent ... --project` and no explicit
path, the prompt lists every matching **registration** row for that project,
not physical destinations: both plain project rows and explicit-path rows
(labelled `explicit path`) appear separately even when two registrations
happen to resolve to the same directory on disk. Selecting a row removes that
registration's bookkeeping and — only when no other registration still
references it — the underlying symlink.

## Optional-package selection state

Optional (`implementation`-class) package selection is recorded **once per
local install state**, in `~/.ddd-workflow-kit/manifest.json`, not once per
destination. Concretely:

- Passing `--skill ddd-impl-fastapi-hdx` when registering one agent/scope
  updates the single shared selection for this machine's install, not just
  that one registration.
- The *next* `install` or `update` call for a different agent or scope on the
  same machine inherits that selection automatically — it also links the
  opted-in implementation package — unless that later call explicitly passes
  a narrower `--skill` (or `--skill` naming only document-class packages,
  which document-class packages always include regardless).
- This is intentional, not incidental: an earlier review found the
  per-destination-looking flag actually behaving machine-wide surprising
  enough to warrant fixing and documenting explicitly, so a package selected
  for one agent does not silently reappear — or silently vanish — on the
  next unrelated registration without a stated reason.

Document-class packages always install and can never be deselected via
`--skill`; only the optional implementation-class selection is affected by
the behavior above.
