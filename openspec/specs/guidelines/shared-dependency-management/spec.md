# Shared Dependency Management

> Dependency management rules shared across all workspaces.

## Adding Dependencies

- Every new dependency MUST be justified — prefer stdlib or existing deps over adding new ones
- PR description MUST explain why the new dependency is needed and why existing options cannot suffice
- Check the license for compatibility before adding any dependency

## Version Pinning

- All dependencies MUST be pinned in lockfiles (`package-lock.json`, `pyproject.toml` constraints) for reproducible builds
- Lockfile MUST be updated and committed in the same PR as the dependency change

## Vulnerability Scanning

- CI MUST run vulnerability scanning on every PR:
  - Python: `pip-audit`
  - Frontend: `npm audit`
- Known CVEs in dependencies MUST block merge

## Update Cadence

- Dependencies MUST be updated regularly — small, frequent updates are safer than large, infrequent ones
- Automated dependency update tooling (Dependabot, Snyk, or equivalent) MUST be enabled on the repository
