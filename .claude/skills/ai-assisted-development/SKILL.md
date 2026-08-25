# AI-Assisted Development

## Purpose

Define a lightweight workflow for developing the project
with AI coding agents while maintaining engineering quality
and helping the developer understand the system.

The goal is NOT to add unnecessary process.

The goal is to balance:

- Development speed
- Code quality
- System understanding
- Architecture awareness
- Learning

---

## Core Principle

Do not apply the same workflow to every task.

First assess the complexity and reversibility of the task.

Use the minimum process necessary.

---

# 1. Assess Task Complexity

Classify the task into:

### Small

Examples:

- Simple bug fix
- Rename
- Small validation change
- Add simple field
- Add test
- Small CRUD modification

Workflow:

Implement → Test

---

### Medium

Examples:

- New API endpoint
- Authentication
- New backend module
- Database schema change
- RAG component

Workflow:

Understand → Plan → Implement → Test → Review

---

### Architectural

Examples:

- Major architecture change
- Database technology change
- RAG architecture
- Agent architecture
- Queue architecture
- Authentication architecture
- Service boundary changes

Workflow:

Understand
→ Explore alternatives
→ Design
→ Discuss trade-offs
→ Plan
→ Implement
→ Test
→ Review

---

# 2. Understand

For medium and architectural tasks:

Before implementation:

1. Inspect the relevant codebase.
2. Identify existing architecture.
3. Identify related components.
4. Identify dependencies.
5. Understand current data flow.
6. Identify constraints.

Do not modify code during this stage.

---

# 3. Plan

For medium and architectural tasks:

Create a concise implementation plan.

Include:

- Files to create/modify
- Components affected
- Request/data flow
- Important design decisions
- Edge cases
- Tests

Do not over-plan simple tasks.

---

# 4. Implement

Implement according to the agreed plan.

Rules:

- Do not expand scope unnecessarily.
- Do not refactor unrelated code.
- Do not introduce new technologies without justification.
- Follow existing project conventions.
- Keep changes focused.

---

# 5. Test

After implementation:

- Run relevant unit tests.
- Run integration tests when applicable.
- Test important error cases.
- Verify that existing functionality is not broken.

Report:

- Tests executed
- Results
- Tests not available
- Remaining risks

---

# 6. Review

For medium and architectural tasks:

Review the implementation for:

- Correctness
- Architecture
- Separation of concerns
- Security
- Error handling
- Performance
- Scalability
- Maintainability
- Edge cases

Do not automatically refactor after review.

First report the findings.

---

# 7. Engineering Record

Create an engineering record only when the task contains meaningful engineering knowledge.

Examples:

- Important architectural decision
- New architecture/component
- Important trade-off
- Difficult bug
- New technical concept
- Significant security consideration
- Significant performance consideration

Do NOT create a record for trivial changes.

Store records under:

docs/engineering/

Recommended structure:

- Context
- What changed
- Architecture
- Data flow
- Design decisions
- Alternatives and trade-offs
- Failure cases
- Security
- Performance
- Testing
- What was learned
- Questions to revisit
- Future improvements

---

# 8. Learning Principle

When appropriate, explain WHY rather than only WHAT.

Focus on:

- Why this design?
- Why this component?
- Why this dependency?
- What alternatives exist?
- What are the trade-offs?
- What happens when the system fails?
- How would this change when scaling?

Do not explain every line of code unless explicitly requested.

---

# 9. Do Not Over-Process

Speed matters.

Do not:

- Create unnecessary documentation.
- Produce long plans for trivial tasks.
- Ask unnecessary questions.
- Refactor unrelated code.
- Introduce unnecessary abstractions.
- Repeat explanations that are already documented.

Use the smallest workflow that provides sufficient confidence.
