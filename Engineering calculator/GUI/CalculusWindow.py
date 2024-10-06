from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QToolBar
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import sys
from Helpers.Helper_class_Plotting import Canvas
import UI_files.Calculus_GUI as Calculus_GUI
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont
from sympy import (
    oo,
    Sum,
    Symbol,
    Interval,
    sympify,
    limit,
    integrate,
    is_increasing,
    is_strictly_increasing,
    is_decreasing,
    is_monotonic,
    is_strictly_decreasing,
    diff,
)
from sympy import (
    sin,
    cos,
    tan,
    log,
    atan,
    asin,
    acos,
    asinh,
    acosh,
    atanh,
    sinh,
    cosh,
    tanh,
    exp,
    Abs,
    sign,
    sqrt,
    sec,
    csc,
    pi,
    E
)
import re
from math import pi


class Window(QMainWindow, Calculus_GUI.Ui_Calculus):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.applyStylesheet(self)

        # Create and add the canvas
        self.canvas = Canvas(self.centralwidget)

        layout = self.canvaswidget.layout()
        if layout is None:
            from PyQt5.QtWidgets import QVBoxLayout
            layout = QVBoxLayout(self.canvaswidget)
            self.canvaswidget.setLayout(layout)

        layout.addWidget(self.canvas)

        self.pushButton.clicked.connect(lambda: self.combobox_selector())
        self.lineEdit.textChanged.connect(self.on_text_changed)

    def combobox_selector(self):
        also = 0
        felso = 0

        try:
            if "pi" in self.lineEdit_2.text() or "pi" in self.lineEdit_3.text():
                print("#LOG PI")
                try:
                    if "pi" in self.lineEdit_2.text() and " " in self.lineEdit_2.text():
                        also = int(int(self.lineEdit_2.text().split(" ")[0]) * pi)
                        print("also if:", also)
                    elif "pi" in self.lineEdit_2.text() and not " " in self.lineEdit_2.text():
                        also = int(int(self.lineEdit_2.text().split("pi")[0]) * pi)
                        print("also else:", also)
                    else:
                        also = int(self.lineEdit_2.text())

                    if "pi" in self.lineEdit_3.text() and " " in self.lineEdit_3.text():
                        felso = int(int(self.lineEdit_3.text().split("pi")[0]) * pi)
                        print("felso if:", felso)
                    elif "pi" in self.lineEdit_3.text() and not " " in self.lineEdit_3.text():
                        felso = int(int(self.lineEdit_3.text().split("pi")[0]) * pi)
                        print("felso else:", felso)
                    else:
                        felso = int(self.lineEdit_3.text())
                except:
                    self.label_2.setText("ERROR: incorrect boundary provided with pi")
                    self.lineEdit_2.setText("-10")
                    self.lineEdit_3.setText("10")
                interval = (also, felso)
            elif (self.is_valid_float(self.lineEdit_2.text().replace("-", "")) and self.is_valid_float(self.lineEdit_3.text().replace("-", ""))):
                print("#LOG Másik ág")
                also = sympify(self.lineEdit_2.text())
                felso = sympify(self.lineEdit_3.text())
                # inf
                if sympify(self.lineEdit_2.text()) == -oo:
                    also = -1000000000

                if sympify(self.lineEdit_3.text()) == oo:
                    felso = 1000000000

                # zero
                if sympify(self.lineEdit_2.text()) == 0:
                    also = 0

                if sympify(self.lineEdit_3.text()) == 0:
                    felso = 0

                # not zero
                if sympify(self.lineEdit_2.text()) != 0:
                    also = float(also)

                if sympify(self.lineEdit_3.text()) != 0:
                    felso = float(felso)
                interval = (also, felso)
            else:
                self.label_2.setText("ERROR: invalid boundaries")
                self.lineEdit_2.setText("-10")
                self.lineEdit_3.setText("10")
                also = -10
                felso = 10
                self.canvas.clear(interval_x=interval, interval_y=interval)
        except:  
            interval = (-10,10)
        input = self.comboBox.currentText()
        text = self.lineEdit.text()
        x = Symbol("x", real=True)

        print(f"input '{input}' {input == "Strictly increasing"}")
        
        if input == "Increasing":
            print("#LOG Increasing")
            try:
                res = is_increasing(sympify(self.replace_sympy_funcs(text)), Interval(also,felso))
                if res == True:
                    self.label_2.setText(text + " increasing")
                elif res == False:
                    self.label_2.setText(text + " not increasing")
                else:
                    self.label_2.setText("Operation cannot be performed!")
                result = self.canvas.plot_function(func_str=text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect increasing function!")

        if input == "Strictly Increasing":
            print("#LOG Strictly increasing")
            try:
                res = is_strictly_increasing(
                    sympify(self.replace_sympy_funcs(text)), Interval(also, felso)
                )
                if res == True:
                    self.label_2.setText(text + " strictly increasing")
                elif res == False:
                    self.label_2.setText(text + " strictly not increasing")
                else:
                    self.label_2.setText("Operation cannot be performed!")
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect strictly increasing function!")

        if input == "Decreasing":
            print("#LOG Decreasing")
            try:
                res = is_decreasing(
                    sympify(self.replace_sympy_funcs(text)), Interval(also, felso)
                )
                if res == True:
                    self.label_2.setText(text + " decreasing")
                elif res == False:
                    self.label_2.setText(text + " not decreasing")
                else:
                    self.label_2.setText("Operation cannot be performed!")
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect decreasing function!")

        if input == "Strictly Decreasing":
            print("#LOG Strictly decreasing")
            try:
                res = is_strictly_decreasing(
                    sympify(self.replace_sympy_funcs(text)), Interval(also, felso)
                )
                print(res)
                if res == True:
                    self.label_2.setText(text + " strictly decreasing")
                elif res == False:
                    self.label_2.setText(text + " strictly not decreasing")
                else:
                    self.label_2.setText("Operation cannot be performed!")
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect strictly decreasing function!")

        if input == "Monotonic":
            print("#LOG Monotonic")
            try:
                res = is_monotonic(
                    sympify(self.replace_sympy_funcs(text)), Interval(also, felso)
                )
                if res == True:
                    self.label_2.setText(text + " Monotonic")
                elif res == False:
                    self.label_2.setText(text + " not monotonic")
                else:
                    self.label_2.setText("Operation cannot be performed!")
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect monotonic function!")

        if input == "Divergent":
            print("#LOG Divergent")
            try:
                exp = sympify(text)
                x = Symbol("x")
                res = limit(exp, x, oo)
                if res == oo or res == -oo:
                    self.label_2.setText(text + " Divergent")
                else:
                    self.label_2.setText(text + " not divergent")
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect divergent function!")
            
        if input == "Limit":
            print("#LOG Limit")
            try:
                if self.has_no_variables(text):
                    self.label_2.setText(text + " -> " + str(eval(text)))
                else:
                    x = Symbol("x")
                    res = limit(sympify(text), x, oo)
                    if "AccumBounds" not in str(res):
                        print(res)
                        self.label_2.setText(text + " -> " + str(res))
                    else:
                        self.label_2.setText(text + " -> " + str(res).replace("AccumBounds", ""))
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect limit function!")
        #javít
        if input == "Konvergens":
            try:
                res = Sum(self.replace_sympy_funcs(text), (x, -oo, oo)).is_convergent()
                print(res)
                if res:
                    self.label_2.setText(text + " the series converges")
                else:
                    self.label_2.setText(text + " the series does not converge")
                result = self.canvas.plot_function(text, interval_x=interval, interval_y=interval)
                if result == False:
                    self.label_2.setText("ERROR: invalid function!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect convergent function!")

        if input == "Differentiation":
            print("#LOG Differentiation")
            try:
                tmp = eval(self.replace_sympy_funcs(text))
                res = diff((tmp), x)
                self.label_2.setText(str(res).replace("E", "e"))
                res_str = str(res).replace("E", "e")
                result = self.canvas.plot_function(res_str, interval_x=interval, interval_y=interval)
                if result == False:
                    #self.label_2.setText("ERROR: hibás függvény!")
                    self.lineEdit.setText("")
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR: incorrect differentiation!")           

        if input == "Integration":
            print("#LOG Integration")
            try:
                self.canvas.show()
                x = Symbol("x")
                res = integrate(self.replace_sympy_funcs(text), x)
                self.label_2.setText(str(res).replace("**", "^").replace("E", "e") + " + C")
                res_str = str(res).replace("E", "e")
                result = self.canvas.plot_function(res_str, interval_x=interval, interval_y=interval)
                print(result)
                if result == False:
                    self.canvas.hide()
                    self.label_2.setText("ERROR: cannot plot integrated function!")
                    pass
            except Exception as e:
                self.canvas.hide()
                self.label_2.setText("Cannot compute integrated function!")
        self.pushButton.setEnabled(False)

    def has_no_variables(self, func_str):
        # Define a regular expression pattern to match mathematical variables
        var_pattern = r"[a-zA-Z]+"
        # Find all matches of variables in the function string
        variables = re.findall(var_pattern, func_str)
        # If no variables are found, return True
        return len(variables) == 0

    def replace_sympy_funcs(self, func_str):
        replacements = {
            r"\b(ln)\b": "log",
            # trig
            r"\bsin\b": "sin",
            r"\bcos\b": "cos",
            r"\btan\b": "tan",
            # Inverse trig
            r"\barctan\b": "atan",
            r"\barcsin\b": "asin",
            r"\barccos\b": "acos",
            # Inverse hyperbolic
            r"\barcsinh\b": "asinh",
            r"\barccosh\b": "acosh",
            r"\barctanh\b": "atanh",
            # hyperbolic
            r"\bsinh\b": "sinh",
            r"\bcosh\b": "cosh",
            r"\btanh\b": "tanh",
            # exp
            r"\bexp\b": "exp",
            # abs
            r"\babs\b": "Abs",
            # sign(x)
            r"\sign\b": "sign",
            # sqrt
            r"\bsqrt\b": "sqrt",
            # secant and cosecant
            r"\bsec\b": "sec",
            r"\bcsc\b": "csc",
            #pi and e
            r"\bpi\b": "pi",
            r"\be\b": "E"
        }

        for pattern, np_func in replacements.items():
            func_str = re.sub(pattern, np_func, func_str)

        func_str = func_str.replace("^", "**")

        return func_str

    def applyStylesheet(self, Calculus):
        stylesheet = """
        QMainWindow {
            background-color: #2E2E2E;
        }
        QComboBox {
            background-color: #4E4E4E;
            font-family: 'Courier New', Courier, monospace;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
        }
        QComboBox#comboBox {
        font-family: 'Courier New', Courier, monospace;
        width: 330px;
        }
        QComboBox QAbstractItemView {
            font-family: 'Courier New', Courier, monospace;
            background-color: #4E4E4E;
            selection-background-color: #5E5E5E;
            color: #FFFFFF;
        }
        QToolBar {
            background-color: #3E3E3E;
            font-family: 'Courier New', Courier, monospace;
            border: none;
        }
        """
        Calculus.setStyleSheet(stylesheet)

    def is_valid_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def on_text_changed(self, text):
        self.pushButton.setEnabled(bool(text.strip()))

def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


############################################
if __name__ == "__main__":
    main()
