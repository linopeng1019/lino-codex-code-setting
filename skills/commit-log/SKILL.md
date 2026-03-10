---
name: commit-log
description: Use this skill when the user asks to rewrite or refine the message of the latest commit (for example "commit-log", "improve last commit message", or "rewrite HEAD message").
---

# Latest commit message refinement skill

## Scope

- Refine the commit message of `HEAD`.
- Keep technical meaning and references from the original message.
- Produce clean alternatives before amending.

## Message style

- English, ASCII only.
- Non-code lines within 79 columns.
- Prefer Conventional Commits subject format:
  `<type>(<scope>): <description>`.
- Use imperative verbs and concise wording.

## Workflow

1. Read current message with `git log -1 --pretty=%B`.
2. Inspect `HEAD` diff to verify intent.
3. Propose 2 or 3 improved message options.
4. Wait for user choice.
5. Amend only after explicit confirmation.

## Notes

- Keep issue numbers and important references.
- If `HEAD` mixes unrelated changes, suggest splitting commits.
