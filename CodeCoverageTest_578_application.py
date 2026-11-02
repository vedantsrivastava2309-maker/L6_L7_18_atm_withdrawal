import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


def test_successful_savings_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_invalid_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 100, "student", True)


def test_invalid_nonpositive_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_invalid_non_hundred_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


def test_daily_limit_exceeded():
    assert withdraw(60000, 25100, "savings", True) == "limit exceeded"


def test_non_own_bank_fee():
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_non_own_bank_large_withdrawal_fee():
    assert withdraw(20000, 11000, "savings", False) == 8970


def test_insufficient_funds():
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_wrong_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


def test_card_blocked_after_third_attempt():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_card_already_blocked():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_note_breakup_with_200_notes():
    assert note_breakup(1200) == (2, 1, 0)


def test_note_breakup_without_200_notes():
    assert note_breakup(1600) == (3, 0, 1)


def test_invalid_note_breakup():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)
