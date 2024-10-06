from PyQt5.QtWidgets import QMainWindow, QApplication
import UI_files.Programmer_Calculator_GUI as Programmer_Calculator_GUI
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import re
from PyQt5.QtWidgets import QInputDialog


class Window(QMainWindow, Programmer_Calculator_GUI.Ui_Programmer_calc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.applyStylesheet(self)
        self.setFocusPolicy(Qt.StrongFocus)

        self.enter_pressed = True  # Set flag to true after pressing Enter
        self.error_displayed = False

        self.operations = []  # List to store operations
        self.operations2 = []  # List to store operations

        self.comboBox_3.currentTextChanged.connect(self.handle_combobox_3_change)

        self.bel_zj.clicked.connect(lambda: self.press_it("("))
        self.eight.clicked.connect(lambda: self.press_it("8"))
        self.D_hex.clicked.connect(lambda: self.press_it("D"))
        self.C_hex.clicked.connect(lambda: self.press_it("C"))
        self.three.clicked.connect(lambda: self.press_it("3"))
        self.minus.clicked.connect(lambda: self.press_it("-"))
        self.dot.clicked.connect(lambda: self.press_it("."))
        self.B_hex.clicked.connect(lambda: self.press_it("B"))
        self.clear.clicked.connect(lambda: self.press_it("DEL"))
        self.four.clicked.connect(lambda: self.press_it("4"))
        self.jobb_zj.clicked.connect(lambda: self.press_it(")"))
        self.one.clicked.connect(lambda: self.press_it("1"))
        self.nine.clicked.connect(lambda: self.press_it("9"))
        self.mod.clicked.connect(lambda: self.press_it("%"))
        self.A_hex.clicked.connect(lambda: self.press_it("A"))
        self.zero.clicked.connect(lambda: self.press_it("0"))
        self.two.clicked.connect(lambda: self.press_it("2"))
        self.six.clicked.connect(lambda: self.press_it("6"))
        self.F_hex.clicked.connect(lambda: self.press_it("F"))
        self.plusz.clicked.connect(lambda: self.press_it("+"))
        self.seven.clicked.connect(lambda: self.press_it("7"))
        self.equal.clicked.connect(lambda: self.evaluate_expression())
        self.five.clicked.connect(lambda: self.press_it("5"))
        self.divide.clicked.connect(lambda: self.press_it("/"))
        self.szorzas.clicked.connect(lambda: self.press_it("*"))
        self.sqrt.clicked.connect(lambda: self.press_it("SQRT"))
        self.E_hex.clicked.connect(lambda: self.press_it("E"))
        self.pi.clicked.connect(lambda: self.press_it("3.14"))
        self.fakt.clicked.connect(lambda: self.press_it("!"))
        self.XOR.clicked.connect(lambda: self.press_it(" XOR "))
        self.abs.clicked.connect(lambda: self.press_it("ABS "))
        self.log.clicked.connect(lambda: self.press_it("log "))
        self.x_xx_y.clicked.connect(lambda: self.press_it("**"))
        self.ones.clicked.connect(lambda: self.press_it("ones "))
        self.int_2.clicked.connect(lambda: self.press_it("int "))
        self.x_xx_1.clicked.connect(lambda: self.press_it("**-1"))
        self.twos.clicked.connect(lambda: self.press_it("twos "))
        self.AND.clicked.connect(lambda: self.press_it(" AND "))
        self.log2.clicked.connect(lambda: self.press_it("log2 "))
        self.OR.clicked.connect(lambda: self.press_it(" OR "))
        self.shift_left.clicked.connect(lambda: self.press_it("<<"))
        self.shift_right.clicked.connect(lambda: self.press_it(">>"))
        self.aaaa.clicked.connect(self.show_dialog)
        self.fact.clicked.connect(lambda: self.press_it("FACT"))

        self.operations_list2.itemClicked.connect(self.on_item_clicked2)
        self.operations_list.itemClicked.connect(self.on_item_clicked)

    def applyStylesheet(self, Programmer_calc):
        stylesheet = """
        QInputDialog{
            color: #FFFFFF;
            background-color: #2E2E2E;
            font-family: 'Courier New', Courier, monospace; /* Monospaced font */
            font-size: 20pt; /* Increase font size */
        }
        """
        Programmer_calc.setStyleSheet(stylesheet)

    def evaluate_expression(self):
        screen = self.Result.text()
        operation = screen  # Store the current operation

        if self.comboBox_3.currentText() == "Decimal":
            if "twos" in screen:
                try:
                    number = screen.split("twos ")[1]
                    answer = self.twos_complement(number, 10)
                    print("#LOG: kettes komlemens")
                except:
                    answer = None
                    self.Result.setText("Incorrect complement two!")
            elif "log2" in screen:
                try:
                    print("#LOG: log2")
                    answer = self.log_from_decimal(screen.split(" ")[1], 2)
                except:
                    answer = None
                    self.Result.setText("Incorrect 2 based logarithmic!")
            elif "log" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_decimal(screen.split(" ")[1], 10)
                except:
                    answer = None
                    self.Result.setText("Incorrect 10 based logarithmic!")
            elif "ABS" in screen:
                try:
                    print("#LOG: abs")
                    if "." in screen:
                        answer = abs(float((screen.split(" ")[1])))
                    else:
                        answer = abs(int((screen.split(" ")[1])))
                except:
                    answer = None
                    self.Result.setText("Incorrect abs!")
            elif "int" in screen:
                try:
                    answer = int(
                        self.round_down_number(
                            screen.split("int")[1], "decimal"
                        ).strip()
                    )
                    print("#LOG: kerekítés egészre")
                except:
                    answer = None
                    self.Result.setText("Incorrect rounding to the whole!")
            elif "ones" in screen:
                try:
                    answer = self.ones_complement(screen.split("ones")[1], 10)
                    print("#LOG: egyes komlemens")
                except:
                    answer = None
                    self.Result.setText("Wrong one complement!")
            elif (
                not self.contain_logical(screen)
                and self.contains_sqrt(screen)
                and self.only_one_fact(screen) == 0
            ):
                try:
                    answer = self.sqrt_func(screen, "decimal")
                    print("#LOG: csak gyökvonás")
                except:
                    answer = None
                    self.Result.setText("Incorrect rooting!")
            elif "<<" in screen or ">>" in screen:
                print("#LOG: shiftelés")
                try:
                    if "<<" in screen:
                        num = screen.split("<<")[0]
                        cnt = screen.split("<<")[1]
                        answer = self.shift_left_func(cnt, num)
                    if ">>" in screen:
                        num = screen.split(">>")[0]
                        cnt = screen.split(">>")[1]
                        answer = self.shift_right_func(cnt, num)
                except:
                    answer = None
                    self.Result.setText("Incorrect shifting!")
            elif (
                self.contain_arithmetic(screen)
                and not self.contain_logical(screen)
                and self.only_one_fact(screen) == 0
            ):
                try:
                    answer = eval(screen)
                    print("#LOG: csak aritmetikai")
                except:
                    answer = None
                    self.Result.setText("Incorrect arithmetic!")
            elif "FACT" in screen:
                try:
                    print("#LOG: FACT")
                    answer = self.convert_and_factorize(screen.split("FACT")[1])
                except:
                    answer = None
                    self.Result.setText("Incorrect factorisation!")
            elif self.only_one_fact(screen) == 1 and "!" in screen:
                try:
                    print("#LOG: factorial")
                    answer = self.factorial(screen.split("!")[0], "decimal")
                except:
                    answer = None
                    self.Result.setText("Incorrect factorial!")
            elif not self.contain_arithmetic(screen) and self.contain_logical(screen):
                try:
                    print("#LOG: csak logikai")
                    answer = self.logical_ops(screen)
                except:
                    answer = None
                    self.Result.setText("Incorrect logic!")
            else:
                try:
                    print("#LOG: egyébként")
                    answer = eval(screen)
                except:
                    self.Result.setText("Wrong action!")
                    answer = None
            if answer is not None:
                if isinstance(answer, float) and answer.is_integer():
                    answer = int(answer)
                self.Result.setText(str(answer))

                self.operations.append(f"{operation}")
                self.update_operations_display()

                self.operations2.append(f"{answer}")
                self.update_operations_display2()
            if type(answer) is int:
                binary_segments = self.decimal_to_decimal_64bit_segments(answer)
                self.n8_63.setText(f"64 {self.format_binary(binary_segments[0])} 48")
                self.h2_47.setText(f"47 {self.format_binary(binary_segments[1])} 32")
                self.t6_31.setText(f"31 {self.format_binary(binary_segments[2])} 16")
                self.nulla_15.setText(f"15 {self.format_binary(binary_segments[3])}  0")
            else:
                self.n8_63.setText(f"")
                self.h2_47.setText(f"")
                self.t6_31.setText(f"")
                self.nulla_15.setText(f"")
        elif self.comboBox_3.currentText() == "Octal":
            answer = 0
            if "twos" in screen:
                print("#LOG: kettes komlemens")
                try:
                    number = screen.split(" ")[1]
                    answer = self.twos_complement(number, 8)
                    print("#LOG: kettes komlemens")
                except:
                    answer = None
                    self.Result.setText("Incorrect complement two!")
            elif "**-" in screen:
                try:
                    print("#LOG: negatív kitevőjű")
                    number = screen.split("**")[0]
                    kitevő = int(screen.split("**")[1])
                    answer = self.power_octal(number, kitevő)
                except:
                    answer = None
                    self.Result.setText("Incorrect negative exponent!")
            elif "<<" in screen or ">>" in screen:
                print("#LOG: shiftelés")
                try:
                    if "<<" in screen:
                        number = screen.split("<<")[0]
                        shift_amount = int(screen.split("<<")[1])
                        answer = self.shift_octal_custom("<<", shift_amount, number)
                    if ">>" in screen:
                        number = screen.split(">>")[0]
                        shift_amount = int(screen.split(">>")[1])
                        answer = self.shift_octal_custom(">>", shift_amount, number)
                except:
                    answer = None
                    self.Result.setText("Incorrect shifting!")
            elif "ABS" in screen:
                try:
                    print("#LOG: abs")
                    answer = float(self.absolute_octal(screen.split(" ")[1]))
                except:
                    answer = None
                    self.Result.setText("Incorrect abs!")
            elif "log2" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_octal(screen.split(" ")[1], 2)
                except:
                    answer = None
                    self.Result.setText("Incorrect 2 based logarithmic!")
            elif "log" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_octal(screen.split(" ")[1], 10)
                except:
                    answer = None
                    self.Result.setText("Incorrect 10 based logarithmic!")
            elif self.only_one_fact(screen) == 1 and "!" in screen:
                try:
                    print("#LOG: faktoriális")
                    answer = int(self.factorial(screen.split("!")[0], "octal"))
                except:
                    answer = None
                    self.Result.setText("Incorrect factorial!")
            elif "int" in screen:
                print("#LOG: kerekítés egészre")
                try:
                    answer = int(
                        self.round_down_number(screen.split("int")[1], "octal").strip()
                    )

                    print("#LOG: kerekítés egészre")
                except:
                    answer = None
                    self.Result.setText("Incorrect rounding to the whole!")
            elif "ones" in screen:
                try:
                    number = screen.split(" ")[1]
                    answer = self.ones_complement(number, 8)
                    print("#LOG: egyes komlemens")
                except:
                    answer = None
                    self.Result.setText("Wrong one complement!")
            elif self.contain_arithmetic(screen) and not self.contain_logical(screen):
                print("# Aritmetikus oktál")
                try:
                    if not "." in self.evaluate_octal_expression(screen):
                        answer = int(self.evaluate_octal_expression(screen))
                    else:
                        answer = self.evaluate_octal_expression(screen)
                except:
                    answer = None
                    self.Result.setText("Incorrect arithmetic!")
            elif not self.contain_arithmetic(screen) and self.contain_logical(screen):
                print("#LOG: logikai oktál")
                try:
                    answer = int(self.evaluate_octal_logical_expression(screen))
                except:
                    answer = None
                    self.Result.setText("Incorrect logic!")
            elif "FACT" in screen:
                print("#LOG: faktorizáció")
                try:
                    answer = self.convert_and_factorize("0o" + screen.split("FACT")[1])
                except:
                    answer = None
                    self.Result.setText("Incorrect factorisation!")
            else:
                print("#LOG: egyéb")
                try:
                    answer = int(self.evaluate_octal_expression(screen))
                except:
                    self.Result.setText("Wrong action!")
            if answer is not None:
                self.Result.setText(str(answer))

                self.operations.append(f"{operation}")
                self.update_operations_display()

                self.operations2.append(f"{answer}")
                self.update_operations_display2()
            if type(answer) is int:
                octal_segments = self.octal_octal_to_64bit_segments(answer)
                self.n8_63.setText(f"64 {self.format_binary(octal_segments[1])} 48")
                self.h2_47.setText(f"47 {self.format_binary(octal_segments[2])} 32")
                self.t6_31.setText(f"31 {self.format_binary(octal_segments[2])} 16")
                self.nulla_15.setText(f"15 {self.format_binary(octal_segments[3])} 0")
            else:
                self.n8_63.setText(f"")
                self.h2_47.setText(f"")
                self.t6_31.setText(f"")
                self.nulla_15.setText(f"")
        elif self.comboBox_3.currentText() == "Binary":
            answer = 0
            if "twos" in screen:
                try:
                    number = screen.split(" ")[1]
                    answer = self.twos_complement(number, 2)
                    print("#LOG: kettes komlemens")
                except:
                    answer = None
                    self.Result.setText("Incorrect complement two!")
            elif (
                self.only_one_fact(screen) == 1
                and "!" in screen
                and not self.contain_arithmetic(screen)
            ):
                try:
                    print("#LOG: factorial")
                    answer = self.factorial(screen.split("!")[0], "binary")
                except:
                    answer = None
                    self.Result.setText("Incorrect factorial!")
            elif "int" in screen:
                try:
                    answer = self.round_down_number(
                        screen.split("int")[1], "binary"
                    ).strip()
                    print("#LOG: kerekítés egészre")
                except:
                    answer = None
                    self.Result.setText("Incorrect rounding to the whole!")
            elif "log2" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_binary(screen.split(" ")[1], 2)
                except:
                    answer = None
                    self.Result.setText("Incorrect 2 based logarithmic!")
            elif "log" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_binary(screen.split(" ")[1], 10)
                except:
                    answer = None
                    self.Result.setText("Incorrect 10 based logarithmic!")
            elif "ABS" in screen:
                print("#LOG: abszolut érték")
                try:

                    answer = self.abs_binary(screen.split(" ")[1])
                except:
                    answer = None
                    self.Result.setText("Incorrect abs!")
            elif "ones" in screen:
                try:
                    answer = self.ones_complement(screen.split("ones")[1], 2)
                    print("#LOG: egyes komlemens")
                except:
                    answer = None
                    self.Result.setText("Wrong one complement!")
            elif "<<" in screen or ">>" in screen:
                print("#LOG: shiftelés")
                try:
                    if "<<" in screen:
                        number = screen.split("<<")[0]
                        shift_amount = screen.split("<<")[1]
                        answer = self.shift_binary_custom("<<", shift_amount, number)
                    if ">>" in screen:
                        number = screen.split(">>")[0]
                        shift_amount = screen.split(">>")[1]
                        answer = self.shift_binary_custom(">>", shift_amount, number)
                except:
                    answer = None
                    self.Result.setText("Incorrect shifting!")
            elif not self.contain_logical(screen) and self.contains_sqrt(screen):
                print("#LOG: gyökvonás")
                try:
                    answer = self.sqrt_func(screen, "binary")
                except:
                    answer = None
                    self.Result.setText("Incorrect root!")
            elif self.contain_arithmetic(screen) and not self.contain_logical(screen):
                print("#LOG: aritmetikai müvelet")
                try:
                    answer = self.evaluate_binary_expression(screen)
                except:
                    answer = None
                    self.Result.setText("Incorrect arithmetic!")
            elif "FACT" in screen:
                print("#LOG: faktorizáció")
                try:
                    answer = self.convert_and_factorize("0b" + screen.split("FACT")[1])
                except:
                    answer = None
                    self.Result.setText("Incorrect factorisation!")
            elif not self.contain_arithmetic(screen) and self.contain_logical(screen):
                print("#LOG: logikai")
                try:
                    answer = self.evaluate_binary_logical_expression(screen)
                except:
                    answer = None
                    self.Result.setText("Incorrect logic!")
            else:
                print("#LOG: egyéb")
                try:
                    answer = self.evaluate_binary_expression(screen)
                except:
                    self.Result.setText("Wrong action!")
            if answer is not None and answer is not False:
                self.Result.setText(str(answer))

                self.operations.append(f"{operation}")
                self.update_operations_display()

                self.operations2.append(f"{answer}")
                self.update_operations_display2()
            if type(answer) is str and not "." in answer and answer is not False:
                if type(answer) is str and not "." in answer and answer is not False:
                    try:
                        binary_segments = self.binary_tobinary_64bit_segments(answer)
                        if binary_segments is False:
                            raise ValueError(
                                "Error: Invalid binary input for 64-bit segmentation."
                            )
                    except Exception as e:
                        print(e)
                        self.Result.setText("Not representable on 64 bit!")
                    else:
                        self.n8_63.setText(
                            f"64 {self.format_binary(binary_segments[0])} 48"
                        )
                        self.h2_47.setText(
                            f"47 {self.format_binary(binary_segments[1])} 32"
                        )
                        self.t6_31.setText(
                            f"31 {self.format_binary(binary_segments[2])} 16"
                        )
                        self.nulla_15.setText(
                            f"15 {self.format_binary(binary_segments[3])}  0"
                        )
            else:
                self.n8_63.setText(f"")
                self.h2_47.setText(f"")
                self.t6_31.setText(f"")
                self.nulla_15.setText(f"")
        elif self.comboBox_3.currentText() == "Hexadecimal":
            answer = 0
            if "twos" in screen:
                try:
                    number = screen.split("twos ")[1]
                    answer = self.twos_complement(number, 16)
                    print("#LOG: kettes komlemens")
                except:
                    answer = None
                    self.Result.setText("Incorrect complement two!")
            elif "log2" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_hex(screen.split(" ")[1], 2)
                except:
                    answer = None
                    self.Result.setText("Incorrect 2 based logarithmic!")
            elif "log" in screen:
                try:
                    print("#LOG: log")
                    answer = self.log_from_hex(screen.split(" ")[1], 10)
                except:
                    answer = None
                    self.Result.setText("Incorrect 10 based logarithmic!")
            elif "ABS" in screen:
                try:
                    answer = self.abs_hex(screen.split(" ")[1])
                    print("#LOG: abs")
                except:
                    answer = None
                    self.Result.setText("Incorrect abs!")
            elif (
                self.only_one_fact(screen) == 1
                and "!" in screen
                and not self.contain_arithmetic(screen)
            ):
                try:
                    print("#LOG: factorial")
                    answer = self.factorial(screen.split("!")[0], "hexadecimal")
                except:
                    answer = None
                    self.Result.setText("Incorrect factorial!")
            elif "int" in screen:
                try:
                    answer = self.evaluate_hex_expression(
                        self.round_down_number(screen.split("int")[1], "hex").strip()
                    )
                    print("#LOG: kerekítés egészre")
                except:
                    answer = None
                    self.Result.setText("Incorrect rounding to the whole!")
            elif "ones" in screen:
                try:
                    number = screen.split(" ")[1]
                    answer = self.ones_complement(number, 16)
                    print("#LOG: egyes komlemens")
                except:
                    answer = None
                    self.Result.setText("Wrong one complement!")
            elif self.contain_arithmetic(screen) and not self.contain_logical(screen):
                try:
                    answer = self.evaluate_hex_expression(screen)
                    print("#LOG: artimetikai")
                except:
                    answer = None
                    self.Result.setText("Incorrect artimetics!")
            elif not self.contain_arithmetic(screen) and self.contain_logical(screen):
                try:
                    answer = self.evaluate_logical_hex_expression(screen)
                    print("#LOG: logikai")
                except:
                    answer = None
                    self.Result.setText("Incorrect logic!")
            elif "FACT" in screen:
                try:
                    print("#LOG: faktorizáció")
                    if screen.split("FACT")[1] != "0":
                        answer = self.convert_and_factorize(
                            "0x" + screen.split("FACT")[1]
                        )
                    else:
                        answer = "0"
                except:
                    answer = None
                    self.Result.setText("Incorrect factorisation!")
            elif "<<" in screen or ">>" in screen:
                print("#LOG: shiftelés")
                try:
                    if "<<" in screen:
                        num = screen.split("<<")[0]
                        cnt = screen.split("<<")[1]
                        answer = self.hex_shift_left_func(cnt, num)
                    if ">>" in screen:
                        num = screen.split(">>")[0]
                        cnt = screen.split(">>")[1]
                        answer = self.hex_shift_right_func(cnt, num)
                except:
                    answer = None
                    self.Result.setText("Incorrect shifting!")
            else:
                try:
                    answer = self.evaluate_hex_expression(screen)
                    print("#LOG else")
                except:
                    self.Result.setText("Incorrect not hex value!")
            if answer is not None:
                self.Result.setText(str(answer))
                self.operations.append(f"{operation}")
                self.update_operations_display()

                self.operations2.append(f"{answer}")
                self.update_operations_display2()
            if (
                isinstance(answer, str)
                and not "." in answer
                and not "*" in answer
                and answer != "0"
            ):
                binary_segments = self.hexidecimal_to_hexidecimal_64bit_segments(
                    str(answer)
                )
                self.n8_63.setText(f"64 {self.format_binary(binary_segments[0])} 48")
                self.h2_47.setText(f"47 {self.format_binary(binary_segments[1])} 32")
                self.t6_31.setText(f"31 {self.format_binary(binary_segments[2])} 16")
                self.nulla_15.setText(f"15 {self.format_binary(binary_segments[3])}  0")
            else:
                self.n8_63.setText(f"")
                self.h2_47.setText(f"")
                self.t6_31.setText(f"")
                self.nulla_15.setText(f"")

    def set_to_null(self, list1, list2):
        for i in list1:
            i.setEnabled(True)

        self.pi.setEnabled(True)
        self.sqrt.setEnabled(True)
        self.dot.setEnabled(True)
        for i in list2:
            i.setEnabled(True)

    def handle_combobox_3_change(self):
        text = self.comboBox_3.currentText()

        hex_buttons = [
            self.A_hex,
            self.B_hex,
            self.C_hex,
            self.D_hex,
            self.E_hex,
            self.F_hex,
        ]
        numbers = [
            self.zero,
            self.one,
            self.two,
            self.three,
            self.four,
            self.five,
            self.six,
            self.seven,
            self.eight,
            self.nine,
        ]

        if text == "Binary":
            self.set_to_null(hex_buttons, numbers)
            for i in hex_buttons:
                i.setEnabled(False)

            self.pi.setEnabled(False)

            for i in range(2, len(numbers)):
                numbers[i].setEnabled(False)
        elif text == "Octal":
            self.set_to_null(hex_buttons, numbers)
            self.pi.setEnabled(False)
            self.sqrt.setEnabled(False)
            for i in hex_buttons:
                i.setEnabled(False)

            for i in range(8, len(numbers)):
                numbers[i].setEnabled(False)
        elif text == "Decimal":
            self.set_to_null(hex_buttons, numbers)
            for i in hex_buttons:
                i.setEnabled(False)
        elif text == "Hexadecimal":
            self.set_to_null(hex_buttons, numbers)
            self.pi.setEnabled(False)
            self.sqrt.setEnabled(False)

    def show_dialog(self):
        text, ok = QInputDialog.getText(self.centralwidget, "", "Enter a character::")
        if ok and text and len(text) == 1:
            ascii_value = ord(text)
            current_mode = self.comboBox_3.currentText()

            if current_mode == "Decimal":
                converted_value = str(ascii_value)
            elif current_mode == "Hexadecimal":
                converted_value = hex(ascii_value)[
                    2:
                ].upper()  # Convert to hex and remove '0x' prefix
            elif current_mode == "Binary":
                converted_value = bin(ascii_value)[
                    2:
                ]  # Convert to binary and remove '0b' prefix
            elif current_mode == "Octal":
                converted_value = oct(ascii_value)[
                    2:
                ]  # Convert to octal and remove '0o' prefix

            self.Result.setText(converted_value)

    def press_it(self, pressed):
        if pressed == "DEL":
            self.Result.setText("0")
        elif "Incorrect" in self.Result.text() and pressed:
            self.Result.setText(pressed)
            # Check to see if it starts with 0 and delete the zero
        elif self.Result.text() == "0":
            self.Result.setText(pressed)
        # concatenate the pressed button with what was there already
        else:
            self.Result.setText(f"{self.Result.text()}{pressed}")

    def is_prime(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def factorize(self, n):
        if self.is_prime(n):
            return [n]

        factors = []
        divisor = 2
        while n >= 2:
            if n % divisor == 0:
                factors.append(divisor)
                n //= divisor
            else:
                divisor += 1
                while not self.is_prime(divisor):
                    divisor += 1
        return factors

    def convert_and_factorize(self, input_num):

        # Determine the base of the input number
        if input_num.startswith("0b"):
            base = 2
        elif input_num.startswith("0x"):
            base = 16
        elif input_num.startswith("0o"):
            base = 8
        else:
            base = 10

        # Convert the number to decimal
        decimal_number = int(input_num, base)

        # Factorize the decimal number
        factors = self.factorize(decimal_number)

        # Convert factors back to the original base
        if base == 2:
            factors_str = "*".join(bin(f)[2:] for f in factors)
        elif base == 16:
            factors_str = "*".join(hex(f)[2:] for f in factors).upper()
        elif base == 8:
            factors_str = "*".join(oct(f)[2:] for f in factors)
        else:
            factors_str = "*".join(map(str, factors))

        return factors_str

    def factorial(self, num_str, num_system):
        # Determine the base and convert to decimal
        if num_system == "binary":
            base = 2
        elif num_system == "octal":
            base = 8
        elif num_system == "hexadecimal":
            base = 16
        elif num_system == "decimal":
            base = 10
        else:
            raise ValueError("Invalid number system")

        # Convert to decimal float
        decimal_num = float(int(num_str, base)) if base != 10 else float(num_str)

        # Calculate factorial
        def calc_factorial(n):
            if n < 0:
                raise ValueError("Factorial is not defined for negative numbers")
            elif n == 0 or n == 1:
                return 1
            elif n != int(n):
                return math.gamma(n + 1)  # Gamma(n+1) is the factorial for non-integers
            else:
                return math.factorial(int(n))  # Use math.factorial for integer values

        factorial_result = calc_factorial(decimal_num)

        # Convert the result back to the original format
        if base == 2:
            result = bin(int(factorial_result))[2:]
        elif base == 8:
            result = oct(int(factorial_result))[2:]
        elif base == 16:
            result = hex(int(factorial_result))[2:].upper()
        else:
            result = str(factorial_result)

        return result

    def only_one_fact(self, string):
        cnt = 0
        for i in string:
            if i == "!":
                cnt += 1

        return cnt

    def twos_complement(self, number: str, base: int) -> str:
        # Convert the input number to an integer
        if base == 2:
            int_number = int(number, 2)
        elif base == 8:
            int_number = int(number, 8)
        elif base == 10:
            int_number = int(number)
        elif base == 16:
            int_number = int(number, 16)
        else:
            raise ValueError("Base must be one of 2, 8, 10, or 16")

        # Calculate one's complement by flipping the bits
        max_num = (1 << 64) - 1
        ones_complement_int = int_number ^ max_num

        # Calculate two's complement by adding one to the one's complement result
        twos_complement_int = ones_complement_int + 1
        if "-" in number:
            if base == 2:
                result = bin(twos_complement_int)[3:].zfill(
                    64
                )  # Remove the '0b' prefix and pad with zeros
            elif base == 8:
                result = oct(twos_complement_int)[3:].zfill(
                    64 // 3
                )  # Remove the '0o' prefix and pad with zeros
            elif base == 10:
                result = str(twos_complement_int)[1:]  # No prefix for decimal
            elif base == 16:
                result = (
                    hex(twos_complement_int)[3:].upper().zfill(64 // 4)
                )  # Remove the '0x' prefix and pad with zeros
        else:
            if base == 2:
                result = bin(twos_complement_int)[2:].zfill(
                    64
                )  # Remove the '0b' prefix and pad with zeros
            elif base == 8:
                result = oct(twos_complement_int)[2:].zfill(
                    64 // 3
                )  # Remove the '0o' prefix and pad with zeros
            elif base == 10:
                result = str(twos_complement_int)  # No prefix for decimal
            elif base == 16:
                result = (
                    hex(twos_complement_int)[2:].upper().zfill(64 // 4)
                )  # Remove the '0x' prefix and pad with zeros

        return result

    def ones_complement(self, number: str, base: int) -> str:
        if "-" in number:
            number = number.replace("-", "")
        # Convert the input number to an integer
        if base == 2:
            int_number = int(number, 2)
        elif base == 8:
            int_number = int(number, 8)
        elif base == 10:
            int_number = int(number)
        elif base == 16:
            int_number = int(number, 16)
        else:
            raise ValueError("Base must be one of 2, 8, 10, or 16")

        # Calculate one's complement by flipping the bits
        max_num = (1 << 64) - 1
        ones_complement_int = int_number ^ max_num

        # Convert back to the original base
        if base == 2:
            result = bin(ones_complement_int)[2:].zfill(
                64
            )  # Remove the '0b' prefix and pad with zeros
        elif base == 8:
            result = oct(ones_complement_int)[2:].zfill(
                64 // 3
            )  # Remove the '0o' prefix and pad with zeros
        elif base == 10:
            result = ones_complement_int
        elif base == 16:
            result = (
                hex(ones_complement_int)[2:].upper().zfill(64 // 4)
            )  # Remove the '0x' prefix and pad with zeros

        return result

    def round_down_number(self, number: str, mode: str) -> str:
        # Check if the input number is valid
        if number.replace("-", "").replace(".", "").isdigit():
            raise ValueError(
                "Invalid input: number must contain only digits and at most one decimal point."
            )

        negative = number.startswith("-")
        if negative:
            number = number[1:]

        if "." in number:
            integer_part, _ = number.split(".")
        else:
            integer_part = number

        if negative:
            integer_part = "-" + integer_part

        return integer_part

    def shift_left_func(self, num: str, number: str):
        # Calculate the new number by shifting to the left
        new_number = int(number) << int(num)

        # Return the new number as a string
        return new_number

    def shift_right_func(self, num: str, number: str):
        # Calculate the new number by shifting to the right
        new_number = int(number) >> int(num)

        # Return the new number as a string
        return new_number

    def abs_hex(self, hex_str):
        """
        Return the absolute value of a hexadecimal number given as a string.

        Parameters:
        hex_str (str): The hexadecimal string representing the number.

        Returns:
        str: The absolute value of the hexadecimal number in hexadecimal format.
        """

        def hex_to_decimal(hex_str):
            """Convert a hexadecimal string to a decimal float."""
            if "." in hex_str:
                int_part, frac_part = hex_str.split(".")
                int_value = int(int_part, 16)
                frac_value = sum(
                    int(digit, 16) * 16**-i for i, digit in enumerate(frac_part, 1)
                )
                return int_value + frac_value
            else:
                return int(hex_str, 16)

        def decimal_to_hex(decimal_num):
            """Convert a decimal number to a hexadecimal string."""
            if decimal_num == 0:
                return "0.0"

            int_part = int(decimal_num)
            frac_part = decimal_num - int_part

            int_hex = hex(int_part).lstrip("0x").upper() + "."

            frac_hex = ""
            while frac_part:
                frac_part *= 16
                digit = int(frac_part)
                frac_part -= digit
                frac_hex += hex(digit).lstrip("0x").upper()
                if (
                    len(frac_hex) > 8
                ):  # limiting the length of the fractional part to 8 digits
                    break

            return int_hex + frac_hex if frac_hex else int_hex.rstrip(".")

            # Remove the negative sign if it exists

        if hex_str.startswith("-"):
            hex_str = hex_str[1:]

        # Convert hexadecimal string to decimal
        decimal_value = hex_to_decimal(hex_str)

        # Get the absolute value
        abs_value = abs(decimal_value)

        # Convert the absolute decimal value back to a hexadecimal string
        return decimal_to_hex(abs_value)

    def log_from_hex(self, hex_str, base=10):
        """
        Calculate the logarithm of a hexadecimal number and return the result in binary and hexadecimal formats.

        Parameters:
        hex_str (str): The hexadecimal string representing the number.
        base (int): The base of the logarithm (default is 10, can also be 2).

        Returns:
        tuple: The logarithm of the hexadecimal number in binary and hexadecimal formats, limited to 8 decimal places.
        """

        def hex_to_decimal(hex_str):
            """Convert a hexadecimal string to a decimal float."""
            return int(hex_str, 16)

        def float_to_binary(value):
            """Convert a float to a binary string limited to 8 decimal places."""
            if value == 0:
                return "0.0"

            int_part = int(value)
            frac_part = value - int_part

            int_bin = bin(int_part).lstrip("0b") + "."

            frac_bin = ""
            for _ in range(8):
                frac_part *= 2
                bit = int(frac_part)
                frac_part -= bit
                frac_bin += str(bit)
                if frac_part == 0:
                    break

            return int_bin + frac_bin

        def float_to_hex(value):
            """Convert a float to a hexadecimal string limited to 8 decimal places."""
            if value == 0:
                return "0.0"

            int_part = int(value)
            frac_part = value - int_part

            int_hex = hex(int_part).lstrip("0x").upper() + "."

            frac_hex = ""
            for _ in range(8):
                frac_part *= 16
                digit = int(frac_part)
                frac_part -= digit
                frac_hex += hex(digit).lstrip("0x").upper()
                if frac_part == 0:
                    break

            return int_hex + frac_hex

        # Convert the hexadecimal string to a decimal number
        decimal_value = hex_to_decimal(hex_str)

        # Check for valid base
        if base not in [2, 10]:
            return "Invalid base. Only base 2 and base 10 are supported."

        # Calculate the logarithm of the decimal value
        log_value = math.log(decimal_value, base)

        # Convert the result to binary and hexadecimal strings
        return float_to_hex(log_value)

    def is_valid_hex(self, number: str) -> bool:
        try:
            int(number, 16)
            return True
        except ValueError:
            return False

    def hex_shift_left_func(self, num: str, hex_number: str) -> str:
        # Ensure the input hex number is valid
        if not self.is_valid_hex(hex_number):
            raise ValueError("The provided number is not a valid hexadecimal")

        new_number = int(hex_number, 16) << int(num)

        return hex(new_number)[2:].upper()

    def hex_shift_right_func(self, num: str, hex_number: str) -> str:
        # Ensure the input hex number is valid
        if not self.is_valid_hex(hex_number):
            raise ValueError("The provided number is not a valid hexadecimal")

        # Calculate the new number by shifting to the right
        new_number = int(hex_number, 16) >> int(num)

        # Return the new number as a hexadecimal string
        return (hex(new_number))[2:].upper()

    def evaluate_logical_hex_expression(self, expression: str) -> str:
        # Split the expression into parts
        tokens = expression.split()

        # Convert the first hex number to an integer
        result = int(tokens[0], 16)

        # Iterate over the tokens and perform operations
        i = 1
        while i < len(tokens):
            operator = tokens[i]
            next_num = int(tokens[i + 1], 16)

            if operator == "OR":
                result |= next_num
            elif operator == "XOR":
                result ^= next_num
            elif operator == "AND":
                result &= next_num

            i += 2

        # Convert the result back to a hexadecimal string and return it
        return hex(result).upper()[2:]

    def contains_sqrt(self, string):
        for i in string:
            if "SQRT" in string:
                return True
        return False

    def contain_arithmetic(self, string):
        contains_arithmetic = False
        arithmetic_exp = ["*", "/", "%", "-", "+"]

        for op in arithmetic_exp:
            if op in string:
                contains_arithmetic = True
                break

        return contains_arithmetic

    def contain_logical(self, string):
        contains_logical = False
        logical_exp = ["AND", "OR", "XOR", "NOT"]

        for op in logical_exp:
            if op in string:
                contains_logical = True
                break

        return contains_logical

    def format_binary(self, binary_string):
        # Insert a space every four characters
        formatted_string = " ".join(
            binary_string[i : i + 4] for i in range(0, len(binary_string), 4)
        )
        return formatted_string

    def decimal_to_decimal_64bit_segments(self, number):
        if not isinstance(number, int):
            return "Error: Input must be an integer."

        is_negative = number < 0

        # Convert decimal to binary string
        if is_negative:
            # Convert to a full 64-bit binary number with two's complement for negative numbers
            binary_string = bin((1 << 64) + number)[2:]
        else:
            binary_string = bin(number)[2:]

        # Pad with leading zeros to make it 64 bits
        padded_binary = binary_string.zfill(64)

        # Ensure it is exactly 64 bits by taking the last 64 bits
        padded_binary = padded_binary[-64:]

        # Split into 16-bit chunks
        chunks = [padded_binary[i : i + 16] for i in range(0, 64, 16)]

        return chunks

    def octal_octal_to_64bit_segments(self, octal_number):
        is_negative = octal_number < 0

        # Convert octal to binary string
        binary_string = bin(int(str(abs(octal_number)), 8))[2:]

        if is_negative:
            # Convert to a full 64-bit binary number with two's complement for negative numbers
            binary_string = bin((1 << 64) - int(binary_string, 2))[2:]

        # Pad with leading zeros to make it 64 bits
        padded_binary = binary_string.zfill(64)

        # Ensure it is exactly 64 bits by taking the last 64 bits
        padded_binary = padded_binary[-64:]

        # Split into 16-bit chunks
        chunks = [padded_binary[i : i + 16] for i in range(0, 64, 16)]

        return chunks

    def evaluate_octal_expression(self, expression):
        # Define a helper function to convert octal to decimal
        def oct_to_dec(oct_str):
            return int(oct_str, 8)

        # Define a helper function to convert decimal to octal
        def dec_to_oct(dec_number):
            if isinstance(dec_number, float):
                integer_part = int(dec_number)
                fractional_part = dec_number - integer_part
                octal_integer = oct(integer_part)[2:]
                octal_fractional = ""
                for _ in range(10):  # Limit the fractional precision
                    fractional_part *= 8
                    octal_fractional += str(int(fractional_part))
                    fractional_part -= int(fractional_part)
                return f"{octal_integer}.{octal_fractional}".rstrip("0").rstrip(".")
            elif dec_number < 0:
                return "-" + oct(abs(int(dec_number)))[2:]
            return oct(int(dec_number))[2:]

        # Replace octal numbers with their decimal equivalents in the expression
        def replace_octal_with_decimal(expr):
            octal_numbers = re.findall(r"-?[0-7]+", expr)
            for oct_num in octal_numbers:
                expr = expr.replace(oct_num, str(oct_to_dec(oct_num)), 1)
            return expr

        # Replace octal numbers with decimal equivalents
        decimal_expression = replace_octal_with_decimal(expression)

        result = eval(decimal_expression)

        # Convert the result back to octal
        return dec_to_oct(result)

    def evaluate_octal_logical_expression(self, expression):
        # Define a helper function to convert octal to decimal
        def oct_to_dec(oct_str):
            return int(oct_str, 8)

        # Define a helper function to convert decimal to octal
        def dec_to_oct(dec_int):
            return oct(dec_int)[2:]

        # Replace octal numbers with their decimal equivalents in the expression
        def replace_octal_with_decimal(expr):
            octal_numbers = re.findall(r"\b[0-7]+\b", expr)
            for oct_num in octal_numbers:
                expr = expr.replace(oct_num, str(oct_to_dec(oct_num)), 1)
            return expr

        # Define the logical operators and their corresponding lambda functions
        logical_ops = {
            "AND": lambda a, b: a & b,
            "OR": lambda a, b: a | b,
            "XOR": lambda a, b: a ^ b,
            "NOT": lambda a: ~a
            & (
                (1 << 63) - 1
            ),  # Ensure NOT operation results in a 63-bit unsigned value
        }

        # Replace octal numbers with decimal equivalents
        decimal_expression = replace_octal_with_decimal(expression)

        # Tokenize the expression into numbers and operators
        tokens = re.split(r"(\bAND\b|\bOR\b|\bXOR\b|\bNOT\b|\s+)", decimal_expression)
        tokens = [token.strip() for token in tokens if token.strip()]

        # Process the tokens to handle logical operations
        def process_tokens(tokens):
            # Stack for numbers and operators
            num_stack = []
            op_stack = []

            def apply_operator():
                op = op_stack.pop()
                if op == "NOT":
                    num = num_stack.pop()
                    num_stack.append(logical_ops[op](num))
                else:
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    num_stack.append(logical_ops[op](num1, num2))

            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token in logical_ops:
                    if token == "NOT":
                        op_stack.append(token)
                    else:
                        while op_stack and op_stack[-1] in logical_ops:
                            apply_operator()
                        op_stack.append(token)
                else:
                    num_stack.append(int(token))
                    while op_stack and op_stack[-1] == "NOT":
                        apply_operator()
                i += 1

            while op_stack:
                apply_operator()

            return num_stack[0]

        # Evaluate the expression
        try:
            result = process_tokens(tokens)
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {e}"

        # Convert the result back to octal
        octal_result = dec_to_oct(result)

        # Ensure the result is in 64-bit octal format and starts with 1
        if "NOT" in expression:
            octal_result = octal_result.zfill(22)
            if not octal_result.startswith("1"):
                octal_result = "1" + octal_result[1:]

        return octal_result

    def shift_octal_custom(self, operation, shift_amount, number):
        octal_value = int(number, 8)
        if operation == "<<":
            shifted_value = octal_value << shift_amount
        elif operation == ">>":
            shifted_value = octal_value >> shift_amount
        else:
            return None

        return int(str(oct(shifted_value))[2:])

    def absolute_octal(self, octal_str: str) -> str:
        if "." in octal_str:
            # Handle both integer and fractional parts separately
            integer_part, fractional_part = octal_str.split(".")

            # Convert integer part from octal to decimal
            decimal_integer = int(integer_part, 8)
            abs_decimal_integer = abs(decimal_integer)

            # Convert fractional part from octal to decimal
            decimal_fractional = sum(
                int(digit, 8) * (8 ** -(index + 1))
                for index, digit in enumerate(fractional_part)
            )
            abs_decimal_fractional = abs(decimal_fractional)

            # Combine the integer and fractional parts back into a single decimal number
            abs_decimal_number = abs_decimal_integer + abs_decimal_fractional

            # Convert the absolute decimal number back to octal
            abs_octal_integer = oct(abs_decimal_integer)[2:]

            # Convert the fractional part back to octal
            abs_octal_fractional = []
            fractional = abs_decimal_fractional
            for _ in range(10):  # Limit the precision to 10 digits
                fractional *= 8
                digit = int(fractional)
                abs_octal_fractional.append(str(digit))
                fractional -= digit
                if fractional == 0:
                    break

            # Return the combined absolute octal string
            return abs_octal_integer + "." + "".join(abs_octal_fractional)
        else:
            # Handle the integer-only case
            decimal_number = int(octal_str, 8)
            abs_decimal = abs(decimal_number)
            return oct(abs_decimal)[2:]

    def float_to_octal(self, f):
        """
        Convert a floating-point number to its octal representation as a string.

        Parameters:
        f (float): The floating-point number to convert.

        Returns:
        str: The octal representation of the floating-point number.
        """
        if f < 0:
            sign = "-"
            f = -f
        else:
            sign = ""

        # Separate the integer part and the fractional part
        integer_part = int(f)
        fractional_part = f - integer_part

        # Convert the integer part to octal
        octal_integer = oct(integer_part)[2:]

        # Convert the fractional part to octal
        octal_fraction = ""
        while (
            fractional_part != 0 and len(octal_fraction) < 12
        ):  # limit length to prevent infinite loop
            fractional_part *= 8
            digit = int(fractional_part)
            octal_fraction += str(digit)
            fractional_part -= digit

        return sign + octal_integer + "." + octal_fraction

    def power_octal(self, octal_str, power_value):
        """
        Calculate the result of raising an octal number to a given power and return the result as an octal string.

        Parameters:
        octal_str (str): The octal number as a string.
        power_value (float): The power to which the octal number is to be raised.

        Returns:
        str: The octal representation of the result after exponentiation.
        """

        # Convert the octal string to a decimal number
        decimal_value = int(octal_str, 8)

        # Perform the power operation
        result_value = decimal_value**power_value

        # Convert the result back to an octal string with fraction handling
        octal_result = self.float_to_octal2(result_value)

        return octal_result

    def float_to_octal2(self, f):
        """
        Convert a floating-point number to its octal representation as a string.

        Parameters:
        f (float): The floating-point number to convert.

        Returns:
        str: The octal representation of the floating-point number.
        """
        if f < 0:
            sign = "-"
            f = -f
        else:
            sign = ""

        # Separate the integer part and the fractional part
        integer_part = int(f)
        fractional_part = f - integer_part

        # Convert the integer part to octal
        octal_integer = oct(integer_part)[2:]

        # Convert the fractional part to octal
        octal_fraction = ""
        while (
            fractional_part != 0 and len(octal_fraction) < 12
        ):  # limit length to prevent infinite loop
            fractional_part *= 8
            digit = int(fractional_part)
            octal_fraction += str(digit)
            fractional_part -= digit

        return sign + octal_integer + ("." + octal_fraction if octal_fraction else "")

    def log_from_binary(self, binary_str, base=10):
        """
        Calculate the logarithm of a binary number and return the result in binary format.

        Parameters:
        binary_str (str): The binary string representing the binary number.
        base (int): The base of the logarithm (default is 10, can also be 2).

        Returns:
        str: The logarithm of the binary number in binary format, limited to 8 decimal places.
        """

        def binary_to_decimal(binary_str):
            """Convert a binary string to a decimal float."""
            return int(binary_str, 2)

        def float_to_binary(value):
            """Convert a float to a binary string limited to 8 decimal places."""
            if value == 0:
                return "0.0"

            int_part = int(value)
            frac_part = value - int_part

            int_bin = bin(int_part).lstrip("0b")
            if int_bin == "":
                int_bin = "0"  # Handle the case where the integer part is zero

            frac_bin = ""
            for _ in range(8):
                frac_part *= 2
                bit = int(frac_part)
                frac_part -= bit
                frac_bin += str(bit)
                if frac_part == 0:
                    break

            return int_bin + "." + frac_bin

        # Convert the binary string to a decimal number
        decimal_value = binary_to_decimal(binary_str)

        # Check for valid base
        if base not in [2, 10]:
            return "Invalid base. Only base 2 and base 10 are supported."

        # Calculate the logarithm of the decimal value
        log_value = math.log(decimal_value, base)

        # Convert the result to a binary string
        log_binary = float_to_binary(log_value)

        return log_binary

    def log_from_decimal(self, decimal_str, base=10):
        """
        Calculate the logarithm of a decimal number and return the result.

        Parameters:
        decimal_str (str): The decimal number as a string.
        base (int): The base of the logarithm (default is 10, can also be 2).

        Returns:
        float: The logarithm of the decimal number.
        """
        # Convert the decimal string to a float
        decimal_value = float(decimal_str)

        # Check for valid base
        if base not in [2, 10]:
            return "Invalid base. Only base 2 and base 10 are supported."

        # Calculate the logarithm of the decimal value
        log_value = math.log(decimal_value, base)
        return log_value

    def log_from_octal(self, octal_str, base=10):
        """
        Calculate the logarithm of an octal number and return the result in both decimal and octal format.

        Parameters:
        octal_str (str): The octal number as a string.
        base (int): The base of the logarithm (default is 10).

        Returns:
        tuple: A tuple containing the logarithm of the octal number in decimal and octal format.
        """
        # Convert the octal string to a decimal integer
        decimal_value = int(octal_str, 8)

        # Calculate the logarithm of the decimal value
        log_value = math.log(decimal_value, base)

        # Convert the logarithm result to octal float representation
        log_value_octal = self.float_to_octal(log_value)

        return log_value_octal

    def binary_tobinary_64bit_segments(self, binary_number):
        if not isinstance(binary_number, str):
            return "Error: Input must be a binary string."

        try:
            if binary_number[0] == "-":
                # Handle negative binary numbers
                binary_value = int(binary_number, 2)
                if binary_value >= 0:
                    raise ValueError(
                        "Invalid input: expected a negative number for two's complement representation."
                    )
                # Calculate the two's complement for a 64-bit representation
                padded_binary = format((1 << 64) + binary_value, "064b")
            else:
                # Handle positive binary numbers
                binary_value = int(binary_number, 2)
                padded_binary = format(binary_value, "064b")

            # Split the padded binary into four 16-bit chunks
            chunks = [padded_binary[i : i + 16] for i in range(0, 64, 16)]

            return chunks
        except:
            return False

    def evaluate_binary_expression(self, expression):
        # Define a helper function to convert binary to decimal
        def bin_to_dec(bin_str):
            if bin_str.startswith("-"):
                return -int(bin_str[1:], 2)
            return int(bin_str, 2)

        # Define a helper function to convert decimal to binary
        def dec_to_bin(dec_int):
            if dec_int < 0:
                return "-" + bin(-int(dec_int))[2:]
            return bin(int(dec_int))[2:]

        # Replace binary numbers with their decimal equivalents in the expression
        def replace_binary_with_decimal(expr):
            binary_numbers = re.findall(r"-?[01]+", expr)
            for bin_num in binary_numbers:
                expr = expr.replace(bin_num, str(bin_to_dec(bin_num)), 1)
            return expr

        # Replace binary numbers with decimal equivalents
        decimal_expression = replace_binary_with_decimal(expression)

        result = eval(decimal_expression)

        # Convert the result back to binary, including handling of fractions
        if isinstance(result, float):
            sign = "-" if result < 0 else ""
            integer_part = abs(int(result))
            fractional_part = abs(result) - integer_part
            binary_result = dec_to_bin(integer_part)
            if fractional_part > 0:
                binary_fraction = []
                while (
                    fractional_part and len(binary_fraction) < 10
                ):  # Limit to 10 fractional bits for simplicity
                    fractional_part *= 2
                    bit = int(fractional_part)
                    binary_fraction.append(str(bit))
                    fractional_part -= bit
                binary_result += "." + "".join(binary_fraction)
            return sign + binary_result

        return dec_to_bin(result)

    def evaluate_binary_logical_expression(self, expression):
        # Define a helper function to convert binary to decimal
        def bin_to_dec(bin_str):
            return int(bin_str, 2)

        # Define a helper function to convert decimal to binary
        def dec_to_bin(dec_int):
            return bin(dec_int)[
                2:
            ]  # Convert to binary without leading '0b' and remove padding

        # Replace binary numbers with their decimal equivalents in the expression
        def replace_binary_with_decimal(expr):
            binary_numbers = re.findall(r"\b[01]+\b", expr)
            for bin_num in binary_numbers:
                expr = expr.replace(bin_num, str(bin_to_dec(bin_num)), 1)
            return expr

        # Define the logical operators and their corresponding lambda functions
        logical_ops = {
            "AND": lambda a, b: a & b,
            "OR": lambda a, b: a | b,
            "XOR": lambda a, b: a ^ b,
            "NOT": lambda a: ~a
            & 0xFFFFFFFFFFFFFFFF,  # Ensure 64-bit representation for NOT
        }

        # Replace binary numbers with decimal equivalents
        decimal_expression = replace_binary_with_decimal(expression)

        # Tokenize the expression into numbers and operators
        tokens = re.split(r"(\bAND\b|\bOR\b|\bXOR\b|\bNOT\b)", decimal_expression)
        tokens = [token.strip() for token in tokens if token.strip()]

        # Process the tokens to handle logical operations
        def process_tokens(tokens):
            # Stack for numbers and operators
            num_stack = []
            op_stack = []

            def apply_operator():
                op = op_stack.pop()
                if op == "NOT":
                    num = num_stack.pop()
                    num_stack.append(logical_ops[op](num))
                else:
                    num2 = num_stack.pop()
                    num1 = num_stack.pop()
                    num_stack.append(logical_ops[op](num1, num2))

            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token in logical_ops:
                    if token == "NOT":
                        op_stack.append(token)
                    else:
                        while (
                            op_stack
                            and op_stack[-1] in logical_ops
                            and logical_ops[op_stack[-1]]
                            in [
                                logical_ops["AND"],
                                logical_ops["OR"],
                                logical_ops["XOR"],
                            ]
                        ):
                            apply_operator()
                        op_stack.append(token)
                else:
                    num_stack.append(int(token))
                i += 1

            while op_stack:
                apply_operator()

            return num_stack[0]

        result = process_tokens(tokens)

        # Convert the result back to binary and remove unnecessary padding
        return dec_to_bin(result)

    def abs_binary(self, binary_str):
        """
        Return the absolute value of a binary number given as a string.

        Parameters:
        binary_str (str): The binary string representing the number.

        Returns:
        str: The absolute value of the binary number in binary format.
        """

        def binary_to_decimal(binary_str):
            """Convert a binary string to a decimal float."""
            if "." in binary_str:
                int_part, frac_part = binary_str.split(".")
                int_value = int(int_part, 2)
                frac_value = sum(int(bit) * 2**-i for i, bit in enumerate(frac_part, 1))
                return int_value + frac_value
            else:
                return int(binary_str, 2)

        def decimal_to_binary(decimal_num):
            """Convert a decimal number to a binary string."""
            if decimal_num == 0:
                return "0.0"

            int_part = int(decimal_num)
            frac_part = decimal_num - int_part

            int_bin = bin(int_part).lstrip("0b") + "."

            frac_bin = ""
            while frac_part:
                frac_part *= 2
                bit = int(frac_part)
                frac_part -= bit
                frac_bin += str(bit)
                if (
                    len(frac_bin) > 8
                ):  # limiting the length of the fractional part to 8 digits
                    break

            return int_bin + frac_bin if frac_bin else int_bin.rstrip(".")

        # Remove the negative sign if it exists
        if binary_str.startswith("-"):
            binary_str = binary_str[1:]

        # Convert binary string to decimal
        decimal_value = binary_to_decimal(binary_str)

        # Get the absolute value
        abs_value = abs(decimal_value)

        # Convert the absolute decimal value back to a binary string
        return decimal_to_binary(abs_value)

    def shift_binary_custom(self, direction, shift_amount_bin, number):
        """
        Shifts a binary number to the left or right by a specified amount given in binary.

        Parameters:
        direction (str): '<<' for left shift, '>>' for right shift.
        shift_amount_bin (str): The number of positions to shift as a binary string.
        number (str): The binary number to shift as a string.

        Returns:
        str: The shifted binary number as a string.
        """
        # Convert binary strings to integers
        shift_amount = int(shift_amount_bin, 2)
        number_int = int(number, 2)

        # Perform the shift operation
        if direction == "<<":
            shifted_number = number_int << shift_amount
        elif direction == ">>":
            shifted_number = number_int >> shift_amount
        else:
            raise ValueError(
                "Invalid direction. Use '<<' for left shift or '>>' for right shift."
            )

        # Convert the shifted number back to binary string
        shifted_binary = bin(shifted_number)[2:]  # Remove the '0b' prefix
        return shifted_binary

    def evaluate_hex_expression(self, expression):
        print("evaluate_hex_expression")
        # Regular expression to find hexadecimal numbers (e.g., A, FF)
        hex_pattern = re.compile(r"\b[0-9a-fA-F]+\b")

        # Function to convert hexadecimal to decimal
        def hex_to_dec(match):
            return str(int(match.group(), 16))

        # Replace all hexadecimal numbers in the expression with their decimal equivalents
        decimal_expression = hex_pattern.sub(hex_to_dec, expression)

        result = eval(decimal_expression)

        if isinstance(result, int):
            if result < 0:
                # Convert the positive value to hexadecimal and add a negative sign
                hex_result = "-" + hex(-result).upper()[2:]
            else:
                # Convert the integer result back to hexadecimal
                hex_result = hex(result).upper()[2:]
        elif isinstance(result, float):
            # Handle float result
            # Extract the integer and fractional parts
            integer_part = int(result)
            fractional_part = result - integer_part

            # Convert the integer part to hexadecimal
            hex_integer_part = hex(abs(integer_part)).upper()[2:]

            # Convert the fractional part to hexadecimal
            hex_fractional_part = []
            while fractional_part != 0:
                fractional_part *= 16
                hex_digit = int(fractional_part)
                hex_fractional_part.append(hex(hex_digit).upper()[2:])
                fractional_part -= hex_digit
                if (
                    len(hex_fractional_part) > 12
                ):  # Limit precision to avoid infinite loops
                    break
            hex_fractional_part = "".join(hex_fractional_part)

            # Combine both parts
            if hex_fractional_part:
                hex_result = f"{hex_integer_part}.{hex_fractional_part}"
            else:
                hex_result = f"{hex_integer_part}"

            if result < 0:
                hex_result = "-" + hex_result

        return hex_result

    def hexidecimal_to_hexidecimal_64bit_segments(self, hex_number):
        # Convert hex to integer
        number = int(hex_number, 16)

        # Handle negative numbers by calculating two's complement for 64 bits
        if number < 0:
            # Calculate two's complement for 64-bit numbers
            number = (1 << 64) + number

        # Special case for zero, with a single 16-bit segment
        if number == 0:
            return ["0" * 16]

        # Get binary representation without '0b' prefix
        binary_result = bin(number)[2:]

        # Pad with leading zeros to make it 64 bits
        binary_result = binary_result.zfill(64)

        # Split into 16-bit segments
        segments = [binary_result[i : i + 16] for i in range(0, 64, 16)]

        return segments

    def logical_ops(self, string):
        # Define allowed operators
        allowed_operators = {"XOR", "OR", "AND", "NOT", "^", "|", "&", "~", "(", ")"}

        # Tokenize the string
        tokens = re.findall(r"\b\w+\b|[&|^~()]+", string)

        # Validate tokens
        for token in tokens:
            if token.isdigit():  # Check if the token is a digit (integer)
                continue
            elif (
                token in allowed_operators
            ):  # Check if the token is an allowed operator
                continue
            else:
                raise ValueError(f"Invalid token found: {token}")

        # Replace logical operators with corresponding symbols
        string = (
            string.replace("XOR", "^")
            .replace("OR", "|")
            .replace("AND", "&")
            .replace("NOT", "~")
        )
        return eval(string)

    def bin_to_dec(self, binary_str):
        return int(binary_str, 2)

    def oct_to_dec(self, octal_str):
        return int(octal_str, 8)

    def hex_to_dec(self, hex_str):
        return int(hex_str, 16)

    def dec_to_bin(self, decimal_float):
        integer_part = int(decimal_float)
        fractional_part = decimal_float - integer_part
        integer_str = bin(integer_part)[2:]

        fractional_str = ""
        while fractional_part > 0 and len(fractional_str) < 10:
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_str += str(bit)
            fractional_part -= bit

        return integer_str + ("." + fractional_str if fractional_str else "")

    def eval_expression(self, expression, mode):
        if mode == "binary":
            expression = re.sub(
                r"(\b[01]+)", lambda x: str(self.bin_to_dec(x.group(1))), expression
            )

        # Replace common operators for Python eval
        expression = expression.replace("×", "*").replace("÷", "/")

        # Evaluate the expression in decimal
        result = eval(expression)
        return result

    def sqrt_func(self, input_str, mode):
        input_str = input_str.strip().upper()

        # Handle the SQRT operation within the expression
        input_str = re.sub(
            r"SQRT\((.*?)\)",
            lambda m: str(math.sqrt(self.eval_expression(m.group(1), mode))),
            input_str,
        )
        input_str = re.sub(
            r"SQRT([0-9A-Fa-f]+)",
            lambda m: str(math.sqrt(self.eval_expression(m.group(1), mode))),
            input_str,
        )

        # Evaluate the final expression
        decimal_value = self.eval_expression(input_str, mode)

        if decimal_value.is_integer():
            decimal_value = int(decimal_value)

        # Convert back to the original mode
        if mode == "binary":
            result = self.dec_to_bin(decimal_value)
        elif mode == "decimal":
            result = decimal_value

        return result

    def update_operations_display(self):
        self.operations_list.clear()
        self.operations_list.addItems(self.operations)
        self.operations_list.scrollToBottom()

    def update_operations_display2(self):
        self.operations_list2.clear()
        self.operations_list2.addItems(self.operations2)
        self.operations_list2.scrollToBottom()

    def on_item_clicked(self, item):
        self.Result.setText("")
        item_text = item.text()
        self.Result.setText(item_text)  # Use the full item text directly

    def on_item_clicked2(self, item):
        self.Result.setText("")
        item_text = item.text()
        self.Result.setText(item_text)

    def keyPressEvent(self, event):
        key = event.key()

        # Handle Enter/Return key to evaluate the expression
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.evaluate_expression()
            self.enter_pressed = True  # Set flag to true after pressing Enter
            self.error_displayed = (
                "Helytelen" in self.Result.text()
            )  # Check if ERROR was displayed

        else:
            # If Enter was pressed before this key or if ERROR is displayed, clear label and start new input
            if self.enter_pressed or self.error_displayed:
                self.text = ""  # Clear the previous text
                self.Result.clear()
                self.enter_pressed = False  # Reset the flag
                self.error_displayed = False  # Reset the error flag

            # Convert the key to a character and append it to the QLineEdit
            if key == Qt.Key_Backspace:
                # Handle backspace
                self.Result.backspace()  # This handles backspace in QLineEdit
            else:
                # Add the pressed key text to QLineEdit
                self.Result.insert(event.text())


def main():
    App = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(App.exec())


############################################
if __name__ == "__main__":
    main()
