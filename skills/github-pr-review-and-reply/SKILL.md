---
name: github-pr-review-and-reply
description: Use this skill when reviewing a GitHub PR and posting the review summary as an English PR comment (for example "review-github-pr-and-reply").
---

# GitHub PR review and reply skill

## Scope

- Run a structured PR review.
- Draft review output in English.
- Post the result back to the PR thread via `gh`.

## Workflow

1. Collect PR context, diff, checks, and commit history.
2. Perform review with severity-based findings.
3. Write final comment body to `review-comments.md`.
4. Post with:
   `gh pr comment <pr-number> --body-file review-comments.md`
5. Remove temporary file after posting.

## Review dimensions

- Code quality and maintainability.
- Functional correctness and edge-case behavior.
- Security posture.
- Test quality and compatibility risk.

## Output requirements

- Posted comment must be English.
- Keep feedback specific and actionable.
- Use clear severity grouping.
