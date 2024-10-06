from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QToolBar
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QFont
import sys
import UI_files.Main_GUI as Main_GUI
import re
import math
from PyQt5.QtCore import Qt


class Window(
    QMainWindow, Main_GUI.Ui_MainWindow
):  # Assuming Ui_MainWindow is in Main_GUI.py
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.outputLabel.setFocus()
        self.clipboard = QApplication.clipboard()

        # A variable to store the current text
        self.text = ""
        self.enter_pressed = False
        self.error_displayed = False

        # Apply the stylesheet
        self.applyStylesheet(self)  # Call applyStylesheet after setting up the UI

        # Connect buttons to their respective functions
        self.plusMinusButton.clicked.connect(lambda: self.plus_minus())
        self.clearButton.clicked.connect(lambda: self.press_it("C"))
        self.equalButton.clicked.connect(lambda: self.equal())
        self.percentageButton.clicked.connect(lambda: self.press_it("%"))
        self.quadratButton.clicked.connect(lambda: self.quadrat())
        self.sqrtButton.clicked.connect(lambda: self.sqrt_func())
        self.onePerXButton.clicked.connect(lambda: self.one_per_x())
        self.plusButton.clicked.connect(lambda: self.press_it("+"))
        self.minusButton.clicked.connect(lambda: self.press_it("-"))
        self.multiplyButton.clicked.connect(lambda: self.press_it("*"))
        self.divideButton.clicked.connect(lambda: self.press_it("/"))
        self.decimalPointButton.clicked.connect(lambda: self.dot())
        self.deleteButton.clicked.connect(lambda: self.delete())

        # Numeric Buttons
        self.zeroButton.clicked.connect(lambda: self.press_it("0"))
        self.Button_1.clicked.connect(lambda: self.press_it("1"))
        self.Button_2.clicked.connect(lambda: self.press_it("2"))
        self.Button_3.clicked.connect(lambda: self.press_it("3"))
        self.Button_4.clicked.connect(lambda: self.press_it("4"))
        self.Button_5.clicked.connect(lambda: self.press_it("5"))
        self.Button_6.clicked.connect(lambda: self.press_it("6"))
        self.Button_7.clicked.connect(lambda: self.press_it("7"))
        self.Button_8.clicked.connect(lambda: self.press_it("8"))
        self.Button_9.clicked.connect(lambda: self.press_it("9"))

    def press_it(self, pressed):
        if pressed == "C":
            self.outputLabel.setText("0")
        elif self.outputLabel.text() == "ERROR":
            self.outputLabel.setText(pressed)
        else:
            # Check to see if it starts with 0 and delete the zero
            if self.outputLabel.text() == "0":
                self.outputLabel.setText("")
            # concatenate the pressed button with what was there already
            self.outputLabel.setText(f"{self.outputLabel.text()}{pressed}")

    def dot(self):
        screen = self.outputLabel.text()

        if screen[-1] == ".":
            pass
        else:
            self.outputLabel.setText(f"{screen}.")

    def delete(self):
        if len(self.outputLabel.text()) > 1:
            self.outputLabel.setText(self.outputLabel.text()[:-1])
        elif len(self.outputLabel.text()) == 1:
            self.outputLabel.setText("0")

    def plus_minus(self):
        original = self.outputLabel.text()
        # print(self.contains_only_one_number(original))

        if self.contains_only_one_number(original) and original[0] != "-":
            res = "-" + original[0:]
            self.outputLabel.setText(res)

        if self.contains_only_one_number(original) and original[0] == "-":
            res = original[1:]
            self.outputLabel.setText(res)

        if self.contains_only_one_float(original) and original[0] != "-":
            res = "-" + original[0:]
            self.outputLabel.setText(res)

        if self.contains_only_one_float(original) and original[0] == "-":
            res = original[1:]
            self.outputLabel.setText(res)

    def equal(self):
        screen = self.outputLabel.text()
        try:
            answer = eval(screen)
            self.outputLabel.setText(str(answer))
        except Exception as e:
            print(e)
            self.outputLabel.setText("ERROR")

    def quadrat(self):
        try:
            original = self.outputLabel.text()
            self.outputLabel.setText(str(float(original) * float(original)))
        except:
            self.outputLabel.setText("ERROR")

    def sqrt_func(self):
        try:
            original = self.outputLabel.text()
            self.outputLabel.setText(str(round(math.sqrt(float(original)), 2)))
        except:
            self.outputLabel.setText("ERROR")

    def one_per_x(self):
        try:
            original = float(self.outputLabel.text())
            if original != 0.0:
                self.outputLabel.setText(str((1 / original)))
        except:
            self.outputLabel.setText("ERROR")

    def last_number(self, string):
        i = len(string) - 1
        while i >= 0 and string[i].isdigit():
            i -= 1
        return string[i + 1 :]

    def contains_only_one_number(self, input_str):
        pattern = r"^\D*\d+\D*$"
        return bool(re.match(pattern, input_str))

    def contains_only_one_float(self, input_str):
        try:
            float_value = float(input_str)
            return True
        except ValueError:
            return False

    def applyStylesheet(self, MainWindow):
        stylesheet = """
            QMainWindow {
                background-color: #2E2E2E;
            }
            QPushButton:hover {
                background-color: #5E5E5E;
            }
            QPushButton:pressed {
                background-color: #6E6E6E;
            }
            QComboBox {
                background-color: #4E4E4E;
                font-family: 'Courier New', Courier, monospace; /* Monospaced font */
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #4E4E4E;
                selection-background-color: #5E5E5E;
                color: #FFFFFF;
                font-family: 'Courier New', Courier, monospace; /* Monospaced font */
            }
            QToolBar {
                background-color: #3E3E3E;
                border: none;
                font-family: 'Courier New', Courier, monospace; /* Monospaced font */
            }
            """
        MainWindow.setStyleSheet(stylesheet)

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = QApplication.keyboardModifiers()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.equal()
            self.enter_pressed = True  # Set flag to true after pressing Enter
            self.error_displayed = (
                self.outputLabel.text() == "ERROR"
            )  # Check if ERROR was displayed

        # Handle 'Ctrl+C' 'Ctrl+V'shortcut to save output to clipboard

        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_C:
                print("Ctrl + C")
                self.save_to_clipboard()

        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_V:
                print("Ctrl + V")
                self.paste_into_clipboard()

        else:
            # If enter was pressed before this key or if ERROR is displayed, clear label and start new input
            if self.enter_pressed or self.error_displayed:
                self.text = ""  # Clear the previous text
                self.outputLabel.clear()
                self.enter_pressed = False  # Reset the flag
                self.error_displayed = False  # Reset the error flag

            # Convert the key to a character and append it
            if key == Qt.Key_Backspace:
                # Handle backspace
                self.text = self.text[:-1]
            else:
                self.text += event.text()

            # Update the label with the current text
            self.outputLabel.setText(self.text)

    # Add this method to the Window class
    def save_to_clipboard(self):
        print(self.outputLabel.text())
        self.clipboard.setText(self.outputLabel.text())

    def paste_into_clipboard(self):
        clipboard_text = self.clipboard.text()
        if clipboard_text:
            if self.outputLabel.text() == "0":
                self.outputLabel.setText(clipboard_text)
            else:
                self.outputLabel.setText(self.outputLabel.text() + clipboard_text)


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


############################################
if __name__ == "__main__":
    main()
