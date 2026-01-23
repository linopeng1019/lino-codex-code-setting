---
name: github-operations
description: Use this skill for any GitHub task (PRs, issues, reviews, workflows, releases, repo info) or when given a GitHub URL; ensure all GitHub operations use the gh CLI, especially for requests like "view PR diff", "list issues", "check actions", or "create PR".
---

# GitHub Operations Guide

## Core Principle

**Always use the `gh` command for ALL GitHub-related operations.** Never use raw API calls, curl to GitHub API, or other methods when `gh` can accomplish the task.

## Operations Requiring Explicit User Permission

**IMPORTANT:** The following operations modify remote state and MUST NOT be performed without explicit user permission:

- **PR comments**: `gh pr comment`, `gh pr review --comment`
- **PR updates**: `gh pr edit`, `gh pr merge`, `gh pr close`, `gh pr reopen`
- **Push to remote**: `git push` (branches or tags)
- **Issue modifications**: `gh issue comment`, `gh issue edit`, `gh issue close`
- **Release creation**: `gh release create`

Always ask the user for confirmation before executing any of these commands. Read-only operations (view, list, diff, checkout) can be performed freely.

## Common Operations

### Pull Requests

```bash
# List PRs
gh pr list

# View specific PR
gh pr view <number>

# View PR diff
gh pr diff <number>

# Create PR
gh pr create --title "Title" --body "Description"

# Check out a PR locally
gh pr checkout <number>

# Review a PR
gh pr review <number> --approve
gh pr review <number> --comment --body "Comment"
gh pr review <number> --request-changes --body "Changes needed"

# Merge a PR
gh pr merge <number>

# View PR comments
gh api repos/{owner}/{repo}/pulls/{number}/comments
```

### Issues

```bash
# List issues
gh issue list

# View specific issue
gh issue view <number>

# Create issue
gh issue create --title "Title" --body "Description"

# Close issue
gh issue close <number>

# Add labels
gh issue edit <number> --add-label "bug,urgent"
```

### Repository Information

```bash
# View repo info
gh repo view

# Clone a repo
gh repo clone <owner>/<repo>

# Fork a repo
gh repo fork <owner>/<repo>
```

### Workflows and Actions

```bash
# List workflow runs
gh run list

# View specific run
gh run view <run-id>

# Watch a run
gh run watch <run-id>

# Rerun failed jobs
gh run rerun <run-id> --failed
```

### Releases

```bash
# List releases
gh release list

# Create release
gh release create <tag> --title "Title" --notes "Notes"

# Download release assets
gh release download <tag>
```

## When Given a GitHub URL

**IMPORTANT:** If the user provides ANY GitHub URL (e.g., `https://github.com/...`), ALWAYS use the `gh` command to handle it. NEVER use WebFetch, curl, or other tools to access GitHub URLs.

Examples:
- `https://github.com/owner/repo/pull/123` → `gh pr view 123 --repo owner/repo`
- `https://github.com/owner/repo/issues/456` → `gh issue view 456 --repo owner/repo`
- `https://github.com/owner/repo` → `gh repo view owner/repo`
- `https://github.com/owner/repo/actions/runs/789` → `gh run view 789 --repo owner/repo`

## Authentication

The `gh` CLI should already be authenticated. If not, prompt the user to run `gh auth login`.
