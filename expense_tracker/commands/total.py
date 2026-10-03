"""The ``total`` command: show total spending."""

from __future__ import annotations

from ..money import format_amount

NAME = "total"
HELP = "Show total spending"


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--category",
        default=None,
        help="Only total expenses in this category",
    )


def handle(args, store) -> int:
    """Calculate and print the total of expenses.
    
    Args:
        args: Parsed command-line arguments with optional category filter.
        store: The expense store to load expenses from.
        
    Returns:
        Process exit code (0 on success).
    """
    expenses = store.load()
    
    # Apply category filter if specified
    if args.category is not None:
        expenses = [e for e in expenses if e.category == args.category]
    
    # Sum all amounts in integer cents, then format for display
    total_cents = sum(e.amount_cents for e in expenses)
    print(format_amount(total_cents))
    return 0
