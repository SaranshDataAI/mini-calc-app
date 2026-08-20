# Codex Engineering Skill — Clean Code, DSA, Dynamic Programming & MLOps

## Purpose

Use this skill when working on Python, software engineering, algorithms, machine learning, AI, data, or MLOps tasks.

The goal is to produce code that is:

- Correct before clever
- Clean, readable, maintainable, and testable
- Efficient in time and memory
- Algorithmically strong, with explicit complexity analysis
- Production-oriented for ML/AI systems
- Robust against edge cases and failure modes
- Easy for another engineer to review and extend

---

## 1. Core Engineering Principles

### 1.1 Correctness first

Before optimizing:

1. Understand the requirement.
2. Identify inputs, outputs, constraints, and edge cases.
3. State assumptions when requirements are ambiguous.
4. Implement the simplest correct solution.
5. Test representative and adversarial cases.
6. Optimize only where complexity or profiling justifies it.

Never trade correctness for premature optimization.

### 1.2 Prefer simple code

Follow:

- KISS — Keep It Simple.
- DRY — Don't Repeat Yourself.
- YAGNI — Don't build unused abstractions.
- SOLID where it genuinely improves maintainability.
- Composition over unnecessary inheritance.
- Explicit behavior over hidden magic.

Avoid:

- Clever one-liners that reduce readability
- Deeply nested conditionals
- Giant functions
- Giant classes
- Global mutable state
- Unnecessary abstractions
- Copy-pasted logic
- Silent exception swallowing
- Magic numbers and unexplained constants

### 1.3 Single responsibility

Each function/class/module should have a clear responsibility.

Bad:

```python
def process_data():
    # loads files
    # cleans data
    # trains model
    # evaluates model
    # sends email
    # writes database records
```

Prefer small composable units:

```python
data = load_data(...)
data = clean_data(data)
model = train_model(data, config)
metrics = evaluate_model(model, data)
persist_results(metrics)
```

### 1.4 Naming

Use names that communicate intent.

Prefer:

```python
max_retries = 3
customer_embeddings
calculate_precision()
```

Avoid:

```python
x = 3
data2
foo()
```

Use:

- `snake_case` for functions/variables
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants

Boolean names should read naturally:

```python
is_valid
has_permission
should_retry
```

---

# 2. Python Clean-Code Standards

## 2.1 Type hints

Use type hints for public functions and important internal interfaces.

```python
from collections.abc import Sequence

def top_k_scores(scores: Sequence[float], k: int) -> list[float]:
    ...
```

Use modern Python typing when appropriate.

Prefer:

```python
list[str]
dict[str, float]
str | None
```

over unnecessarily verbose legacy syntax when project compatibility permits.

## 2.2 Docstrings

Public modules, classes, and non-obvious functions should have concise docstrings.

Document:

- Purpose
- Important parameters
- Return value
- Important exceptions
- Non-obvious behavior

Do not write meaningless docstrings that merely repeat the function name.

## 2.3 Error handling

Catch specific exceptions.

Good:

```python
try:
    config = load_config(path)
except FileNotFoundError as exc:
    raise ConfigurationError(f"Config not found: {path}") from exc
```

Avoid:

```python
try:
    ...
except Exception:
    pass
```

Never silently hide failures.

Use exceptions for exceptional conditions, not ordinary control flow.

## 2.4 Logging

Use structured, useful logs.

Log:

- Important lifecycle events
- Failures
- Retry attempts
- Model/version information
- Request IDs where relevant
- Latency and performance metrics

Do not log:

- Passwords
- API keys
- Tokens
- Secrets
- Sensitive personal information

Prefer logging with context over random `print()` statements in production code.

---

# 3. Performance Engineering

## 3.1 Complexity must be explicit

For algorithmic code, always determine:

- Time complexity
- Space complexity
- Best/average/worst case when relevant

Example:

```text
Time: O(n log n)
Space: O(n)
```

Do not optimize based on intuition alone when complexity can be reasoned about directly.

## 3.2 Common performance rules

Prefer:

