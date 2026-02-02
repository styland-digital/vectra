---
description: Implement a feature following TDD workflow. Creates branch, writes tests first, then implements code.
allowed-tools: Read, Write, Edit, Bash, Task
---

# Implement Feature: $ARGUMENTS

## Workflow

### Step 1: Create Feature Branch
```bash
git checkout -b feature/$ARGUMENTS
```

### Step 2: Understand Requirements
- Read relevant documentation in `/docs/`
- Check existing patterns in codebase
- Identify affected files

### Step 3: Write Tests FIRST (TDD)
- Create test file(s)
- Write failing tests that describe expected behavior
- Run tests to confirm they fail

### Step 4: Implement Minimum Code
- Write just enough code to make tests pass
- Follow patterns in `vectra-patterns` skill
- Apply multi-tenant filters on all queries

### Step 5: Refactor
- Clean up code while keeping tests green
- Remove duplication
- Improve naming

### Step 6: Documentation
- Add docstrings/JSDoc
- Update API docs if creating endpoint
- Add CHANGELOG entry

### Step 7: Commit
```bash
git add .
git commit -m "feat: $ARGUMENTS"
```

## Checklist Before Completing
- [ ] Tests written and passing
- [ ] Type hints complete
- [ ] Multi-tenant filters applied
- [ ] Error handling in place
- [ ] Documentation updated
- [ ] Code formatted (auto via hooks)
