# Shared Git Workflow

> Git workflow and commit message format standards shared across all workspaces.

## Branching

- Never commit directly to `main` — always create a feature branch and open a PR
- Branch names MUST use descriptive prefixes: `feat/`, `fix/`, `hotfix/`, `release/`
- Keep branches short-lived — merge or close within days, not weeks; flag stale branches after one week of inactivity
- Each PR MUST contain one logical change — multi-topic PRs MUST be flagged and split

## Commit Message Format

All commit messages MUST follow this structured release notes format:

```
[Primary Change Description]; [Secondary Changes] & more…

{PackageName}
- [Action verb] [concise description ≤ 120 chars]
- [Action verb] [another change description]

(No dependency updates.)
```

Rules:
- **Title line** — lead with the most newsworthy change; end with `& more…` if multi-topic; no trailing period
- **Group changes** under `{PkgName}` headers (e.g., `{Backend}`, `{Frontend}`, `{CI}`, `{Docs}`, `{Dependencies}`)
- **Bullets** — present-tense action verb (`Add`, `Fix`, `Refactor`, `Improve`, `Remove`); ≤ 120 chars; no trailing period
- **No dependency updates** — include the literal line `(No dependency updates.)` when no deps changed
- **Body line limit** — body (all lines after title) MUST NOT exceed 10 lines; reference an issue or PR link (`See #123`) for additional context
- **No attribution tags** — NEVER include `Co-authored-by:` trailers or AI generator attribution

## Merge Strategy

- Merges to `main` MUST use rebase or squash-merge — never a merge commit
- Every commit that passes CI MUST be potentially deployable (Continuous Delivery)