- Hash maps/sets for O(1) average lookup
- Sorting once instead of repeatedly
- Binary search when data is sorted
- Prefix sums for repeated range queries
- Two pointers for suitable ordered-array problems
- Sliding windows for contiguous-range problems
- Heaps for top-k/streaming selection
- BFS/DFS instead of brute force when graph structure applies
- Dynamic programming when overlapping subproblems exist

Avoid:

```python
for item in items:
    if item in large_list:
        ...
```

when a set is appropriate:

```python
lookup = set(large_list)
for item in items:
    if item in lookup:
        ...
```

## 3.3 Avoid unnecessary allocations

Be careful with:

- Repeated string concatenation
- Repeated list copying
- Large temporary objects
- Converting the same data repeatedly
- Materializing entire datasets when streaming is sufficient

Use generators for large streams when appropriate.

## 3.4 Vectorization

For NumPy/Pandas workloads, prefer vectorized operations over Python loops when practical.

Avoid unnecessary:

```python
for row in dataframe.itertuples():
    ...
```

when an equivalent vectorized operation exists.

However, do not force vectorization if it makes correctness or maintainability substantially worse.

---

# 4. DSA Problem-Solving Framework

When solving an algorithmic problem, follow this sequence.

## Step 1 — Understand

Extract:

- Input
- Output
- Constraints
- Ordering guarantees
- Duplicates
- Negative values
- Empty input
- Mutation requirements

## Step 2 — Identify the pattern

Check for:

- Array/string
- Hashing
- Two pointers
- Sliding window
- Prefix sum
- Binary search
- Stack
- Monotonic stack
- Queue/deque
- Linked list
- Tree
- BST
- Heap/priority queue
- Graph
- BFS
- DFS
- Union-Find
- Greedy
- Backtracking
- Dynamic programming
- Trie
- Bit manipulation
- Sorting

## Step 3 — Establish brute force

If useful, briefly reason about the naive approach.

Then ask:

> What repeated work can be eliminated?

## Step 4 — Optimize

Look for:

- Duplicate computation
- Unnecessary nested loops
- Repeated searches
- State that can be cached
- Monotonicity
- Overlapping subproblems
- Useful preprocessing

## Step 5 — Prove correctness

Explain why the algorithm produces the required result.

For greedy algorithms, identify the greedy-choice justification.

For DP, define the state and recurrence.

For binary search, identify the monotonic predicate/invariant.

## Step 6 — Implement

Keep implementation close to the reasoning.

## Step 7 — Test

Always test:

1. Normal case
2. Empty/minimum case
3. Single element
4. Duplicate values
5. Boundary values
6. Worst-case structure
7. Large input conceptually

---

# 5. Dynamic Programming — Required Method

Do not jump directly into code.

Use the following DP framework.

## 5.1 Identify whether DP applies

DP is appropriate when there are:

- Overlapping subproblems
- Optimal substructure
- A manageable state space

Ask:

> If I solve a smaller version, can that result help solve a larger version?

## 5.2 Define the state

Clearly write what `dp[i]` or `dp[i][j]` means.

Example:

```text
dp[i] = maximum value obtainable using the first i items.
```

Never use an undefined DP array.

## 5.3 Define the transition

Write:

```text
dp[state] = best combination of previous states
```

Example:

```text
dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
```

## 5.4 Base cases

Explicitly identify:

- Initial state
- Empty input
- Minimum valid input

## 5.5 Direction

Choose:

- Top-down + memoization
- Bottom-up tabulation
- Space-optimized DP

Use the simplest form that preserves clarity.

## 5.6 Space optimization

If:

```text
dp[i] only depends on dp[i-1] and dp[i-2]
```

consider reducing:

```text
O(n) -> O(1)
```

But do not sacrifice readability for trivial memory savings.

## 5.7 Common DP patterns

Be strong with:

### 1D DP

- Climbing stairs
- House robber
- Fibonacci variants
- Minimum cost paths
- Coin change

### 2D DP

- Grid paths
- Longest common subsequence
- Edit distance
- 0/1 knapsack

### Subsequence DP

- LIS
- LCS
- Maximum subsequence variants

### Partition DP

