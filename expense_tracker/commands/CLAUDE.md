# Commands

This folder contains the command implementations for the expense tracker.

## Files

- `add.py` — adds a new expense entry
- `delete.py` — removes an expense by id
- `list_cmd.py` — lists recorded expenses
- `summary.py` — shows a summary grouped by category
- `total.py` — shows the overall total

## Conventions

- Keep command logic focused on CLI behavior.
- Validate arguments before writing to storage.
- Use the shared storage layer for all JSON reads and writes.
- Preserve the existing money and date conventions used by the app.
