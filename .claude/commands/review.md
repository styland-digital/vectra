---
description: Perform code review on recent changes using the code-reviewer agent.
allowed-tools: Task, Read, Grep, Glob
---

# Code Review

## Instructions

1. **Get changed files**
   ```bash
   git diff --name-only HEAD~1
   ```

2. **Spawn code-reviewer subagent**
   Use Task tool with `subagent_type='code-reviewer'` to review each changed file.

3. **Compile results**
   Aggregate findings from the subagent into a structured review.

## Output Format

```markdown
## Code Review Summary

**Status**: ✅ APPROVED | ⚠️ APPROVED WITH COMMENTS | ❌ CHANGES REQUESTED

### Files Reviewed
- path/to/file1.py
- path/to/file2.ts

### 🔴 Critical Issues
[List blocking issues]

### 🟡 Suggestions
[List non-blocking improvements]

### 🟢 Good Practices Observed
[Highlight what's done well]
```
