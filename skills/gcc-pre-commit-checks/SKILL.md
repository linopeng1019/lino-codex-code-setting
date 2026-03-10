---
name: gcc-pre-commit-checks
description: Use this as the default GCC pre-commit workflow. It runs three required gates in order on staged changes: git clang-format, contrib/check_GNU_style.py, and contrib/gcc-changelog/git_check_commit.py after commit or amend. Use for requests like "check before commit", "run all GCC checks", or "prepare this patch for upstream".
---

# GCC pre-commit checks skill

## Scope

- Canonical and default entry point for GCC patch finalization
- Enforce all required quality gates in fixed order
- Include commit message and ChangeLog validation as part of the same flow

## Positioning

- Use this skill by default for any "ready to commit/send" GCC task
- This skill includes GNU style checking internally
- This skill is responsible for commit message and ChangeLog validation

## Preconditions

- Run commands from GCC repository root
- Ensure `git clang-format` is available
- Ensure GNU style checker dependencies are available:
  `pip3 install --user unidiff termcolor`

## Standard workflow

1. Prepare staged changes
- Stage the intended patch first
- Prefer checking staged content to avoid unrelated working-tree noise

2. Run clang-format on staged hunks
- Command:
  `git clang-format --staged`
- If needed, limit to specific files:
  `git clang-format --staged -- <file1> <file2>`
- Re-stage files if your local setup requires it

3. Run GNU style patch checker
- Command:
  `git diff --cached | ./contrib/check_GNU_style.py -`
- If checker fails, fix reported locations and repeat from step 2

4. Create or amend the commit
- Write commit message and ChangeLog in GCC format
- Subject format:
  `component[, component]: Brief description`
- Ensure affected directories have matching ChangeLog sections:
  `gcc/ChangeLog`, `gcc/cp/ChangeLog`, `gcc/testsuite/ChangeLog`,
  `libstdc++-v3/ChangeLog`, etc.

5. Run commit ChangeLog validation
- Command:
  `python3 contrib/gcc-changelog/git_check_commit.py HEAD`
- If validation fails, amend commit message/ChangeLog and re-run until clean

## Pass criteria

- `git clang-format --staged` completes without unresolved formatting issues
- `./contrib/check_GNU_style.py` exits with code `0` on staged diff
- `git_check_commit.py HEAD` exits with code `0`

## Agent behavior expectations

- Do not skip steps unless user explicitly asks
- Report exact failing command output and affected files/lines
- When checks fail, apply minimal targeted fixes and re-run the same gate
- Before final submission, summarize which gates passed
- If user asks only for GNU style, allow switching to `gcc-gnu-style-check`
