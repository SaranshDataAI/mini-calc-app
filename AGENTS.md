# Codex Engineering Instructions

## Primary Engineering Standard

Before modifying any code, read and follow:

`.codex/skill.md`

This file contains the detailed engineering standards for this repository.

## Priorities

Always prioritize:

1. Correctness
2. Clean and maintainable code
3. Appropriate algorithmic complexity
4. Strong DSA practices
5. Dynamic Programming reasoning
6. Testing
7. Performance
8. Security
9. Production-ready ML/MLOps engineering

## Repository Workflow

Before making changes:

1. Inspect the repository structure.
2. Read the relevant existing files.
3. Understand the existing architecture.
4. Identify existing utilities before creating new ones.
5. Make the smallest safe change required.
6. Do not modify unrelated code.

After making changes:

1. Run relevant tests.
2. Run linting/formatting if configured.
3. Check for regressions.
4. Review the final diff.
5. Clearly report what changed and what was tested.

## DSA Requirements

For algorithmic problems, explicitly reason about:

- Problem pattern
- Approach
- Correctness
- Time complexity
- Space complexity
- Edge cases

Avoid brute force when constraints require a better solution.

Consider appropriate patterns such as:

- Hashing
- Two pointers
- Sliding window
- Prefix sums
- Binary search
- Stack / monotonic stack
- Heap
- BFS / DFS
- Graph algorithms
- Greedy
- Backtracking
- Dynamic Programming
- Union-Find
- Trie
- Bit manipulation

## Dynamic Programming Requirements

For DP problems explicitly identify:

- State
- Transition
- Base cases
- Iteration order
- Final answer
- Time complexity
- Space complexity
- Possible space optimization

Do not write DP code without understanding and defining the state.

## ML / AI Requirements

For ML/AI code:

- Prevent data leakage.
- Keep preprocessing separate from training.
- Make experiments reproducible.
- Version important artifacts.
- Validate input data.
- Track model and dataset versions.
- Separate training, evaluation, and inference.
- Prefer production-ready architecture over notebook-only implementations.

## MLOps Requirements

Consider:

- Data validation
- Experiment tracking
- Model versioning
- Model validation gates
- CI/CD
- Deployment strategy
- Monitoring
- Logging
- Rollback
- Reproducibility

## Python Standards

Write:

- Type-safe code
- Small focused functions
- Meaningful names
- Clear interfaces
- Proper exception handling
- Testable components

Avoid:

- Giant functions
- Unnecessary abstractions
- Duplicate logic
- Magic numbers
- Silent exception handling
- Hard-coded secrets
- Unnecessary refactoring

## Performance

Always consider:

- Time complexity
- Space complexity
- Unnecessary loops
- Repeated computation
- Unnecessary allocations
- Database/API bottlenecks
- Vectorization where appropriate

Do not perform premature optimization when it harms readability.

## Security

Never hard-code:

- API keys
- Passwords
- Tokens
- Credentials
- Private secrets

Never expose secrets in logs or API responses.

## Final Quality Gate

Before finishing a task, verify:

- [ ] Requirement understood
- [ ] Correct solution implemented
- [ ] Edge cases considered
- [ ] Complexity is appropriate
- [ ] Code is readable
- [ ] No unnecessary duplication
- [ ] Tests added/updated where appropriate
- [ ] Relevant tests executed
- [ ] Security checked
- [ ] Final diff reviewed