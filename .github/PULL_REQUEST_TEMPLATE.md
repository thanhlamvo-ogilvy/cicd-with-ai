## Description

<!-- A clear and concise description of the changes introduced by this PR. -->

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactoring / code quality improvement
- [ ] Documentation update
- [ ] CI/CD or configuration change

## AI-Generated Code Declaration

- [ ] This PR contains **no** AI-generated code
- [ ] This PR contains AI-generated code. I have reviewed it for correctness, security, and style.

If AI-generated code is present, describe what was generated and how it was reviewed:

<!-- e.g. "Used Copilot to scaffold the CRUD service. Manually verified all edge cases and replaced
     the generated SQL with parameterised ORM queries." -->

## Pre-Merge Checklist

- [ ] My changes follow the coding conventions in `.github/copilot-review-instructions.md`
- [ ] I have added/updated tests that cover my changes
- [ ] All existing tests pass locally (`pytest`)
- [ ] I have run `ruff check . --fix` and `ruff format .` (or pre-commit hooks)
- [ ] I have run `bandit -r app/` and addressed any findings
- [ ] I have updated the relevant documentation (README, docstrings, etc.)
- [ ] No secrets, credentials, or sensitive data are committed
- [ ] Database migrations have been generated and reviewed (if schema changed)
