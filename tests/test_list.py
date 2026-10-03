from expense_tracker.commands import add, list_cmd
from tests.conftest import args, make_store


def _seed(store):
    add.handle(args(amount="10.00", category="food", date="2026-01-01", note=""), store)
    add.handle(args(amount="20.00", category="travel", date="2026-01-02", note=""), store)
    add.handle(args(amount="5.00", category="food", date="2026-01-03", note=""), store)


def test_list_all(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(
        args(category=None, since=None, until=None), store
    )
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 3


def test_list_filtered_by_category(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    list_cmd.handle(args(category="food", since=None, until=None), store)
    out = capsys.readouterr().out
    assert "food" in out
    assert "travel" not in out


def test_list_empty(tmp_path, capsys):
    store = make_store(tmp_path)
    code = list_cmd.handle(args(category=None, since=None, until=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert "No expenses found." in out


def test_list_with_since_and_until(tmp_path, capsys):
    """Filter with both --since and --until bounds (inclusive)."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(
        args(category=None, since="2026-01-02", until="2026-01-02"), store
    )
    out = capsys.readouterr().out
    assert code == 0
    assert "travel" in out  # only 2026-01-02
    assert out.count("\n") == 1


def test_list_with_since_only(tmp_path, capsys):
    """Filter with only --since bound (inclusive)."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = list_cmd.handle(args(category=None, since="2026-01-02", until=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 2  # 2026-01-02 and 2026-01-03
    assert "2026-01-01" not in out


def test_list_with_until_only(tmp_path, capsys):
    """Filter with only --until bound (inclusive)."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = list_cmd.handle(args(category=None, since=None, until="2026-01-02"), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 2  # 2026-01-01 and 2026-01-02
    assert "2026-01-03" not in out


def test_list_with_neither_since_nor_until(tmp_path, capsys):
    """Neither bound specified (original behavior)."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = list_cmd.handle(args(category=None, since=None, until=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 3  # all three expenses


def test_list_with_invalid_since_date(tmp_path, capsys):
    """Invalid ISO 8601 date in --since exits with code 1 and prints error."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = list_cmd.handle(args(category=None, since="2026-13-01", until=None), store)
    out = capsys.readouterr().out
    assert code == 1
    assert "error:" in out


def test_list_with_invalid_until_date(tmp_path, capsys):
    """Invalid ISO 8601 date in --until exits with code 1 and prints error."""
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()
    code = list_cmd.handle(args(category=None, since=None, until="not-a-date"), store)
    out = capsys.readouterr().out
    assert code == 1
    assert "error:" in out
