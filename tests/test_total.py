"""Tests for the ``total`` command."""

from expense_tracker.commands import add, total
from tests.conftest import args, make_store


def _seed(store):
    """Seed the store with test expenses."""
    add.handle(args(amount="10.00", category="food", date="2026-01-01", note=""), store)
    add.handle(args(amount="20.00", category="travel", date="2026-01-02", note=""), store)
    add.handle(args(amount="5.00", category="food", date="2026-01-03", note=""), store)


def test_total_all_expenses(tmp_path, capsys):
    """Total of all expenses is formatted correctly."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = total.handle(args(category=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert "$35.00" in out.strip()


def test_total_filtered_by_category(tmp_path, capsys):
    """Total filtered by category."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = total.handle(args(category="food"), store)
    out = capsys.readouterr().out
    assert code == 0
    assert "$15.00" in out.strip()  # 10.00 + 5.00


def test_total_empty(tmp_path, capsys):
    """Total of no expenses shows $0.00."""
    store = make_store(tmp_path)
    code = total.handle(args(category=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert "$0.00" in out.strip()


def test_total_category_with_no_match(tmp_path, capsys):
    """Total of non-matching category shows $0.00."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = total.handle(args(category="nonexistent"), store)
    out = capsys.readouterr().out
    assert code == 0
    assert "$0.00" in out.strip()
