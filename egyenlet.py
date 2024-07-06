# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'egyenlet.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Canvas_for_plot import Canvas
from PyQt5.QtWidgets import QTextEdit
from sympy import *
from numpy import *
import sys
import re


class Ui_Egyenlet(object):

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
            # gyok
            r"\bsqrt\b": "",
            # szekánsok
            r"\bsec\b": "",
            r"\bcsc\b": "",
        }

        for pattern, replacement in replacements.items():
            func_str = re.sub(pattern, replacement, func_str)

        return func_str

    def extract_variable(self, expression):
        valtozok = []

        for i in expression:
            if i not in valtozok and i.isalpha():
                valtozok.append(i.lower())

        return valtozok

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
        number_of_rows = (
            funcs.pop()
        )  # Remove the last element which is the number of equations
        symbols_set = set()
        equations = []

        for eq_str in funcs:
            lhs, rhs = eq_str.split("=")
            lhs_sympy = sympify(lhs.strip())
            rhs_sympy = sympify(rhs.strip())
            symbols_in_eq = self.extract_variable(
                self.replace_trigonometric_funcs(lhs)
            ) + self.extract_variable(self.replace_trigonometric_funcs(rhs))
            symbols_set.update(symbols_in_eq)
            equations.append(Eq(lhs_sympy, rhs_sympy))

        symbols_list = list(symbols_set)
        symbol_objects = symbols(" ".join(symbols_list))

        # Solve the system of equations
        solution = solve(equations, symbol_objects)

        # Format the solution to have each result on a new line
        formatted_solution = "\n".join([str(sol) for sol in solution])
        print("for_sol: ", formatted_solution)

        return formatted_solution

    def one_func(self, one_func, replaced_func):
        try:
            inequality = ["<=", ">=", "<", ">"]
            inequality_type = None

            for ineq in inequality:
                if ineq in one_func:
                    inequality_type = ineq
                    break

            if inequality_type:
                symbs = self.extract_variable(replaced_func)
                result = solve(one_func, tuple(symbs))
                print(f"ineq: {result}")
                print(f"type: {type(result)}")

                inequality_results = self.from_OrAnd_to_set(result)
                x_intervals = sorted(list(inequality_results))

                for i in inequality_results:
                    self.common_area.append(i)
                print(f"vagyés: {self.from_OrAnd_to_set(result)}")

                self.label_2.setText(pretty(result))

                # Call plot_area_between_functions with intervals and inequality type
                self.canvas.plot_area_between_functions(x_intervals, inequality_type)
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
                print(f"Numerical res: {numerical_results}")
                for i in numerical_results:
                    self.common_area.append(i)
                result_text = "\n".join(formatted_results)

                self.label_2.setText(result_text.replace("**", "^"))

        except SympifyError as e:
            print("Sympify error:", e)
            self.label_2.setText("Invalid equation!")
        except Exception as x:
            print(x)
            self.label_2.setText("An error occurred!")



    def combobox_selector(self):
        input_text = self.comboBox.currentText()
        function_text = self.text_edit.toPlainText().lower()
        number_of_rows = self.number_of_lines(function_text)
        inequality = ["<=", ">=", "<", ">", "="]

        if input_text == "Egyenlet":
            if len(number_of_rows) == 2:
                self.common_area = []
                self.one_func(function_text, self.replace_trigonometric_funcs(function_text).replace("sqrt", ""))
                for ineq in inequality:
                    if ineq in function_text:
                        self.canvas.clear((-100, 100), (-10, 10))
                        self.canvas.plotted_functions = []
                        lhs, rhs = function_text.split(ineq)
                        print(lhs, rhs)
                        self.canvas.plot_function(lhs, (-100, 100), clear=False)
                        self.canvas.store_function(lhs, (-100, 100), self.canvas.interval_y, None, False, "")
                        self.canvas.plot_function(rhs, (-100, 100), clear=False)
                        self.canvas.store_function(rhs, (-100, 100), self.canvas.interval_y, None, False, "")
                        
                        # Convert sympy types to float
                        self.common_area = [float(val) for val in self.common_area]
                        
                        print(f"Calling plot_area_between_functions with {self.common_area}")  # Debug statement
                        self.canvas.plot_area_between_functions(self.common_area, ineq)
                        break
            else:
                self.label_2.setText("Egy sort adj meg")
                self.text_edit.setText("")
        if input_text == "Egyenletrendszerek":
            if len(number_of_rows) >= 2:
                formatted_solution = self.system_of_equations(number_of_rows)
                self.label_2.setText(formatted_solution)
            else:
                self.label_2.setText("Egy sort adj meg")
                self.text_edit.setText("")


    def back_to_mainwindow(self, Egyenlet, MainWindow):
        Egyenlet.close()
        MainWindow.show()

    def applyStylesheet(self, Egyenlet):
        stylesheet = """
        QMainWindow {
            background-color: #2E2E2E;
        }
        QWidget#centralwidget {
            background-color: #2E2E2E;
        }
        QLabel {
            color: #FFFFFF;
        }
        QComboBox, QTextEdit {
            background-color: #4E4E4E;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
        }
        QComboBox QAbstractItemView {
            background-color: #4E4E4E;
            selection-background-color: #5E5E5E;
            color: #FFFFFF;
        }
        QLabel#label {
            font-family: Times New Roman;
            font-size: 12pt;
            text-align: center;
        }
        QLabel#label_2 {
            font-size: 14pt;
            qproperty-alignment: 'AlignRight | AlignTrailing | AlignVCenter';
        }
        QPushButton {
            background-color: #4E4E4E;
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
        Egyenlet.setStyleSheet(stylesheet)

    def setupUi(self, Egyenlet, MainWindow):
        self.applyStylesheet(Egyenlet)
        Egyenlet.setObjectName("Egyenlet")
        Egyenlet.resize(800, 760)
        Egyenlet.setMinimumSize(QtCore.QSize(800, 760))
        Egyenlet.setMaximumSize(QtCore.QSize(800, 760))
        self.centralwidget = QtWidgets.QWidget(Egyenlet)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 70, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 780, 200))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_2.setObjectName("label_2")
        self.label_2.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.canvas = Canvas(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(9, 340, 781, 341))

        self.pushButton = QtWidgets.QPushButton(
            self.centralwidget, clicked=lambda: self.combobox_selector()
        )
        self.pushButton.setGeometry(QtCore.QRect(710, 70, 75, 51))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(
            self.centralwidget,
            clicked=lambda: self.back_to_mainwindow(Egyenlet, MainWindow),
        )
        self.pushButton_2.setGeometry(QtCore.QRect(714, 690, 75, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.text_edit = QTextEdit(self.centralwidget)
        self.text_edit.setGeometry(310, 20, 391, 101)
        self.text_edit.setObjectName("text_edit")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(250, 10, 391, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        Egyenlet.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Egyenlet)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Egyenlet.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Egyenlet)
        self.statusbar.setObjectName("statusbar")
        Egyenlet.setStatusBar(self.statusbar)

        self.retranslateUi(Egyenlet)
        QtCore.QMetaObject.connectSlotsByName(Egyenlet)

    def retranslateUi(self, Egyenlet):
        _translate = QtCore.QCoreApplication.translate
        Egyenlet.setWindowTitle(_translate("Egyenlet", "Egyenlet"))
        self.comboBox.setItemText(0, _translate("Egyenlet", "Egyenlet"))
        self.comboBox.setItemText(1, _translate("Egyenlet", "Egyenletrendszerek"))
        self.label.setText(
            _translate("Egyenlet", "Válaszd ki a végrahajtandó műveletet")
        )
        self.label_2.setText(_translate("Egyenlet", "Eredmény"))
        self.pushButton.setText(_translate("Egyenlet", "Enter"))
        self.pushButton_2.setText(_translate("Egyenlet", "Vissza"))
        self.label_3.setText(_translate("Egyenlet", "Egyenlet"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Egyenlet = QtWidgets.QMainWindow()
    ui = Ui_Egyenlet()
    ui.setupUi(Egyenlet)
    Egyenlet.show()
    sys.exit(app.exec_())
