from PyQt5.QtWidgets import QMainWindow, QApplication
import UI_files.Probability_And_Statistics_GUI as Probability_And_Statistics_GUI
import os
import math
import sys
from matplotlib.pylab import pareto
import numpy as np
from Helpers.Helper_class_Plotting import Canvas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit
from scipy import stats
import statistics
from scipy.stats import norm
from sympy import N, pretty, sympify, symbols, gamma, log, digamma, sqrt
from sympy.stats import (
    Normal,
    Geometric,
    Poisson,
    Logarithmic,
    Erlang,
    Pareto,
    P,
    E,
    variance,
    density,
    entropy,
    variance,
)


class Window(QMainWindow, Probability_And_Statistics_GUI.Ui_Ui_Prob_and_Stat):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.comboBox.currentTextChanged.connect(self.handle_combobox_change)
        self.comboBox_2.currentTextChanged.connect(self.handle_combobox2_change)
        self.pushButton.clicked.connect(lambda: self.combobox_selector())

        # Create and add the canvas
        self.canvas = Canvas(self.centralwidget)

        layout = self.canvaswidget.layout()
        if layout is None:
            from PyQt5.QtWidgets import QVBoxLayout

            layout = QVBoxLayout(self.canvaswidget)
            self.canvaswidget.setLayout(layout)

        layout.addWidget(self.canvas)
        self.canvas.hide()

    def string_to_S(self, string):

        return string.replace(" ", "").replace("1/", "S.One/")

    def number_of_lines(self, expression):
        res = []
        number = 0

        for line in expression.splitlines():
            if line.strip():
                number += 1
                res.append(line)

        return res

    def str_to_list(self, list_string):
        return [float(num) for num in list_string.split(",")]

    def t_test(self=None, mu=None, alpha=None, x=None, y=None, paired=None):

        if x is not None and mu is not None and alpha is not None:
            print("#LOG egymintás t")
            result_string = ""

            avg = statistics.mean(x)
            stan_dev = statistics.stdev(x)
            m = mu
            n = len(x)

            Alpha = 1 - alpha
            df = n - 1

            t = (avg - m) / (stan_dev / sqrt(n))
            t = float(t)  # Ensure numerical evaluation

            t_p = stats.t.ppf(q=1 - Alpha / 2, df=df)
            p_value = 2 * (1 - stats.t.sf(abs(float(t)), df))

            if abs(t) >= t_p:

                result_string += (
                    f"\nH0 is rejected t: {t}\n{abs(t)} >= {t_p}\np: {2 - p_value}\n"
                )
                # result_string += f"two tail  t:{abs(stats.t.ppf(q= Alpha/2,df= df) )}" +"\n"
                # result_string += f"one tail  t:{abs(stats.t.ppf(q= Alpha,df= df) )}" +"\n"
            elif abs(t) < t_p:
                result_string += (
                    f"\nH0 is accepted t: {t}\n{abs(t)} < {t_p}\np: {2 - p_value}\n"
                )
                # result_string += f"two tail  t:{abs(stats.t.ppf(q= Alpha/2,df= df) )}" +"\n"
                # result_string += f"one tail  t:{abs(stats.t.ppf(q= Alpha,df= df) )}" +"\n"

            return result_string
        elif (
            x is not None and y is not None and alpha is not None and paired is not None
        ):
            print("#LOG kétmintás párosított t próba")
            result_string = ""

            x = np.array(x)
            y = np.array(y)
            z = y - x
            N = len(z)
            Alpha = 1 - alpha

            # Paired t-test using scipy.stats
            t_stat, p_value = stats.ttest_1samp(z, 0)

            # Determine if we reject or accept the null hypothesis
            if p_value < Alpha:
                result_string += "H0 is rejected\n"  # We reject H0
            else:
                result_string += "H0 is accepted\n"  # We accept H0

            result_string += f"t: {t_stat} p: {p_value}\n"

            return result_string
        elif x is not None and y is not None and alpha is not None:
            print("#LOG kétmintás t")
            result_string = ""

            t_statistic, p_value = stats.ttest_ind(x, y)

            Alpha = 1 - alpha
            if p_value < Alpha:
                result_string += "H0 is rejected\n"
            else:
                result_string += "H0 is accepted\n"

            result_string += f"P: {p_value} T: {t_statistic}\n"
            # result_string += f"two tail p: {stats.t.ppf(q=Alpha/2, df=(len(x) + len(y) - 2))}\n"
            # result_string += f"one tail p: {stats.t.ppf(q=Alpha, df=(len(x) + len(y) - 2))}\n"

            return result_string

    def u_test(self, X=None, mu=None, sigma=None, alpha=None):
        if X is not None and mu is not None and sigma is not None and alpha is not None:
            # Sample statistics
            n = len(X)
            if n == 0:
                raise ValueError("Sample data X cannot be empty.")

            sample_mean = np.mean(X)
            Alpha = 1 - alpha

            # Calculate Z-value
            z_value = (sample_mean - mu) / (sigma / np.sqrt(n))

            # Left-tailed test
            z_critical_left = norm.ppf(Alpha)
            p_value_left = norm.cdf(z_value)
            accept_null_left = "yes" if p_value_left > Alpha else "no"
            left_test_result = f"Left test: critical Z-value:{z_critical_left}, \nP-value: {p_value_left}, HO adoption: {accept_null_left}"

            # Two-tailed test
            z_critical_two = norm.ppf(1 - Alpha / 2)
            p_value_two = 2 * (1 - norm.cdf(abs(z_value)))
            accept_null_two = "yes" if p_value_two > Alpha else "no"
            two_test_result = f"Two-sided test: critical Z-value: ±{z_critical_two}, \nP-value: {p_value_two}, HO adoption: {accept_null_two}"

            # Right-tailed test
            z_critical_right = norm.ppf(1 - Alpha)
            p_value_right = 1 - norm.cdf(z_value)
            accept_null_right = "yes" if p_value_right > Alpha else "no"
            right_test_result = f"Right test: critical Z-value: {z_critical_right}, \nP-value: {p_value_right}, HO adoption: {accept_null_right}"

            return (
                f"Z-value: {z_value}\n\n"
                f"{left_test_result}\n\n"
                f"{two_test_result}\n\n"
                f"{right_test_result}"
            )

    def logarithmic_entropy(self, p, k_max=1000):
        entropy = 0
        for k in range(1, k_max + 1):
            pk = -(p**k) / (k * np.log(1 - p))
            if pk > 0:
                entropy += pk * np.log(pk)
        return -entropy

    def combobox_selector(self):
        distribution = self.comboBox_2.currentText()
        operation_type = self.comboBox.currentText()
        self.canvas.clear(interval_x=(0, 10), interval_y=(0, 5))

        m = 0
        s = 0

        text = self.lineEdit_2.toPlainText()
        lines = self.number_of_lines(text)

        if operation_type in ["T test", "U test"]:
            if operation_type == "T test":
                if distribution == "Single sample t test":
                    if len(lines) == 1:
                        try:
                            x = self.str_to_list(lines[0])
                            mu = int(self.mu.toPlainText())
                            alpha = float(self.sigma.toPlainText())
                        except:
                            self.label_2.setText("ERROR failed t test!")
                        else:
                            res = self.t_test(x=x, mu=mu, alpha=alpha)
                            self.label_2.setText(res)
                    else:
                        self.label_2.setText("Give me a list!")
                elif distribution == "Two-sample paired t test":
                    if len(lines) == 2:
                        try:
                            x = self.str_to_list(lines[0])
                            y = self.str_to_list(lines[1])
                            alpha = float(self.sigma.toPlainText())
                            mu = float(self.sigma.toPlainText())
                        except:
                            self.label_2.setText("ERROR failed t test!")
                        else:
                            res = self.t_test(x=x, y=y, alpha=alpha, paired=True)
                            self.label_2.setText(res)
                    else:
                        self.label_2.setText("Give me two lists!")
                elif distribution == "Two sample t test":
                    if len(lines) == 2:
                        try:
                            x = self.str_to_list(lines[0])
                            y = self.str_to_list(lines[1])
                            alpha = float(self.sigma.toPlainText())
                        except:
                            self.label_2.setText("ERROR failed t test!")
                        else:
                            res = self.t_test(x=x, y=y, alpha=alpha)
                            self.label_2.setText(res)
                    else:
                        self.label_2.setText("Give me two lists!")

            if operation_type == "U test":
                if distribution == "Single sample u test":
                    if len(lines) == 1:
                        try:
                            x = self.str_to_list(lines[0])
                            mu = int(self.mu.toPlainText())
                            alpha = float(self.alpha.toPlainText())
                            sigma = int(self.sigma.toPlainText())
                        except:
                            self.label_2.setText("ERROR failed u test!")
                        else:
                            res = self.u_test(X=x, mu=mu, sigma=sigma, alpha=alpha)
                            self.label_2.setText(res)
                    else:
                        self.label_2.setText("Give me a list!")

        if distribution == "Normal":

            try:
                self.label_2.setText("")

                m = float(self.mu.toPlainText())
                s = float(sqrt(float(self.sigma.toPlainText())))
                X = Normal("X", m, s)
                x = symbols("x")

                if operation_type == "Probability":
                    if self.lineEdit_2.toPlainText() == "":
                        self.label_2.setText("Give a condition for the probability!")
                    else:
                        condition = sympify(
                            self.lineEdit_2.toPlainText(), locals={"X": X}
                        )
                        self.label_2.setText(str(N(P(condition))))

                elif operation_type == "Expected value":
                    self.label_2.setText(str(E(X)))

                elif operation_type == "Entropy":
                    try:
                        self.label_2.setText(str(entropy(X)))
                    except:
                        self.label_2.setText("Hiba")
                    else:
                        self.label_2.setText(str(round(entropy(X).evalf(), 4)))

                elif operation_type == "Variancia":
                    self.label_2.setText(str(variance(X)))

                elif operation_type == "Density function":
                    self.label_2.setText(str(density(X)(x)))
                    func_str = self.label_2.text()
                    self.canvas.plot_function(
                        func_str, interval_x=(-5, 5), interval_y=(0, 1)
                    )
                #
            except:
                self.label_2.setText("ERROR incorrect Normal value!")

        elif distribution == "Geometric":
            try:
                self.label_2.setText("")
                try:
                    p = float(self.mu.toPlainText())
                except ValueError:
                    self.label_2.setText("ERROR incorrect input!")
                else:
                    if p <= 0.0 or p >= 1.0:
                        self.label_2.setText(
                            "The probability should be between 0 and 1"
                        )
                    else:
                        X = Geometric("X", p)
                        x = symbols("x")
                        if operation_type == "Probability":
                            if self.lineEdit_2.toPlainText() == "":
                                self.label_2.setText(
                                    "Give a condition for the probability!"
                                )
                            else:
                                condition = sympify(
                                    self.lineEdit_2.toPlainText(), locals={"X": X}
                                )
                                self.label_2.setText(str(P(condition)))
                        if operation_type == "Expected value":
                            self.label_2.setText(str(E(X)))
                        elif operation_type == "Entropy":
                            self.label_2.setText(str(entropy(X)))
                        elif operation_type == "Variancia":
                            self.label_2.setText(str(variance(X)))
                        elif operation_type == "Density function":
                            self.label_2.setText(str((1 - p) ** x * p))
                            func_str = self.label_2.text()
                            self.canvas.plot_function(
                                func_str, interval_x=(-5, 5), interval_y=(0, 1)
                            )
            except:
                self.label_2.setText("ERROR incorrect Geometric value!")

        elif distribution == "Poisson":
            try:
                self.label_2.setText("")
                λ_value = int(self.mu.toPlainText())
                if λ_value <= 0:
                    self.label_2.setText("Incorrect lambda variable!")
                else:
                    X = Poisson("X", λ_value)
                    x = symbols("x")
                    if operation_type == "Probability":
                        if self.lineEdit_2.toPlainText() == "":
                            self.label_2.setText(
                                "Give a condition for the probability!"
                            )
                        else:
                            condition = sympify(
                                self.lineEdit_2.toPlainText(), locals={"X": X}
                            )
                            self.label_2.setText(str(N(P(condition))))
                    if operation_type == "Expected value":
                        self.label_2.setText(str(E(X)))
                    elif operation_type == "Entropy":
                        self.label_2.setText(
                            str(
                                0.5 * np.log(2 * np.pi * np.e * λ_value)
                                - 1 / (12 * λ_value)
                            )
                        )
                    elif operation_type == "Variancia":
                        self.label_2.setText(str(variance(X)))
                    elif operation_type == "Density function":
                        self.label_2.setText(str(density(X)(x)))
                        # JAVÍT vlmi nem jó
                        func_str = self.label_2.text()
                        self.canvas.plot_function(
                            func_str, interval_x=(0, 15), interval_y=(0, 1)
                        )
            except:
                self.label_2.setText("ERROR: incorrect Poisson's ratio!")

        elif distribution == "Logarithmic":
            self.label_2.setText("")
            try:
                P_s = sympify(self.string_to_S(self.mu.toPlainText()))
                p = float(eval(self.mu.toPlainText()))
                if p <= 0.0 or p >= 1.0:
                    self.label_2.setText("The probability must be between 0 and 1")
                else:
                    X = Logarithmic("X", P_s)
                    x = symbols("x")
                    if operation_type == "Probability":
                        if self.lineEdit_2.toPlainText() == "":
                            self.label_2.setText("Give me a condition!")
                        else:
                            condition = sympify(
                                self.lineEdit_2.toPlainText(), locals={"X": X}
                            )
                            self.label_2.setText(str(P(condition).evalf()))
                    if operation_type == "Expected value":
                        self.label_2.setText(str(E(X).evalf()))
                    elif operation_type == "Entropy":
                        self.label_2.setText(str(self.logarithmic_entropy(p)))
                    elif operation_type == "Variancia":
                        self.label_2.setText(str(variance(X).evalf()))
                    elif operation_type == "Density function":
                        result = density(X)(x)
                        # JAVÍT vlmi nem jó
                        self.label_2.setText(str(result))
                        func_str = self.label_2.text()
                        self.canvas.plot_function(func_str, (0, 15))
            except Exception as x:
                print(x)
                self.label_2.setText("ERROR incorrect Logarithmic value!")

        elif distribution == "Erlang":
            self.label_2.setText("")
            try:
                k = int(self.mu.toPlainText())
                l = float(self.sigma.toPlainText())
                X = Erlang("X", k, l)
                x = symbols("x")

                if operation_type == "Probability":
                    if self.lineEdit_2.toPlainText() == "":
                        self.label_2.setText("Specify a condition!")
                    else:
                        condition = sympify(
                            self.lineEdit_2.toPlainText(), locals={"X": X}
                        )
                        self.label_2.setText(str(P(condition)))

                elif operation_type == "Expected value":
                    self.label_2.setText(str(E(X)))

                elif operation_type == "Entropy":
                    e = k - log(l) + log(gamma(k)) + (1 - k) * digamma(k)
                    try:
                        self.label_2.setText(str(e.evalf()))
                    except:
                        self.label_2.setText("ERROR")
                    else:
                        self.label_2.setText(str(e.evalf()))

                elif operation_type == "Variancia":
                    self.label_2.setText(str(variance(X)))

                elif operation_type == "Density function":
                    self.label_2.setText(str(density(X)(x)))
                    func_str = self.label_2.text()
                    self.canvas.plot_function(func_str, (0, 15))
            except Exception as e:
                print(e)
                self.label_2.setText("ERROR incorrect Erlang value!")

        elif distribution == "Pareto":
            try:
                xm = float(self.mu.toPlainText())
                alpha = float(self.sigma.toPlainText())
                X = Pareto("X", xm, alpha)
                x = symbols("x")

                if operation_type == "Probability":
                    if self.lineEdit_2.toPlainText() == "":
                        self.label_2.setText("Specify a condition!")
                    else:
                        condition = sympify(
                            self.lineEdit_2.toPlainText(), locals={"X": X}
                        )
                        self.label_2.setText(str(N(P(condition))))

                elif operation_type == "Expected value":
                    self.label_2.setText(str(E(X)))

                elif operation_type == "Entropy":
                    self.label_2.setText(str(math.log(xm / alpha) + 1 / alpha + 1))

                elif operation_type == "Variancia":
                    self.label_2.setText(str(variance(X)))

                elif operation_type == "Density function":
                    self.label_2.setText(str(density(X)(x)))
                    func_str = self.label_2.text()
                    self.canvas.plot_function(func_str, (xm, 15))
            except Exception as x:
                print(x)
                self.label_2.setText("ERROR incorrect Pareto value!")

    def handle_combobox2_change(self):
        distribution = self.comboBox_2.currentText()

        if distribution in [
            "Geometric",
            "Poisson",
            "Logarithmic",
            "Erlang",
            "Pareto",
        ]:
            self.sigma.hide()
            if distribution == "Geometric" or distribution == "Logarithmic":
                self.mu.setPlaceholderText("p")
                self.sigma.hide()
            elif distribution == "Poisson":
                self.mu.setPlaceholderText("lambda")
            elif distribution == "Erlang":
                self.sigma.show()
                self.mu.setPlaceholderText("k")
                self.sigma.setPlaceholderText("l")
            elif distribution == "Pareto":
                self.sigma.show()
                self.mu.setPlaceholderText("xm")
                self.sigma.setPlaceholderText("alpha")
        elif distribution in [
            "Single sample t test",
            "Two-sample paired t test",
            "Two sample t test",
        ]:
            if distribution == "Single sample t test":
                self.mu.show()
                self.mu.setPlaceholderText("m")
                self.sigma.show()
                self.sigma.setPlaceholderText("alpha")
                self.lineEdit_2.setPlaceholderText("X values separated by " "," "")
            if (
                distribution == "Two sample t test"
                or distribution == "Two-sample paired t test"
            ):
                self.mu.hide()
                self.sigma.show()
                self.sigma.setPlaceholderText("alpha")
                self.lineEdit_2.setPlaceholderText(
                    "X Y values separated by " "," " in new line"
                )
        elif distribution in ["Single sample u test"]:
            self.lineEdit_2.setPlaceholderText(
                "X Y values separated by " "," " in new line"
            )
            self.mu.setPlaceholderText("m")
            self.alpha.show()
        else:
            self.alpha.hide()
            self.sigma.show()
            self.mu.show()
            self.lineEdit_2.setPlaceholderText("Condition: X < 12")
            self.mu.setPlaceholderText("μ")
            self.sigma.setPlaceholderText("σ2")

    def handle_combobox_change(self):
        text = self.comboBox.currentText()
        current_distribution = (
            self.comboBox_2.currentText()
        )  # Save the current selection
        eloszlások = [
            "Normal",
            "Geometric",
            "Poisson",
            "Logarithmic",
            "Erlang",
            "Pareto",
        ]
        t = ["Single sample t test", "Two-sample paired t test", "Two sample t test"]
        u = ["Single sample u test"]

        if text == "Density function":
            self.canvas.show()
        else:
            self.canvas.hide()

        if text == "T test":
            self.label.hide()
            self.comboBox_2.clear()
            self.comboBox_2.addItems(t)
            self.sigma.setPlaceholderText("alpha")
        elif text == "U test":
            self.label.hide()
            self.mu.show()
            self.comboBox_2.clear()
            self.comboBox_2.addItems(u)
        else:
            self.label.show()
            self.comboBox_2.clear()
            self.comboBox_2.addItems(eloszlások)
            self.sigma.setPlaceholderText("sigma")

        # Restore the previous selection
        index = self.comboBox_2.findText(current_distribution)
        if index != -1:
            self.comboBox_2.setCurrentIndex(index)

        self.handle_combobox2_change()  # Ensure the UI updates correctly based on the new selection


def main():
    App = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(App.exec())


############################################
if __name__ == "__main__":
    main()
