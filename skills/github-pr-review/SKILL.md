---
name: github-pr-review
description: Use this skill when reviewing a GitHub PR and returning structured review feedback without posting a comment automatically (for example "review-github-pr" or "review PR #123").
---

# GitHub PR review skill

## Scope

- Perform a structured review for a target PR.
- Gather PR metadata, diff, checks, and commit context via `gh`.
- Produce high-signal review feedback for the user.

## Data collection

- `gh pr view <pr>`
- `gh pr diff <pr>`
- `gh pr checks <pr>`
- diff stats between base and head refs
- commit message history in the PR

## Review dimensions

- Code quality and readability.
- Functional correctness and edge cases.
- Security implications.
- Testing depth and regression coverage.
- Documentation and maintenance impact.

## Output format

- Overall assessment (`Approve`, `Request Changes`, or `Comment`).
- Strengths.
- Issues grouped by severity (`Critical`, `Major`, `Minor`).
- Concrete fix guidance.
- Security and test recommendations.