- Matrix-chain style problems
- Palindrome partitioning
- Interval partitioning

### State-machine DP

- Stock buy/sell
- Cooldown
- Transaction limits

### Bitmask DP

Use only when the state space permits it, typically for small `n`.

---

# 6. DSA Implementation Quality

Every algorithm implementation should aim for:

```text
Readable
Correct
Optimal for constraints
Edge-case safe
Testable
Complexity documented
```

Example structure:

```python
def solve(nums: list[int]) -> int:
    """
    Return the required result.

    Time: O(n)
    Space: O(1)
    """
    ...
```

Do not over-comment obvious code.

Comment the reasoning, invariant, or non-obvious optimization.

---

# 7. Machine Learning Engineering

Treat ML code as software, not just experimentation.

## 7.1 Reproducibility

Control:

- Random seeds where appropriate
- Dataset versions
- Dependency versions
- Model versions
- Configuration
- Feature definitions
- Training parameters

A model should be reproducible enough to diagnose changes.

## 7.2 Separate concerns

Use distinct layers for:

```text
Data ingestion
    ↓
Validation
    ↓
Preprocessing
    ↓
Feature engineering
    ↓
Training
    ↓
Evaluation
    ↓
Model registry/artifact storage
    ↓
Serving
    ↓
Monitoring
```

Avoid putting all ML logic inside one notebook or API route.

## 7.3 Configuration

Do not hard-code:

- Learning rate
- Batch size
- Model paths
- Database URLs
- API keys
- Environment-specific settings

Use configuration objects/environment variables.

Secrets must come from a secure secret-management mechanism.

## 7.4 Data validation

Validate:

- Schema
- Data types
- Missing values
- Duplicates
- Ranges
- Category validity
- Distribution changes
- Target leakage

Fail early when critical assumptions are violated.

## 7.5 Prevent data leakage

Never allow information from validation/test/future data to influence training.

Examples of risky leakage:

- Fitting scalers on the entire dataset before splitting
- Computing target-based features using future observations
- Selecting features using the test set
- Tuning hyperparameters directly against the test set

Correct pattern:

```text
Split
  ↓
Fit preprocessing on train
  ↓
Transform train/validation/test
```

---

# 8. MLOps Production Pipeline

A production ML system should consider:

```text
Data
 ↓
Validation
 ↓
Feature pipeline
 ↓
Training
 ↓
Evaluation
 ↓
Model validation gate
 ↓
Registry
 ↓
Deployment
 ↓
Inference
 ↓
Monitoring
 ↓
Retraining
```

## 8.1 Model validation gate

Before deployment, verify:

- Required metrics
- Regression against previous model
- Latency
- Memory usage
- Input schema compatibility
- Output validity
- Safety/business constraints

Do not automatically deploy a model merely because training succeeded.

## 8.2 Model versioning

Track:

- Model version
- Dataset version
- Code commit
- Feature version
- Configuration
- Training timestamp
- Evaluation metrics

A production prediction should be traceable back to the model and relevant configuration.

## 8.3 Experiment tracking

Record:

- Parameters
- Metrics
- Artifacts
- Dataset reference
- Code version
- Environment

Avoid relying on memory or notebook cell history.

## 8.4 CI/CD for ML

CI should test:

- Unit tests
- Data validation
- Model-loading behavior
- API contracts
- Static checks
- Formatting/linting
- Security checks

CD should support:

- Staging
- Model validation
- Controlled production rollout
- Rollback

## 8.5 Deployment strategies

Know when to use:

- Blue/green deployment
- Canary deployment
- Rolling deployment
- Shadow deployment
- A/B testing

For risky model changes, prefer controlled rollout over immediate full replacement.

---

# 9. FastAPI / ML API Standards

For ML APIs:

## Request flow

```text
Request
 ↓
Schema validation
 ↓
Authentication/authorization
 ↓
Input normalization
 ↓
Model inference
 ↓
Output validation
 ↓
Response
```

Keep routes thin.

Bad:

```python
@app.post("/predict")
def predict(request):
    # 300 lines of preprocessing,
    # model logic, database logic, etc.
```

Prefer:

