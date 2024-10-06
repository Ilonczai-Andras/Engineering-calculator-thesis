from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit
from sympy import (
    false,
    pretty,
    symbols,
    Function,
    Eq,
    diff,
    dsolve,
    sympify,
    pprint,
    true,
)
from sympy.parsing.sympy_parser import parse_expr
from Helpers.Helper_class_Plotting import Canvas
import UI_files.DifferentialEquation_GUI as DifferentialEquation_GUI


class Window(QMainWindow, DifferentialEquation_GUI.Ui_Egyenlet):
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

        self.pushButton.clicked.connect(
            lambda: self.show_diff_equation_result(self.textEdit.toPlainText().lower())
        )

    def is_first_order_ode(self, func):
        lhs, rhs = func.split("=")

        return (
            "y'(x)" == lhs
            and "y'(x)" not in rhs
            and "y''(x)" not in rhs
            and "y'''(x)" not in rhs
        )

    def extract_number_from_string(self, s):
        """
        This function extracts and returns a number from a string.
        The string is assumed to contain only one number.

        :param s: The input string containing one number
        :return: The extracted number as an integer
        """
        import re

        # Use regular expression to find the number in the string
        match = re.search(r"\d+", s)

        # If a match is found, return it as an integer
        if match:
            return int(match.group())
        else:
            raise ValueError("No number found in the string")

    def show_diff_equation_result(self, string):
        replaced = self.replace_nth_derivative(string)
        self.canvas.show()

        initial_value_problem = ""

        try:
            if self.lineEdit.text() != "":
                initial_value_problem = self.lineEdit.text().split("=")
                initial_value_problem[0] = self.extract_number_from_string(
                    initial_value_problem[0]
                )
                initial_value_problem[1] = int(initial_value_problem[1])

                solution = self.solve_diff_eq_from_string(
                    replaced, initial_value=initial_value_problem
                )
            else:
                solution = self.solve_diff_eq_from_string(replaced)

            self.canvas.clear((-100, 100), (-10, 10))

            print(f"rhs: {str(solution.rhs)}")
            print(f"replaced: {replaced}")
            if self.is_first_order_ode(string):
                self.canvas.plot_function(
                    str(solution.rhs),
                    (-10, 10),
                    C=[1, 1, 1],
                    clear=false,
                    df=true,
                    df_func=replaced,
                )
            else:
                self.canvas.plot_function(
                    str(solution.rhs), (-10, 10), C=[1, 1, 1], clear=false, df=false
                )

            latex_solution = pretty(solution)
            self.label_2.setText(f"{latex_solution}")
            self.label_4.setText(f"{solution.rhs}")
            self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        except:
            self.canvas.hide()
            self.label_2.setText("ERROR: helytelen differenciál egyenlet")
            self.label_4.setText("")

    def replace_nth_derivative(self, eq_string):
        # Handle third-order derivatives first
        if "y'''(x)" in eq_string:
            eq_string = eq_string.replace("y'''(x)", "y(x).diff(x,x,x)")
        # Handle second-order derivatives next
        if "y''(x)" in eq_string:
            eq_string = eq_string.replace("y''(x)", "y(x).diff(x,x)")
        # Handle first-order derivatives last
        if "y'(x)" in eq_string:
            eq_string = eq_string.replace("y'(x)", "y(x).diff(x)")
        return eq_string

    def solve_diff_eq_from_string(self, eq_string, initial_value=None):

        x = symbols("x")
        y = Function("y")(x)

        eq1 = sympify(eq_string.split("=")[0])
        eq2 = sympify(eq_string.split("=")[1])
        rearranged_equation = eq1 - eq2

        # Solving the differential equation with or without the initial condition
        if initial_value is not None:
            solution = dsolve(
                rearranged_equation,
                y,
                ics={y.subs(x, initial_value[0]): initial_value[1]},
            )
        else:
            solution = dsolve(rearranged_equation)
        return solution

    def applyStylesheet(self, Diff_Egyenlet):

        stylesheet = """
        QMainWindow {
            background-color: #2E2E2E;
        }
        QWidget#centralwidget {
            background-color: #2E2E2E;
        }
        QTextEdit#text_edit{
            color: #FFFFFF;
            background-color: #1C1C1C;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14pt;
        }
        
        QLineEdit#lineEdit {
            background-color: #1C1C1C;
            color: #FFFFFF;
            font-size: 10pt;
            font-family: 'Courier New', Courier, monospace;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
        }
        QLabel#label_2, QLabel#label_4{
            color: #FFFFFF;
            font-size: 14pt;
            font-family: 'Courier New', Courier, monospace;
        }
        QLabel#label_3{
            color: #FFFFFF;
            font-size: 10pt;
            font-family: 'Courier New', Courier, monospace;
            qproperty-alignment: 'AlignLeft;
        }
        QPushButton {
            background-color: #1C1C1C;
            font-family: 'Courier New', Courier, monospace;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 10px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #5E5E5E;
        }
        QPushButton:pressed {
            background-color: #6E6E6E;
        }
        """
        Diff_Egyenlet.setStyleSheet(stylesheet)


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


############################################
if __name__ == "__main__":
    main()
