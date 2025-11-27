## Copilot / AI agent instructions — Healthy-Food-Recipe-Planning-

Purpose: provide concise, actionable context so an AI coding assistant can be immediately productive in this repository.

1) Big picture (what to read first)
- The project is a small web app split into three logical parts (described in `README.md`):
  - Frontend: `frontend/` — static pages (`index.html`, `dashboard.html`, `login.html`) and client JS under `frontend/scripts/`.
  - Backend: `backend/` — application entry `app.py`, recommendation logic in `engine.py`, data helpers in `data_loader.py`.
  - Data & analysis: `data/recipes_600dataset.csv` and `data_exploration.ipynb` for dataset inspection and prototypes.

  Data flow (inferred from README structure):
  - User profile & pantry -> backend engine filters/ ranks recipes from `data/recipes_600dataset.csv` -> API returns JSON -> frontend displays.

2) Key files & current state (note gaps found)
- `README.md` — project overview and module responsibilities (use this to understand intent).
- `data/recipes_600dataset.csv` — canonical dataset for recipe filtering and scoring.
- `data_exploration.ipynb` — exploratory notebook; good place to extract feature engineering and nutritional calculations.
- `frontend/` — static UI; `frontend/scripts/app.js` currently exists but is empty (no client logic found).
- `backend/app.py`, `backend/engine.py`, `backend/data_loader.py` — all present but currently empty. Treat these as the primary implementation targets.
- `backend/requirements.txt` — present but empty; no explicit dependency list discovered.

3) Practical guidance for edits
- If implementing backend endpoints, follow a minimal contract:
  - Entry: `backend/app.py` should expose an HTTP API (simple JSON endpoints) or a CLI runner. If you add Flask/FastAPI, list packages in `backend/requirements.txt` and create a small `if __name__ == '__main__'` runner.
  - Core engine API (suggested, confirm with owner):
    ```py
    # backend/engine.py (suggested signature)
    def rank_recipes(user_profile: dict, pantry: list) -> list:
        """Return a ranked list of recipe dicts (id, score, match_reason).
        Input shapes: user_profile contains goals/allergies/preferences; pantry is list of ingredient names.
        """
    ```
  - Data loader (suggested): `backend/data_loader.py` should expose `load_recipes(path)` returning a pandas DataFrame or list of dicts. Use `data/recipes_600dataset.csv` for examples.

4) Project-specific conventions & patterns to preserve
- Module responsibilities are split as in the README — keep the engine purely algorithmic (no UI code), and keep the frontend purely presentational.
- Name things explicitly: functions like `rank_recipes`, `load_recipes`, and `get_user_profile` make interfaces easy to discover and test.

5) Integration points & external dependencies
- The repository currently has no declared dependencies. If you add frameworks (Flask/FastAPI, pandas, scikit-learn), add them to `backend/requirements.txt` and document run steps in `README.md`.
- Frontend is static HTML/JS — communication between front and back should be via JSON endpoints under `/api/*` (recommended).

6) Quick onboarding checklist for an AI agent
- Read `README.md` and `data_exploration.ipynb` to extract feature logic (how nutrition is calculated).
- Inspect `data/recipes_600dataset.csv` to understand schema (ingredient names, nutrition columns).
- Implement `backend/data_loader.py` first (simple CSV loader), then `backend/engine.py` with a small `rank_recipes` function, then wire an endpoint in `backend/app.py`.
- Add packages to `backend/requirements.txt` and a short run note in `README.md` when you add runtime dependencies.

7) Edge cases and tests to create (practical, repo-focused)
- Empty pantry -> `rank_recipes` should return an empty list or well-documented fallback.
- Missing nutrition columns in CSV -> raise a clear error from `load_recipes`.
- Encoding/CSV parsing problems -> prefer `utf-8` with fallback; document the expected CSV columns in `backend/data_loader.py` docstring.

8) Actionable examples to copy-paste
- Example return contract from `rank_recipes`:
  ```json
  [{"id": 123, "title": "Oat Pancake", "score": 0.87, "match_reason": "matches pantry: oats, milk"}]
  ```

9) Notes & constraints discovered
- There are no CI, tests, or run scripts in the repo. Avoid making assumptions about server framework; prefer to add minimal, explicit choices and document them.
- Many backend files are empty — treat them as TODOs and keep changes small and well-documented.

If any of these assumptions are incorrect (for example, you want a specific framework or test runner), tell me which choices you prefer and I will update the instructions and optionally implement the initial scaffolding (loader, engine, endpoint) and tests.

---
Please review this draft and tell me which sections need more detail or which conventions you want the agent to follow exactly (framework, test framework, preferred return shapes). I'll iterate quickly.
