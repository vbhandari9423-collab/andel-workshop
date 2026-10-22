# expense-tracker

A command-line expense tracker. Records expenses to a local JSON file and
lists, summarises and deletes them. Standard library only.

## Commands

| Task                  | Command                                 |
| :-------------------- | :-------------------------------------- |
| Run the app           | `python -m expense_tracker <command>`   |
| Full test suite       | `pytest`                                |
| One test file         | `pytest tests/test_add.py -v`           |
| Lint and format check | `ruff check . && ruff format --check .` |

Install dev dependencies with `pip install -r requirements-dev.txt`.

## Rules and conventions

- Money is an integer number of cents everywhere, including intermediate
  arithmetic. Parse with `money.parse_amount`, display with
  `money.format_amount`. A float anywhere in a money path is a bug, even when
  the test passes.
- Dates are ISO 8601 strings in `YYYY-MM-DD` form. Validate with
  `date.fromisoformat` before storing. Never store a raw user string.
- The app targets Python 3.10 and imports nothing outside the standard library.
  Adding a runtime dependency is a conversation, not a commit.
- Changing the shape of `expenses.json` requires a migration note in the README.
- Conventional Commits. Pull request descriptions say what changed, why, and how
  it was verified.

## Boundaries

- Storage goes through `storage.py`. No module reads or writes the JSON file
  directly.
- Do not add third-party dependencies without asking.

## Definition of done

A change is done when `pytest` passes, `ruff check .` is clean, the new
behaviour has a test that fails without the change, and the README is updated
if the way you run or configure the tool changed.