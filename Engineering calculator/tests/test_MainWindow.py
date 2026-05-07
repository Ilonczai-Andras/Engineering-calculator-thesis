import sys
import os
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from GUI.MainWindow import Window

@pytest.fixture
def app(qtbot):
    """Fixture to initialize the main window."""
    test_app = Window()
    qtbot.addWidget(test_app)
    return test_app

def test_initial_state(app):
    """Test if the calculator starts with 0."""
    assert app._get() == "0"

def test_addition(app, qtbot):
    """Test basic addition."""
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "3"

def test_subtraction(app, qtbot):
    """Test basic subtraction."""
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.minusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "2"

def test_multiplication(app, qtbot):
    """Test basic multiplication."""
    qtbot.mouseClick(app.Button_4, Qt.LeftButton)
    qtbot.mouseClick(app.multiplyButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_6, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "24"

def test_division(app, qtbot):
    """Test basic division."""
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.divideButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "4"

def test_division_by_zero(app, qtbot):
    """Test dividing by zero returns an ERROR."""
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.divideButton, Qt.LeftButton)
    qtbot.mouseClick(app.zeroButton, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "ERROR"

def test_clear(app, qtbot):
    """Test the clear (C) button."""
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.clearButton, Qt.LeftButton)
    assert app._get() == "0"

def test_delete(app, qtbot):
    """Test the delete (Backspace/DEL) button."""
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.deleteButton, Qt.LeftButton)
    assert app._get() == "1"
    qtbot.mouseClick(app.deleteButton, Qt.LeftButton)
    assert app._get() == "0"

def test_decimal(app, qtbot):
    """Test adding a decimal point."""
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    assert app._get() == "1.2"

def test_multiple_decimals_prevented(app, qtbot):
    """Test that multiple decimals in a single number are ignored."""
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    assert app._get() == "1.2"

def test_quadrat(app, qtbot):
    """Test the square (x²) function."""
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.quadratButton, Qt.LeftButton)
    assert app._get() == "25"

def test_sqrt(app, qtbot):
    """Test the square root (√) function."""
    qtbot.mouseClick(app.Button_9, Qt.LeftButton)
    qtbot.mouseClick(app.sqrtButton, Qt.LeftButton)
    assert app._get() == "3"

def test_sqrt_negative(app, qtbot):
    """Test taking square root of a negative number throws an ERROR."""
    qtbot.mouseClick(app.Button_9, Qt.LeftButton)
    qtbot.mouseClick(app.plusMinusButton, Qt.LeftButton)
    qtbot.mouseClick(app.sqrtButton, Qt.LeftButton)
    assert app._get() == "ERROR"

def test_one_per_x(app, qtbot):
    """Test the reciprocal (1/x) function."""
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.onePerXButton, Qt.LeftButton)
    assert app._get() == "0.5"

def test_one_per_x_zero(app, qtbot):
    """Test dividing 1 by 0 using 1/x throws an ERROR."""
    qtbot.mouseClick(app.zeroButton, Qt.LeftButton)
    qtbot.mouseClick(app.onePerXButton, Qt.LeftButton)
    assert app._get() == "ERROR"

def test_plus_minus(app, qtbot):
    """Test the +/- toggling logic."""
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.plusMinusButton, Qt.LeftButton)
    assert app._get() == "-5"
    qtbot.mouseClick(app.plusMinusButton, Qt.LeftButton)
    assert app._get() == "5"

def test_modulo(app, qtbot):
    """Test the % modulo button logic."""
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.percentageButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "1"

def test_keyboard_input(app, qtbot):
    """Test that numbers and operators typed via the keyboard simulate button presses correctly."""
    qtbot.keyClicks(app, "12+34")
    qtbot.keyClick(app, Qt.Key_Return)
    assert app._get() == "46"

def test_chain_operations(app, qtbot):
    """Test chaining expressions with calculations."""
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "5"
    
    qtbot.mouseClick(app.multiplyButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "10"

def test_error_recovery(app, qtbot):
    """Test if pressing numbers after an ERROR state successfully resets the screen."""
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.divideButton, Qt.LeftButton)
    qtbot.mouseClick(app.zeroButton, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "ERROR"
    
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    assert app._get() == "5"

def test_copy_paste(app, qtbot):
    """Test copying to and pasting from clipboard."""
    # Simulate pasting from the clipboard
    app.clipboard.setText("42")
    qtbot.keyClick(app, Qt.Key_V, modifier=Qt.ControlModifier)
    assert app._get() == "42"

    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    
    assert app._get() == "50"
    
    # Simulate copying to the clipboard
    qtbot.keyClick(app, Qt.Key_C, modifier=Qt.ControlModifier)
    assert app.clipboard.text() == "50"

def test_decimal_on_result(app, qtbot):
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    assert app._get() == "0."

# ── Input building ────────────────────────────────────────────────────────────

def test_multidigit_number(app, qtbot):
    """Entering multiple digits builds the correct number (not just single digits)."""
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    assert app._get() == "123"


def test_leading_zero_replaced(app, qtbot):
    """Pressing a digit when display shows '0' replaces it, not appends."""
    assert app._get() == "0"
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    assert app._get() == "5"


# ── Decimal arithmetic ────────────────────────────────────────────────────────

def test_decimal_addition(app, qtbot):
    """1.5 + 2.5 should equal 4, not 4.0."""
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_2, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "4"


def test_decimal_second_operand(app, qtbot):
    """Decimal point in the second operand: 3 + 1.5 = 4.5."""
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_1, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "4.5"


def test_decimal_not_duplicated_after_operator(app, qtbot):
    """
    A dot added after an operator starts a new decimal segment.
    e.g. '3+.' should become '3+.' and then '3+.5' is valid.
    """
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)
    qtbot.mouseClick(app.decimalPointButton, Qt.LeftButton)   # second dot ignored
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "3.5"


