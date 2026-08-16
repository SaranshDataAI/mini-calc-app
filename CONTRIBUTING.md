# Contributing Workflow

Same rules as before, adapted for a project with a frontend and a
backend. This file is the actual point of the project.

## 1. Never commit directly to `main`

Every change goes through a branch and a Pull Request. No exceptions,
even for a one-line fix. This is the habit we're building.

## 2. Suggested ownership (to start)

- One person owns `backend/`
- The other owns `frontend/`

This isn't a hard rule — it's just a starting point so you each have a
clear "home" while learning. Once branching feels natural, mix it up
on purpose so you both touch both sides.

## 3. Branch naming

`<type>/<short-description>`, e.g.:
- `feature/add-history-endpoint`
- `feature/calculator-ui`
- `fix/divide-by-zero-crash`

Types: `feature`, `fix`, `docs`, `chore`.

## 4. Commit messages

`<type>: <what changed, present tense>`, e.g.
`feature: add square root operation to backend`

## 5. The workflow, step by step

1. `git pull origin main`
2. `git checkout -b feature/your-thing`
3. Do the work, commit as you go.
4. `git push origin feature/your-thing`
5. Open a PR on GitHub targeting `main`.
6. The other person reviews — actually read the diff, leave at least
   one comment.
7. Once approved: **Squash and merge**.
8. Delete the branch.

## 6. Where you'll naturally hit conflicts on THIS project

Adding a new operation (say, square root) touches both sides:
- Backend: add to the `OPERATIONS` dict in `main.py`
- Frontend: add an `<option>` in `index.html` and handle it in
  `script.js`

If you both grab "add square root" as separate branches without
talking first, you'll get a real conflict when one of you tries to
merge after the other. That's expected — work through it using the
conflict resolution steps from the original CONTRIBUTING guide:

1. `git pull origin main` on your branch to surface the conflict.
2. Open the file, look for `<<<<<<<` / `=======` / `>>>>>>>` markers.
3. Decide what the merged result should actually look like.
4. Remove the markers, `git add`, `git commit`, push, continue the PR.

## What's coming later

- GitHub Issues instead of an informal task list
- GitHub Actions running `pytest` on every PR automatically
- Branch protection requiring review before merge
- Maybe a real database instead of SQLite, once the basics are solid