```python
@app.post("/predict")
def predict(request: PredictionRequest) -> PredictionResponse:
    result = prediction_service.predict(request)
    return PredictionResponse(result=result)
```

## API requirements

Use:

- Pydantic models
- Explicit response schemas
- Proper HTTP status codes
- Timeouts
- Structured logging
- Request IDs when useful
- Dependency injection where appropriate
- Health/readiness endpoints
- Centralized exception handling

Do not expose stack traces or internal secrets to clients.

---

# 10. Testing Standards

Use layered testing.

## Unit tests

Test:

- Pure functions
- Edge cases
- Error conditions
- Algorithmic correctness

## Integration tests

Test:

- Database interactions
- Model loading
- API + service boundaries
- External service integration

## End-to-end tests

Test important production workflows.

## Algorithm tests

For DSA problems, include:

```text
empty input
single element
minimum constraint
maximum constraint
duplicates
already sorted
reverse sorted
negative values
all equal
```

When appropriate, compare an optimized solution against a brute-force reference on randomly generated small cases.

---

# 11. Security Rules

Never hard-code secrets.

Never commit:

```text
API keys
passwords
tokens
private credentials
.env files containing secrets
```

Validate untrusted input.

Use parameterized queries.

Avoid unsafe deserialization of untrusted data.

For ML systems, also consider:

- Prompt injection
- Data poisoning
- Model extraction
- Sensitive-data leakage
- Unsafe tool execution
- Malicious uploaded files

Apply least privilege.

---

# 12. Code Review Checklist

Before considering code complete, ask:

### Correctness

- Does it solve the actual requirement?
- Are edge cases handled?
- Are errors handled correctly?

### Readability

- Are names meaningful?
- Are functions focused?
- Is control flow understandable?

### Performance

- What is time complexity?
- What is space complexity?
- Are there avoidable O(n²) operations?
- Are repeated computations cached or eliminated?

### Maintainability

- Is logic duplicated?
- Are abstractions justified?
- Are constants/configuration separated?

### Testing

- Are important paths covered?
- Are failure cases tested?
- Are regression tests included?

### Production readiness

- Are logs useful?
- Are secrets protected?
- Is configuration externalized?
- Can the component be monitored?
- Can failures be diagnosed?
- Can the deployment be rolled back?

---

# 13. Codex Behavior

When modifying an existing repository:

1. Inspect the repository structure first.
2. Read relevant files before changing them.
3. Understand existing conventions.
4. Reuse existing utilities before creating duplicates.
5. Make the smallest safe change.
6. Do not rewrite unrelated code.
7. Preserve public APIs unless the task requires a breaking change.
8. Run relevant tests after modifications.
9. Run formatting/linting when configured.
10. Review the final diff for accidental changes.

When a test fails:

1. Read the failure carefully.
2. Identify the root cause.
3. Fix the underlying issue.
4. Re-run the smallest relevant test.
5. Re-run the broader suite when practical.

Never hide failing tests merely to obtain a green build.

---

# 14. Algorithm Answer Format

When asked to solve a DSA problem, prefer this structure:

```text
1. Approach
2. Why it works
3. Algorithm
4. Code
5. Time complexity
6. Space complexity
7. Edge cases
```

For DP, additionally include:

```text
State:
Transition:
Base case:
Iteration/order:
Space optimization:
```

For graph problems, additionally identify:

```text
Graph representation:
Traversal:
Visited strategy:
Complexity:
```

For binary search, explicitly identify the monotonic property and search invariant.

---

# 15. Final Quality Gate

Before returning code, mentally run this checklist:

```text
[ ] Requirement understood
[ ] Correct algorithm selected
[ ] Edge cases considered
[ ] Time complexity acceptable
[ ] Space complexity acceptable
[ ] Names are clear
[ ] Functions are focused
[ ] No unnecessary duplication
[ ] Errors are handled
[ ] Secrets are protected
[ ] Tests added/updated
[ ] Existing conventions preserved
[ ] Relevant tests executed
[ ] Final diff reviewed
```

The default engineering standard is:

> Write the clearest correct solution first, then make it efficient, testable, observable, and production-ready.
