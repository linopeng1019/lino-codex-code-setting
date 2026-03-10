---
name: llvm-commit-log
description: Use this skill when writing or refining LLVM-style commit messages (for example "llvm-commit-log", "LLVM commit message", or "rewrite this commit in LLVM style").
---

# LLVM commit message skill

## Scope

- Draft or refine commit messages for LLVM projects.
- Follow LLVM component-tag subject style.
- Preserve technical intent and issue references.

## Message style

- English, ASCII only.
- Non-code lines within 79 columns.
- Subject format: `[Component] Brief description`.
- Prefer imperative verbs such as `Fix`, `Add`, `Implement`, `Improve`.

## Component guidance

- Common tags include:
  `[clang]`, `[llvm]`, `[mlir]`, `[flang]`, `[lld]`, `[lldb]`, `[openmp]`,
  `[CodeGen]`, `[X86]`, `[AArch64]`, `[RISCV]`, `[IR]`, `[MC]`, `[test]`.

## Workflow

1. Inspect the diff and current commit message (if any).
2. Identify the most accurate LLVM component tags.
3. Provide 2 or 3 complete message options.
4. Wait for user selection.
5. Amend/apply message only after explicit confirmation.

## Notes

- If changes span unrelated components, suggest commit split.
- Keep references to bug IDs, PRs, or design discussions.
