---
description: Research a topic using parallel subagents for documentation, codebase analysis, and web search.
allowed-tools: Task, WebSearch, WebFetch, Read, Grep, Glob, Write
---

# Research: $ARGUMENTS

## Instructions

Launch 3 parallel subagents to gather comprehensive information:

### 1. Documentation Agent (subagent_type: general-purpose)
Search for:
- Official documentation
- Best practices
- GitHub issues and discussions
- Recommended patterns

### 2. Codebase Explorer (subagent_type: Explore)
Search the Vectra codebase for:
- Related existing patterns
- Similar implementations
- Relevant files and functions

### 3. Web Research Agent (subagent_type: general-purpose)
Find:
- Recent blog posts and articles
- Stack Overflow solutions
- Known issues and workarounds

## Output

Create research document at `docs/research/$(date +%Y-%m-%d)-$ARGUMENTS.md`:

```markdown
# Research: $ARGUMENTS

**Date:** [Today's date]
**Status:** Complete

## Problem Statement
[Why we're researching this]

## Key Findings
[Most important discoveries]

## Codebase Patterns
[What we already have that's relevant]

## Recommended Approach
[Suggested solution based on research]

## Sources
- [List of sources with links]
```