# ── Negative numbers ──────────────────────────────────────────────────────────

def test_negative_number_arithmetic(app, qtbot):
    """Arithmetic with a negated number: -3 + 8 = 5."""
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    qtbot.mouseClick(app.plusMinusButton, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "5"


def test_plus_minus_ignored_on_expression(app, qtbot):
    """
    +/- does nothing when the display holds an expression (not a bare number).
    e.g. '5+3' can't be toggled as a unit.
    """
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    before = app._get()           # "5+3"
    qtbot.mouseClick(app.plusMinusButton, Qt.LeftButton)
    assert app._get() == before   # unchanged


# ── State transitions ─────────────────────────────────────────────────────────

def test_digit_after_result_starts_fresh(app, qtbot):
    """After pressing =, typing a digit should start a new expression."""
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.multiplyButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_5, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "25"

    qtbot.mouseClick(app.Button_6, Qt.LeftButton)
    assert app._get() == "6"      # fresh start, not "256"


def test_operator_after_result_chains(app, qtbot):
    """After pressing =, an operator should chain from the result."""
    qtbot.mouseClick(app.Button_4, Qt.LeftButton)
    qtbot.mouseClick(app.plusButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_6, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "10"

    qtbot.mouseClick(app.minusButton, Qt.LeftButton)   # chains: "10−"
    qtbot.mouseClick(app.Button_3, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "7"


def test_delete_after_result_resets(app, qtbot):
    """DEL immediately after = should reset display to 0, not strip a digit."""
    qtbot.mouseClick(app.Button_9, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "9"

    qtbot.mouseClick(app.deleteButton, Qt.LeftButton)
    assert app._get() == "0"


def test_repeated_equals(app, qtbot):
    """Pressing = multiple times on a bare number should keep returning it."""
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "8"
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "8"


def test_clear_resets_after_result(app, qtbot):
    """C should always reset to 0, including right after a calculation."""
    qtbot.mouseClick(app.Button_7, Qt.LeftButton)
    qtbot.mouseClick(app.multiplyButton, Qt.LeftButton)
    qtbot.mouseClick(app.Button_7, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "49"

    qtbot.mouseClick(app.clearButton, Qt.LeftButton)
    assert app._get() == "0"


def test_error_then_operator_starts_fresh(app, qtbot):
    """After an ERROR, pressing an operator (not just a digit) also starts fresh."""
    qtbot.mouseClick(app.Button_8, Qt.LeftButton)
    qtbot.mouseClick(app.divideButton, Qt.LeftButton)
    qtbot.mouseClick(app.zeroButton, Qt.LeftButton)
    qtbot.mouseClick(app.equalButton, Qt.LeftButton)
    assert app._get() == "ERROR"

    qtbot.mouseClick(app.plusButton, Qt.LeftButton)   # should not crash / corrupt
    # display should be "+" or "0+" — either is acceptable, but must not be "ERROR"
    assert app._get() != "ERROR"


# ── Keyboard edge cases ───────────────────────────────────────────────────────

def test_keyboard_backspace(app, qtbot):
    """Backspace key should behave the same as the DEL button."""
    qtbot.keyClicks(app, "123")
    assert app._get() == "123"
    qtbot.keyClick(app, Qt.Key_Backspace)
    assert app._get() == "12"
    qtbot.keyClick(app, Qt.Key_Backspace)
    assert app._get() == "1"
    qtbot.keyClick(app, Qt.Key_Backspace)
    assert app._get() == "0"


def test_keyboard_delete_key_clears(app, qtbot):
    """The Delete key should behave the same as the C button."""
    qtbot.keyClicks(app, "99")
    assert app._get() == "99"
    qtbot.keyClick(app, Qt.Key_Delete)
    assert app._get() == "0"


def test_keyboard_subtraction(app, qtbot):
    """Minus key via keyboard should produce correct result."""
    qtbot.keyClicks(app, "9-4")
    qtbot.keyClick(app, Qt.Key_Return)
    assert app._get() == "5"


def test_keyboard_multiplication(app, qtbot):
    """Asterisk key via keyboard should multiply correctly."""
    qtbot.keyClicks(app, "6*7")
    qtbot.keyClick(app, Qt.Key_Return)
    assert app._get() == "42"


def test_keyboard_division(app, qtbot):
    """Slash key via keyboard should divide correctly."""
    qtbot.keyClicks(app, "9/3")
    qtbot.keyClick(app, Qt.Key_Return)
    assert app._get() == "3"


# ── Known float precision behaviour ──────────────────────────────────────────

def test_float_precision_documented(app, qtbot):
    """
    0.1 + 0.2 does NOT equal 0.3 due to IEEE-754 float representation.
    This test documents the known behaviour rather than asserting "0.3".
    If a future version adds rounding, update this test accordingly.
    """
    qtbot.keyClicks(app, "0.1+0.2")
    qtbot.keyClick(app, Qt.Key_Return)
    result = app._get()
    assert result != "0.3"          # floating-point artefact is expected
    assert result.startswith("0.3") # ...but it should be close
