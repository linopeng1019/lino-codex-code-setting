---
name: commit-message
description: Use this skill when the user asks to write commit messages for current unstaged or staged changes (for example "commit message", "commit.md", or "help me write a commit message").
---

# Commit message drafting skill

## Scope

- Draft commit messages for current working tree changes.
- Improve existing draft messages while preserving intent.
- Keep output concise and ready to use.

## Message style

- Write in English using ASCII only.
- Keep non-code lines within 79 columns.
- Use an imperative subject line that states what changed.
- Add a body only when it adds necessary context.

## Workflow

1. Inspect current diff (`git diff` and `git diff --cached` as needed).
2. If a commit message draft already exists, show it first and explain how it can improve.
3. Provide 2 or 3 message options.
4. Wait for user selection or edits.
5. Apply the selected message only after explicit confirmation.

## Notes

- If changes are broad or mixed, suggest splitting into multiple commits.
- Preserve important issue IDs, links, and user-provided wording when possible.
