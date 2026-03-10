---
name: gcc-reduce-case
description: Use this skill to minimize GCC ICE reproducer test cases with creduce from a full compiler command (for example "gcc-reduce-case" or "reduce this ICE testcase").
---

# GCC ICE testcase reduction skill

## Scope

- Reduce a crashing GCC testcase with `creduce`.
- Preserve only flags required to reproduce the same ICE.
- Output a minimized preprocessed file and reproducible compile command.

## Required input

- Full compiler invocation that reproduces the ICE.
- The source file path and all flags used by the user.

## Workflow

1. Parse the invocation into compiler path, source, and flags.
2. Execute original command and capture the ICE signature from stderr.
3. Generate preprocessed input (`.i` or `.ii`) using `--save-temps -c`.
4. Minimize flags while always preserving `-march=*` and `-mabi=*`.
5. Create `test.sh` interestingness script that returns `0` only when the same
   ICE is reproduced.
6. Verify `test.sh` is deterministic.
7. Run `creduce ./test.sh <preprocessed-file>`.
8. Validate the reduced case still reproduces the same ICE.

## Output

- Reduced testcase content (or file path).
- Simplified reproduction command.
- Removed flags and preserved flags.
- Size reduction statistics.

## Notes

- Use compile-only mode (`-c -o /dev/null`) to avoid link noise.
- Prefer absolute compiler/build paths in `test.sh`.
