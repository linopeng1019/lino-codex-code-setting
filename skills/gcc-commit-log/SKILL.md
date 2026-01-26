---
name: gcc-commit-log
description: Use this skill when generating, reviewing, or amending GCC project commit messages and ChangeLog entries from a git diff. This skill enforces GCC component naming, subject formatting, hangeLog structure, and validation using contrib/gcc-changelog/git_check_commit.py, iterating until the commit passes all checks and is ready for upstream submission.
---

# GCC commit message and ChangeLog skill

## Scope

- Primary use: generate and refine GCC project commit messages and ChangeLog
  entries from a git tree diff (staged or unstaged)
- Output must strictly follow GCC conventions and be suitable for upstream
  submission without further manual editing

## GCC commit message conventions

- Use the GCC standard subject format:
  component[, component]: Brief description
- Component names must be lower-case and match GCC conventions, except use "RISC-V" uppercase when the component refers to the RISC-V target, e.g.:
  c++, c, fortran, ada, go, objc, objc++, jit
  tree-optimization, rtl-optimization, middle-end
  target (or a specific port such as i386, aarch64, rs6000, RISC-V)
  libstdc++, libgcc, libgomp, libgfortran, libobjc
  testsuite, docs, build-system, driver
- Multiple components are comma-separated, e.g.:
  c++, middle-end: ...
- Subcomponents use a slash, e.g.:
  libstdc++/ranges: ...
- Keep non-code lines within 79 columns
  Code, commands, paths, and URLs may exceed 79 columns
- Write in English, concise and conversational
- ASCII only, no emoji, no non-ASCII characters
- Use sentence-style capitalization for the subject line
- Do not end the subject line with a period

## Commit body content rules

- Prefer user-visible behavior changes over internal implementation details
- Use consistent verbs:
  - Fix: bug fix or correctness issue
  - Add / Implement: new feature or new support
  - Improve / Optimize: performance or compile-time improvements
  - Clean up / Refactor: code organization changes without behavior changes
- Use GCC terminology when appropriate (gimple, RTL, IPA, LTO, etc.)
- Preserve and include important references:
  - Bugzilla / PR references must use GCC format:
    PR c++/12345, PR target/67890
  - Regressions must be explicit:
    PR regression/xxxxx
  - ABI changes must be called out explicitly in the description

## ChangeLog generation (required)

- A ChangeLog entry is required and must follow GCC style
- Each affected directory must have a corresponding ChangeLog section,
  for example:
  gcc/ChangeLog, gcc/cp/ChangeLog, gcc/testsuite/ChangeLog,
  libstdc++-v3/ChangeLog
- Each ChangeLog section format:

  <dir>/ChangeLog:

  <blank line>
  <tab>* file (function): Description.
  <tab>* file: New file.
  <tab>* file: Removed.

- Use a single tab for indentation before each "*" line
- Descriptions must start with a capital letter and end with a period
- Keep descriptions short and focused on the actual change

## Workflow expectations

- If the change already has an existing commit message, show the original
  message first, then propose improvements in GCC style
- Inspect the diff to identify:
  - the correct component or components
  - affected directories for ChangeLog entries
  - any testsuite updates or new tests required
  - any ABI or regression implications
- Always provide 1 complete commit message options
  Each option must include the required ChangeLog sections
- If changes span multiple unrelated components, suggest splitting commits

## Validation expectations

- After writing or amending a commit message, validate it using:
  contrib/gcc-changelog/git_check_commit.py
- If validation fails:
  - show the exact error output
  - explain which GCC rules are violated
  - fix the commit message accordingly
  - amend and re-run validation until it passes

## Output format template

- Subject line
- Blank line
- ChangeLog blocks per affected directory
- Optional additional paragraphs only when they add value, such as:
  - rationale for behavior change
  - brief notes on tests added or updated
  - PR, regression, or ABI callouts

## Example

c++: Implement C++23 consteval if feature

gcc/cp/ChangeLog:

	* parser.cc (cp_parser_selection_statement): Add consteval if parsing.
	* semantics.cc (finish_if_stmt): Handle consteval conditions.
gcc/testsuite/ChangeLog:

	* g++.dg/cpp23/consteval-if1.C: New test.
