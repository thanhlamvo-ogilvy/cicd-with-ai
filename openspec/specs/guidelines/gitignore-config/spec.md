# Gitignore Config

> Root `.gitignore` rules preventing unnecessary files from being tracked by Git.

## Required Exclusions

**Python bytecode**
- `__pycache__/`, `*.pyc`, `*.pyo`

**Virtual environments**
- `.venv/`, `venv/`, `env/`

**Secrets**
- `.env` — MUST be excluded; `.env.example` MUST be tracked
- Never commit secrets to Git

**Tool caches**
- `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.coverage`

**Build artifacts**
- `dist/`, `build/`, `*.egg-info/`

**IDE & OS files**
- `.idea/`, `.DS_Store`, `Thumbs.db`
- `.vscode/` — exclude personal settings; shared workspace settings (`.vscode/settings.json`) MAY be tracked if intentional
