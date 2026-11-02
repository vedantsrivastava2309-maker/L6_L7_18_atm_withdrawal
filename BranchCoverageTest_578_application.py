import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

# WITHDRAW: test each decision and boundary condition.

def test_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(10000, 100, "business", True)

def test_amount_zero_is_invalid():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 0, "savings", True)

def test_amount_not_multiple_of_100_is_invalid():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 150, "savings", True)

def test_savings_limit_exceeded():
    assert withdraw(50000, 25100, "savings", True) == "limit exceeded"

def test_current_account_withdrawal_at_limit():
    assert withdraw(60000, 50000, "current", True) == 10000

def test_own_bank_withdrawal_has_no_fee():
    assert withdraw(5000, 1000, "savings", True) == 4000

def test_other_bank_standard_fee():
    assert withdraw(5000, 1000, "savings", False) == 3980

def test_other_bank_large_withdrawal_extra_fee():
    assert withdraw(20000, 11000, "savings", False) == 8970

def test_insufficient_balance_including_fee():
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"

# PIN CHECK: test blocked, correct, retry, and final failed attempt.

def test_pin_card_already_blocked():
    assert pin_check(1234, 1234, 3) == "card blocked"

def test_pin_correct_before_blocking():
    assert pin_check(1234, 1234, 0) == "ok"

def test_wrong_pin_allows_retry():
    assert pin_check(1111, 1234, 0) == "retry"

def test_wrong_pin_on_last_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"

# NOTE BREAKUP: test invalid amount and both remaining-value branches.

def test_note_breakup_with_200_notes():
    assert note_breakup(1200) == (2, 1, 0)

def test_note_breakup_without_200_notes():
    assert note_breakup(1600) == (3, 0, 1)

def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(155)
