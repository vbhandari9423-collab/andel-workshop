"""The ``list`` command: show recorded expenses."""

from __future__ import annotations

from datetime import date as date_cls

from ..money import format_amount

NAME = "list"
HELP = "List expenses, optionally filtered by category"


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--category",
        default=None,
        help="Only show expenses in this category",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Only show expenses on or after this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="Only show expenses on or before this date (YYYY-MM-DD)",
    )


def _validate_date(value: str) -> str:
    """Validate and return an ISO 8601 date string.
    
    Args:
        value: A date string that should be in YYYY-MM-DD format.
        
    Returns:
        The validated date string.
        
    Raises:
        ValueError: If the date is malformed.
    """
    date_cls.fromisoformat(value)
    return value


def handle(args, store) -> int:
    # Validate and parse date bounds
    since_date = None
    until_date = None
    
    if args.since is not None:
        try:
            since_date = _validate_date(args.since)
        except ValueError as exc:
            print(f"error: invalid --since date: {exc}")
            return 1
    
    if args.until is not None:
        try:
            until_date = _validate_date(args.until)
        except ValueError as exc:
            print(f"error: invalid --until date: {exc}")
            return 1
    
    expenses = store.load()
    
    # Apply category filter
    if args.category is not None:
        expenses = [e for e in expenses if e.category == args.category]
    
    # Apply date filters (inclusive bounds)
    if since_date is not None:
        expenses = [e for e in expenses if e.date >= since_date]
    if until_date is not None:
        expenses = [e for e in expenses if e.date <= until_date]

    if not expenses:
        print("No expenses found.")
        return 0

    for e in expenses:
        note = f"  ({e.note})" if e.note else ""
        print(f"#{e.id}  {e.date}  {format_amount(e.amount_cents):>10}  {e.category}{note}")
    return 0
