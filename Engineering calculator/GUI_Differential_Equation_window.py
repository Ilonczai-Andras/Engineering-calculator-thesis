from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit
from sympy import false, pretty, symbols, Function, Eq, diff, dsolve, sympify, pprint, true
from sympy.parsing.sympy_parser import parse_expr
from Helper_class_Plotting import Canvas

class Ui_Differential_Equation(object):

    direction_field_showed = true

    def is_first_order_ode(self, func):
        lhs, rhs = func.split("=")

        return "y'(x)" == lhs and "y'(x)" not in rhs and "y''(x)" not in rhs and  "y'''(x)" not in rhs

    def extract_number_from_string(self,s):
        """
        This function extracts and returns a number from a string.
        The string is assumed to contain only one number.

        :param s: The input string containing one number
        :return: The extracted number as an integer
        """
        import re

        # Use regular expression to find the number in the string
        match = re.search(r'\d+', s)
        
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
                initial_value_problem[0] = self.extract_number_from_string(initial_value_problem[0])
                initial_value_problem[1] = int(initial_value_problem[1])

                solution = self.solve_diff_eq_from_string(replaced, initial_value=initial_value_problem)
            else:
                solution = self.solve_diff_eq_from_string(replaced)

            self.canvas.clear((-100, 100), (-10, 10))

            print(f"rhs: {str(solution.rhs)}")
            print(f"replaced: {replaced}")
            if self.is_first_order_ode(string):
                self.canvas.plot_function(str(solution.rhs), (-10,10), C=[1,1,1],clear=false, df=true, df_func=replaced)
            else:
                self.canvas.plot_function(str(solution.rhs), (-10,10), C=[1,1,1],clear=false, df=false)

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
            solution = dsolve(rearranged_equation, y, ics={y.subs(x, initial_value[0]): initial_value[1]})
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

    def back_to_mainwindow(self, Egyenlet, MainWindow):
        Egyenlet.close()
        MainWindow.show()

    def setupUi(self, Diff_Egyenlet, MainWindow):
        self.applyStylesheet(Diff_Egyenlet)
        Diff_Egyenlet.setObjectName("Diff_Egyenlet")
        Diff_Egyenlet.resize(800, 760)
        Diff_Egyenlet.setMinimumSize(QtCore.QSize(800, 760))
        Diff_Egyenlet.setMaximumSize(QtCore.QSize(800, 760))
        self.centralwidget = QtWidgets.QWidget(Diff_Egyenlet)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 780, 141))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 280, 781, 54))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_4.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.pushButton = QtWidgets.QPushButton(
            self.centralwidget,
            clicked=lambda: self.show_diff_equation_result(
                self.text_edit.toPlainText().lower()
            ),
        )
        self.pushButton.setGeometry(QtCore.QRect(610, 70, 170, 50))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(
            self.centralwidget,
            clicked=lambda: self.back_to_mainwindow(Diff_Egyenlet, MainWindow),
        )
        self.pushButton_2.setGeometry(QtCore.QRect(714, 690, 75, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.canvas = Canvas(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(9, 340, 781, 341))

        self.text_edit = QTextEdit(self.centralwidget)
        self.text_edit.setGeometry(QtCore.QRect(250, 10, 330, 100))
        self.text_edit.setObjectName("text_edit")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(610, 10, 170, 50))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Kezdeti érték probléma")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        Diff_Egyenlet.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Diff_Egyenlet)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Diff_Egyenlet.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Diff_Egyenlet)
        self.statusbar.setObjectName("statusbar")
        Diff_Egyenlet.setStatusBar(self.statusbar)

        self.retranslateUi(Diff_Egyenlet)
        QtCore.QMetaObject.connectSlotsByName(Diff_Egyenlet)

    def retranslateUi(self, Diff_Egyenlet):
        _translate = QtCore.QCoreApplication.translate
        Diff_Egyenlet.setWindowTitle(_translate("Diff_Egyenlet", "Differenciál egyenletek"))
        self.label_2.setText(_translate("Diff_Egyenlet", "Eredmény"))
        self.pushButton.setText(_translate("Diff_Egyenlet", "Enter"))
        self.pushButton_2.setText(_translate("Egyenlet", "Vissza"))
        self.label_3.setText(_translate("Diff_Egyenlet", "Differenciál Egyenlet"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Differential_Equation = QtWidgets.QMainWindow()
    ui = Ui_Differential_Equation()
    ui.setupUi(Differential_Equation)
    Differential_Equation.show()
    sys.exit(app.exec_())