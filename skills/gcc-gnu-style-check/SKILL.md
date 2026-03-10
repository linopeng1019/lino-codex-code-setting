---
name: gcc-gnu-style-check
description: Use this for a standalone GCC GNU style check on patch diffs (staged, unstaged, commit, or patch file). For full patch finalization, prefer gcc-pre-commit-checks, which already includes this gate.
---

# GCC GNU style patch check skill

## Scope

- Primary use: verify GNU style compliance for GCC patches with `./contrib/check_GNU_style.py`
- Check changed lines via patch diffs instead of scanning whole files
- Quick standalone style gate before commit or review

## Preconditions

- Run commands from GCC repository root
- Ensure required Python modules are available:
  `pip3 install --user unidiff termcolor`
- Understand checker limits:
  - It skips files under `testsuite/`
  - It skips `.py` files
  - It skips `libstdc++-v3/`
  - It checks added lines in the patch

## Positioning

- Use when user asks only for GNU style diagnostics or quick cleanup
- For full "ready to commit" flow, use `gcc-pre-commit-checks`

## Patch selection workflow

- Unstaged working tree changes:
  `git diff | ./contrib/check_GNU_style.py -`
- Staged changes only:
  `git diff --cached | ./contrib/check_GNU_style.py -`
- A specific commit:
  `git show --format=email --no-stat <commit> | ./contrib/check_GNU_style.py -`
- A pre-generated patch file:
  `./contrib/check_GNU_style.py <patch-file>`

## Output modes

- Default `stdio` mode:
  `./contrib/check_GNU_style.py -f stdio <patch-file-or->`
  - Group errors by type and print exact `file:line:column`
- `quickfix` mode:
  `./contrib/check_GNU_style.py -f quickfix <patch-file-or->`
  - Write diagnostics to `errors.err` for editor quickfix usage

## Iteration expectations

- If the checker exits non-zero:
  - Keep the exact diagnostics
  - Fix reported style violations in source files
  - Re-run with the same patch scope until exit code is `0`
- If no diff exists, report there is nothing to check
- Do not claim style compliance without a successful checker run

## Agent behavior expectations

- Prefer `git diff --cached` when user is preparing a commit
- Use `git diff` when there are no staged changes
- If the user provides a patch file or commit hash, use that exact scope
- After style cleanup, suggest running the relevant tests for touched code
- Do not claim full pre-commit readiness from this check alone
