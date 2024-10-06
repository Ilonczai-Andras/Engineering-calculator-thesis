from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QToolBar
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import sys
from Helpers.Helper_class_Plotting import Canvas
import UI_files.Equality_GUI as Equality_GUI
from sympy import (
    Or,
    And,
    sympify,
    fourier_transform,
    symbols,
    solve,
    Eq,
    SympifyError,
    oo,
    pretty,
    FourierTransform,
    fourier_series,
)
from numpy import *
import re


class Window(QMainWindow, Equality_GUI.Ui_Egyenlet):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Create and add the canvas
        self.canvas = Canvas(self.centralwidget)

        layout = self.canvaswidget.layout()
        if layout is None:
            from PyQt5.QtWidgets import QVBoxLayout

            layout = QVBoxLayout(self.canvaswidget)
            self.canvaswidget.setLayout(layout)

        layout.addWidget(self.canvas)

        self.pushButton.clicked.connect(lambda: self.combobox_selector())

        common_area = []

    def replace_trigonometric_funcs(self, func_str):
        replacements = {
            # log
            r"\blog\b": "",
            r"\bln\b": "",
            # Inverse
            r"\barctan\b": "",
            r"\barcsin\b": "",
            r"\barccos\b": "",
            # Inverse hyperbolic
            r"\barcsinh\b": "",
            r"\barccosh\b": "",
            r"\barctanh\b": "",
            # trig
            r"\bsin\b": "",
            r"\bcos\b": "",
            r"\btan\b": "",
            # hyperbolic
            r"\bsinh\b": "",
            r"\bcosh\b": "",
            r"\btanh\b": "",
            # exp
            r"\bexp\b": "",
            # abs
            r"\babs\b": "",
            # sign(x)
            r"\bsign\b": "",
            # sqrt
            r"\bsqrt\b": "",
            # secant and cosecant
            r"\bsec\b": "",
            r"\bcsc\b": "",
        }

        for pattern, replacement in replacements.items():
            func_str = re.sub(pattern, replacement, func_str)

        return func_str

    def extract_variable(self, expression):
        variables = []

        for i in expression:
            if i not in variables and i.isalpha():
                variables.append(i.lower())

        return variables

    def number_of_lines(self, expression):
        res = []
        number = 0

        for line in expression.splitlines():
            if line.strip():
                number += 1
                res.append(line)

        res.append(number)
        return res

    def from_OrAnd_to_set(self, expr):
        numbers = set()
        self._extract_numbers(expr, numbers)
        return numbers

    def _extract_numbers(self, expr, numbers):
        # Ensure we are dealing with logical or relational expressions
        if isinstance(expr, (Or, And)):
            for arg in expr.args:
                self._extract_numbers(arg, numbers)
        elif expr.is_Relational:
            lhs, rhs = expr.lhs, expr.rhs
            # Check if lhs is a number and not -oo or oo
            if lhs.is_number and lhs != -oo and lhs != oo:
                numbers.add(lhs)
            # Check if rhs is a number and not -oo or oo
            if rhs.is_number and rhs != -oo and rhs != oo:
                numbers.add(rhs)

    def system_of_equations(self, funcs):
        print("#LOG system of equations")
        number_of_rows = funcs.pop()

        symbols_set = set()
        equations = []

        for eq_str in funcs:
            # Split the equation into left-hand side and right-hand side
            lhs, rhs = eq_str.split("=")
            lhs_sympy = sympify(lhs.strip())
            rhs_sympy = sympify(rhs.strip())

            # Replace trigonometric functions and extract variables
            lhs_vars = self.extract_variable(self.replace_trigonometric_funcs(lhs))
            rhs_vars = self.extract_variable(self.replace_trigonometric_funcs(rhs))
            symbols_in_eq = lhs_vars + rhs_vars

            # Update the set of symbols with variables found in this equation
            symbols_set.update(symbols_in_eq)

            # Create a sympy Eq object and add it to the equations list
            equations.append(Eq(lhs_sympy, rhs_sympy))

        # Convert the set of symbols into a list and then into sympy symbols
        symbols_list = list(symbols_set)
        symbol_objects = symbols(" ".join(symbols_list))

        # Solve the system of equations
        solution = solve(equations, symbol_objects)

        # Check if the solution is a dictionary and format it
        if isinstance(solution, dict):
            print("Solution is a dictionary")
            formatted_solution = "\n".join(
                [f"{str(key)} = {str(value)}" for key, value in solution.items()]
            )
        if isinstance(solution, list) and all(
            isinstance(item, tuple) for item in solution
        ):
            print("Solution is a list")
            formatted_solution = "\n".join(
                [f"({', '.join(map(str, item))})" for item in solution]
            )
        else:
            formatted_solution = str(solution)

        return formatted_solution

    def one_func(self, one_func, replaced_func):
        inequality = ["<=", ">=", "<", ">"]
        inequality_type = None

        for ineq in inequality:
            if ineq in one_func:
                inequality_type = ineq
                break

        if inequality_type:
            symbs = self.extract_variable(replaced_func)
            result = solve(one_func, tuple(symbs))

            inequality_results = self.from_OrAnd_to_set(result)
            x_intervals = sorted(list(inequality_results))

            for i in inequality_results:
                self.common_area.append(i)

            self.label_2.setText(pretty(result))

            self.canvas.plot_area_between_functions(x_intervals)
        else:
            splitted_func = one_func.replace(" ", "").split("=")
            symbs = self.extract_variable(replaced_func)

            equation = Eq(sympify(splitted_func[0]), sympify(splitted_func[1]))

            rearranged_equation = equation.lhs - equation.rhs
            result = solve(rearranged_equation, tuple(symbs))

            numerical_results = [sol.evalf() for sol in result]
            rounded_results = [
                complex(
                    round(sol.as_real_imag()[0], 2), round(sol.as_real_imag()[1], 2)
                )
                for sol in numerical_results
            ]

            formatted_results = [
                (
                    f"{sol.real:.2f} + {sol.imag:.2f}i"
                    if sol.imag >= 0
                    else f"{sol.real:.2f} - {abs(sol.imag):.2f}i"
                )
                for sol in rounded_results
            ]
            for i in numerical_results:
                self.common_area.append(i)
            result_text = "\n".join(formatted_results)

            self.label_2.setText(result_text.replace("**", "^"))

    def combobox_selector(self):
        input_text = self.comboBox.currentText()
        function_text = self.text_edit.toPlainText().lower()
        number_of_rows = self.number_of_lines(function_text)
        inequality = ["<=", ">=", "<", ">", "="]

        if input_text == "Equation":
            print("#LOG Equation")
            lhs = rhs = None  # Initialize lhs and rhs to None
            try:
                self.canvas.show()
                if len(number_of_rows) == 2:
                    self.common_area = []

                    for ineq in inequality:
                        if ineq in function_text:
                            lhs, rhs = function_text.split(ineq)
                            break

                    self.one_func(
                        function_text,
                        self.replace_trigonometric_funcs(function_text).replace(
                            "sqrt", ""
                        ),
                    )
                else:
                    self.label_2.setText("Provide a single line")
                    self.text_edit.setText("")
                    return  # Exit early if there isn't a valid equation
            except Exception as e:
                print(e)
                self.label_2.setText(
                    "ERROR: incorrect equation, please provide a new one!"
                )
                return  # Exit early in case of an exception
            finally:
                # Ensure lhs and rhs are not None before plotting
                if lhs and rhs:
                    self.canvas.clear((-10, 10), (-10, 10))
                    self.canvas.plotted_functions = []
                    self.canvas.plot_function(
                        lhs, (-10, 10), (-10, 10), clear=False, Color="red"
                    )
                    self.canvas.store_function(
                        lhs, (-10, 10), (-10, 10), None, False, ""
                    )
                    self.canvas.plot_function(
                        rhs, (-10, 10), (-10, 10), clear=False, Color="blue"
                    )
                    self.canvas.store_function(
                        rhs, (-10, 10), (-10, 10), None, False, ""
                    )
                else:
                    self.label_2.setText("No valid equation to plot.")
        if input_text == "System of Equations":
            print("#LOG System of Equations")
            self.canvas.hide()
            try:
                if len(number_of_rows) - 1 >= 2:
                    formatted_solution = self.system_of_equations(number_of_rows)
                    self.label_2.setText(formatted_solution)
                else:
                    self.label_2.setText("Provide more equations!")
                    self.text_edit.setText("")
            except Exception as e:
                self.label_2.setText(
                    "ERROR: incorrect system of equations, please provide a new one!"
                )
        if input_text == "Fourier Transform":
            print("#LOG Fourier Transform")
            if len(number_of_rows) == 2:
                t, x = symbols("t x")
                self.canvas.hide()
                try:
                    input_function = sympify(function_text)
                    ft = fourier_transform(input_function, t, x)
                    result = str(ft)
                    if not isinstance(ft, FourierTransform) and result != "0":
                        self.label_2.setText(result)
                        self.label_2.setText(result)
                        self.canvas.clear((-10, 10), (-10, 10))
                        self.canvas.plotted_functions = []
                        self.canvas.plot_function(
                            result, (-10, 10), (-10, 10), clear=False
                        )
                        self.canvas.store_function(
                            result, (-10, 10), self.canvas.interval_y, None, False, ""
                        )
                    else:
                        self.label_2.setText("Fourier transform cannot be computed")
                except SympifyError as e:
                    self.label_2.setText("Invalid function for Fourier transform")
                    print(f"Sympify error: {e}")
            else:
                self.canvas.hide()
                self.label_2.setText("Provide a single line")
                self.text_edit.setText("")
        if input_text == "Fourier Series":
            print("#LOG Fourier Series")
            self.canvas.show()
            if len(number_of_rows) == 2:
                try:
                    input_function = sympify(function_text)
                    series = fourier_series(input_function)
                    result = str(series.truncate())
                    self.label_2.setText(result)
                    self.canvas.clear((-10, 10), (-10, 10))

                    self.canvas.plotted_functions = []
                    self.canvas.plot_function(result, (-10, 10), (-10, 10), clear=False)
                except Exception as e:
                    print(e)
                    self.label_2.setText("Invalid function for Fourier series")
                    self.text_edit.setText("")
            else:
                self.label_2.setText("Provide a single line")
                self.text_edit.setText("")


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


############################################
if __name__ == "__main__":
    main()
