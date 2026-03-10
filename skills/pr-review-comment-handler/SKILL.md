---
name: pr-review-comment-handler
description: Use this skill when the user asks to process review comments on a GitHub PR and apply requested changes (for example "process-review-comment", "handle review comments on PR #123", or similar requests).
---

# PR review comment handling skill

## Scope

- Fetch latest review comments from a target PR.
- Analyze comment threads and apply requested code changes.
- Produce a clear done/not-done summary.

## Preconditions

- `gh` CLI authenticated and repository access available.
- A PR number provided by the user.

## Workflow

1. Verify PR exists and is accessible (`gh pr view <pr>`).
2. Create an isolated worktree and check out the PR branch.
3. Resolve repository owner/name from git remote.
4. Fetch reviews and locate the latest review ID.
5. Fetch comments for that review, including reply-thread context when
   `in_reply_to_id` is present.
6. Implement required code changes in the PR worktree.
7. Validate affected code/tests as appropriate.
8. Report completed items and skipped items with reasons.

## Reporting format

- Completed changes mapped to specific review comments.
- Unresolved comments and concrete blocking reasons.
- Risks or follow-up actions required.

## Notes

- Prioritize correctness over broad refactors.
- Keep edits minimal and directly tied to reviewer feedback.
