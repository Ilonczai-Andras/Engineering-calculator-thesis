from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
import sys
import UI_files.Main_GUI as Main_GUI
import re
import math


# ── Symbol translation ────────────────────────────────────────────────────────

OP_DISPLAY = {"*": "×", "/": "÷", "-": "−"}
OP_EVAL    = {"×": "*", "÷": "/", "−": "-"}


def _to_eval(expr: str) -> str:
    for sym, op in OP_EVAL.items():
        expr = expr.replace(sym, op)
    return expr


def _fmt(value) -> str:
    """Strip pointless .0 suffix (4.0 → '4')."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


# ── Main window ───────────────────────────────────────────────────────────────

class Window(QMainWindow, Main_GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.outputLabel.setReadOnly(True)
        self.outputLabel.setFocusPolicy(Qt.NoFocus)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.clipboard = QApplication.clipboard()
        self._after_result = False

        # ── Button connections ────────────────────────────────────────────────
        self.clearButton.clicked.connect(lambda: self.press_it("C"))
        self.deleteButton.clicked.connect(self.delete)
        self.decimalPointButton.clicked.connect(self.dot)
        self.equalButton.clicked.connect(self.equal)
        self.plusMinusButton.clicked.connect(self.plus_minus)
        self.percentageButton.clicked.connect(lambda: self.press_it("%"))

        self.plusButton.clicked.connect(lambda: self.press_it("+"))
        self.minusButton.clicked.connect(lambda: self.press_it("-"))
        self.multiplyButton.clicked.connect(lambda: self.press_it("*"))
        self.divideButton.clicked.connect(lambda: self.press_it("/"))

        self.quadratButton.clicked.connect(self.quadrat)
        self.sqrtButton.clicked.connect(self.sqrt_func)
        self.onePerXButton.clicked.connect(self.one_per_x)

        # Numeric buttons
        self.Button_0 = self.zeroButton   # alias for uniform loop below
        for digit, button in [
            ("0", self.zeroButton),
            ("1", self.Button_1),
            ("2", self.Button_2),
            ("3", self.Button_3),
            ("4", self.Button_4),
            ("5", self.Button_5),
            ("6", self.Button_6),
            ("7", self.Button_7),
            ("8", self.Button_8),
            ("9", self.Button_9),
        ]:
            button.clicked.connect(
                (lambda d: lambda: self.press_it(d))(digit)
            )

    # ── Display helpers ───────────────────────────────────────────────────────

    def _get(self) -> str:
        return self.outputLabel.text()

    def _set(self, value: str):
        self.outputLabel.setText(value)

    def _is_error(self) -> bool:
        return self._get() == "ERROR"

    def _reset_if_needed(self):
        """Clear the display when the first new input arrives after a result."""
        if self._after_result:
            self._set("0")
            self._after_result = False

    # ── Core input handler ────────────────────────────────────────────────────

    def press_it(self, raw: str):
        """Main entry point for all digit / operator / special key input."""

        if raw == "C":
            self._set("0")
            self._after_result = False
            return

        display = OP_DISPLAY.get(raw, raw)   # e.g. "*" → "×"

        if self._is_error():
            self._set(display)
            self._after_result = False
            return

        if self._after_result:
            if display.isdigit():
                self._set(display)
                self._after_result = False
                return
            else:
                self._after_result = False

        current = self._get()

        if current == "0" and display.isdigit():
            self._set(display)
        else:
            self._set(current + display)

    def dot(self):
        if self._is_error():
            self._set("0.")
            self._after_result = False
            return
        self._reset_if_needed()
        current = self._get()
        last_num = re.split(r"[+×÷−]", current)[-1]
        if "." not in last_num:
            self._set(current + ".")

    def delete(self):
        if self._is_error() or self._after_result:
            self._set("0")
            self._after_result = False
            return
        current = self._get()
        self._set(current[:-1] if len(current) > 1 else "0")

    def plus_minus(self):
        current = self._get()
        if self._is_error():
            return
        try:
            float(current)
            if current.startswith("-"):
                self._set(current[1:])
            else:
                self._set("-" + current)
        except ValueError:
            pass

    # ── Calculation actions ───────────────────────────────────────────────────

    def equal(self):
        try:
            result = eval(_to_eval(self._get()))
            self._set(_fmt(result))
        except Exception as exc:
            print(f"eval error: {exc}")
            self._set("ERROR")
        self._after_result = True

    def quadrat(self):
        try:
            val = float(_to_eval(self._get()))
            self._set(_fmt(val * val))
        except Exception:
            self._set("ERROR")
        self._after_result = True

    def sqrt_func(self):
        try:
            val = float(_to_eval(self._get()))
            if val < 0:
                raise ValueError
            self._set(_fmt(round(math.sqrt(val), 10)))
        except Exception:
            self._set("ERROR")
        self._after_result = True

    def one_per_x(self):
        try:
            val = float(_to_eval(self._get()))
            if val == 0.0:
                raise ZeroDivisionError
            self._set(_fmt(1 / val))
        except Exception:
            self._set("ERROR")
        self._after_result = True

    # ── Keyboard support ──────────────────────────────────────────────────────

    def keyPressEvent(self, event):
        key  = event.key()
        mods = event.modifiers()

        if mods & Qt.ControlModifier:
            if key == Qt.Key_C:
                self.clipboard.setText(self._get())
            elif key == Qt.Key_V:
                self._paste()
            return

        if key in (Qt.Key_Return, Qt.Key_Enter):
            self.equal()
        elif key == Qt.Key_Backspace:
            self.delete()
        elif key == Qt.Key_Delete:
            self.press_it("C")
        else:
            char = event.text()
            if char in "0123456789":
                self.press_it(char)
            elif char == "+":
                self.press_it("+")
            elif char in ("-", "−"):
                self.press_it("-")
            elif char in ("*", "×"):
                self.press_it("*")
            elif char in ("/", "÷"):
                self.press_it("/")
            elif char == ".":
                self.dot()
            elif char == "%":
                self.press_it("%")

    def _paste(self):
        text = self.clipboard.text().strip()
        if not text:
            return
        current = self._get()
        self._set(text if current == "0" else current + text)
        self._after_result = False


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()