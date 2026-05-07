from PyQt5 import QtCore, QtGui, QtWidgets

# ── Shared style tokens ────────────────────────────────────────────────────────

BG_WINDOW   = "#141414"   # near-black window
BG_DISPLAY  = "#0D0D0D"   # display well
BG_FUNC     = "#1E1E1E"   # function buttons (DEL / % / C / operators)
BG_FUNC_H   = "#2C2C2C"   # function hover
BG_FUNC_P   = "#111111"   # function pressed
BG_NUM      = "#FF7A00"   # digit buttons  (orange)
BG_NUM_H    = "#FF9633"   # digit hover    (lighter orange)
BG_NUM_P    = "#CC6000"   # digit pressed  (darker orange)
BG_EQ       = "#E86500"   # equals
BG_EQ_H     = "#FF7A00"
BG_EQ_P     = "#B55000"
COLOR_TEXT  = "#F0F0F0"
COLOR_DIM   = "#A0A0A0"
BORDER_CLR  = "#2A2A2A"
RADIUS      = "12px"


def _btn_style(bg, hover, pressed, text_color=COLOR_TEXT, font_size=22):
    return f"""
        QPushButton {{
            background-color: {bg};
            color: {text_color};
            border: 1px solid {BORDER_CLR};
            border-radius: {RADIUS};
            font-family: 'Courier New', Courier, monospace;
            font-size: {font_size}px;
            font-weight: 600;
            padding: 8px;
        }}
        QPushButton:hover {{
            background-color: {hover};
            border: 1px solid #3A3A3A;
        }}
        QPushButton:pressed {{
            background-color: {pressed};
            border: 1px solid #111;
            padding-top: 10px;   /* subtle sink effect */
        }}
    """


STYLE_FUNC  = _btn_style(BG_FUNC,  BG_FUNC_H, BG_FUNC_P, COLOR_TEXT,  20)
STYLE_NUM   = _btn_style(BG_NUM,   BG_NUM_H,  BG_NUM_P,  "#FFFFFF",    24)
STYLE_EQ    = _btn_style(BG_EQ,    BG_EQ_H,   BG_EQ_P,   "#FFFFFF",    26)

STYLE_DISPLAY = f"""
    QLineEdit {{
        background-color: {BG_DISPLAY};
        color: {COLOR_TEXT};
        font-family: 'Courier New', Courier, monospace;
        font-size: 42px;
        font-weight: 300;
        border: 1px solid #222222;
        border-radius: 10px;
        padding: 12px 16px;
        selection-background-color: {BG_NUM};
    }}
"""

STYLE_WINDOW = f"""
    QMainWindow, QWidget {{
        background-color: {BG_WINDOW};
    }}
    QComboBox {{
        background-color: #1A1A1A;
        color: {COLOR_DIM};
        border: 1px solid #2A2A2A;
        border-radius: 6px;
        padding: 4px 10px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 13px;
    }}
    QComboBox::drop-down {{
        border: none;
    }}
"""

# ── UI class ───────────────────────────────────────────────────────────────────

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(530, 750)
        MainWindow.setMinimumSize(QtCore.QSize(340, 520))
        sp = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        MainWindow.setSizePolicy(sp)
        MainWindow.setStyleSheet(STYLE_WINDOW)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setSizePolicy(sp)
        self.centralwidget.setObjectName("centralwidget")

        # ── Root layout ────────────────────────────────────────────────────────
        root = QtWidgets.QVBoxLayout(self.centralwidget)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)
        root.setObjectName("verticalLayout_3")

        inner = QtWidgets.QVBoxLayout()
        inner.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        inner.setSpacing(6)
        inner.setObjectName("verticalLayout")

        # ── Display ────────────────────────────────────────────────────────────
        displayBox = QtWidgets.QVBoxLayout()
        displayBox.setObjectName("verticalLayout_2")

        self.outputLabel = QtWidgets.QLineEdit(self.centralwidget)
        self.outputLabel.setMinimumSize(QtCore.QSize(0, 90))
        self.outputLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.outputLabel.setStyleSheet(STYLE_DISPLAY)
        self.outputLabel.setObjectName("outputLabel")
        displayBox.addWidget(self.outputLabel)
        inner.addLayout(displayBox)

        # ── Helper: make an expanding button ──────────────────────────────────
        def btn(parent, name, style):
            b = QtWidgets.QPushButton(parent)
            b.setSizePolicy(sp)
            b.setMinimumHeight(60)
            font = QtGui.QFont("Courier New", 22)
            font.setWeight(QtGui.QFont.DemiBold)
            b.setFont(font)
            b.setStyleSheet(style)
            b.setObjectName(name)
            return b

        # ── Row 1 : DEL  %  C ─────────────────────────────────────────────────
        row1 = QtWidgets.QHBoxLayout()
        row1.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        row1.setObjectName("horizontalLayout_6")

        self.deleteButton     = btn(self.centralwidget, "deleteButton",     STYLE_FUNC)
        self.percentageButton = btn(self.centralwidget, "percentageButton", STYLE_FUNC)
        self.clearButton      = btn(self.centralwidget, "clearButton",      STYLE_FUNC)

        row1.addWidget(self.deleteButton)
        row1.addWidget(self.percentageButton)
        row1.addWidget(self.clearButton)
        inner.addLayout(row1)

        # ── Row 2 : x²  1/x  sqrt  / ─────────────────────────────────────────
        row2 = QtWidgets.QHBoxLayout()
        row2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        row2.setObjectName("horizontalLayout_5")

        self.quadratButton  = btn(self.centralwidget, "quadratButton",  STYLE_FUNC)
        self.onePerXButton  = btn(self.centralwidget, "onePerXButton",  STYLE_FUNC)
        self.sqrtButton     = btn(self.centralwidget, "sqrtButton",     STYLE_FUNC)
        self.divideButton   = btn(self.centralwidget, "divideButton",   STYLE_FUNC)

        row2.addWidget(self.quadratButton)
        row2.addWidget(self.onePerXButton)
        row2.addWidget(self.sqrtButton)
        row2.addWidget(self.divideButton)
        inner.addLayout(row2)

        # ── Row 3 : 7  8  9  * ────────────────────────────────────────────────
        row3 = QtWidgets.QHBoxLayout()
        row3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        row3.setObjectName("horizontalLayout_4")

        self.Button_7       = btn(self.centralwidget, "Button_7",       STYLE_NUM)
        self.Button_8       = btn(self.centralwidget, "Button_8",       STYLE_NUM)
        self.Button_9       = btn(self.centralwidget, "Button_9",       STYLE_NUM)
        self.multiplyButton = btn(self.centralwidget, "multiplyButton", STYLE_FUNC)

        row3.addWidget(self.Button_7)
        row3.addWidget(self.Button_8)
        row3.addWidget(self.Button_9)
        row3.addWidget(self.multiplyButton)
        inner.addLayout(row3)

        # ── Row 4 : 4  5  6  - ────────────────────────────────────────────────
        row4 = QtWidgets.QHBoxLayout()
        row4.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        row4.setObjectName("horizontalLayout_3")

        self.Button_4   = btn(self.centralwidget, "Button_4",   STYLE_NUM)
        self.Button_5   = btn(self.centralwidget, "Button_5",   STYLE_NUM)
        self.Button_6   = btn(self.centralwidget, "Button_6",   STYLE_NUM)
        self.minusButton = btn(self.centralwidget, "minusButton", STYLE_FUNC)

        row4.addWidget(self.Button_4)
        row4.addWidget(self.Button_5)
        row4.addWidget(self.Button_6)
        row4.addWidget(self.minusButton)
        inner.addLayout(row4)

        # ── Row 5 : 1  2  3  + ────────────────────────────────────────────────
        row5 = QtWidgets.QHBoxLayout()
        row5.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        row5.setObjectName("horizontalLayout_2")

        self.Button_1  = btn(self.centralwidget, "Button_1",  STYLE_NUM)
        self.Button_2  = btn(self.centralwidget, "Button_2",  STYLE_NUM)
        self.Button_3  = btn(self.centralwidget, "Button_3",  STYLE_NUM)
        self.plusButton = btn(self.centralwidget, "plusButton", STYLE_FUNC)

        row5.addWidget(self.Button_1)
        row5.addWidget(self.Button_2)
        row5.addWidget(self.Button_3)
        row5.addWidget(self.plusButton)
        inner.addLayout(row5)

        # ── Row 6 : +/-  0  .  = ──────────────────────────────────────────────
        row6 = QtWidgets.QHBoxLayout()
        row6.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        row6.setObjectName("horizontalLayout")

        self.plusMinusButton      = btn(self.centralwidget, "plusMinusButton",      STYLE_FUNC)
        self.zeroButton           = btn(self.centralwidget, "zeroButton",           STYLE_NUM)
        self.decimalPointButton   = btn(self.centralwidget, "decimalPointButton",   STYLE_FUNC)
        self.equalButton          = btn(self.centralwidget, "equalButton",          STYLE_EQ)

        row6.addWidget(self.plusMinusButton)
        row6.addWidget(self.zeroButton)
        row6.addWidget(self.decimalPointButton)
        row6.addWidget(self.equalButton)
        inner.addLayout(row6)

        root.addLayout(inner)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _t = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_t("MainWindow", "Engineering Calculator"))
        self.outputLabel.setText(_t("MainWindow", "0"))
        self.deleteButton.setText(_t("MainWindow", "DEL"))
        self.percentageButton.setText(_t("MainWindow", "%"))
        self.clearButton.setText(_t("MainWindow", "C"))
        self.quadratButton.setText(_t("MainWindow", "x²"))
        self.onePerXButton.setText(_t("MainWindow", "1/x"))
        self.sqrtButton.setText(_t("MainWindow", "√"))
        self.divideButton.setText(_t("MainWindow", "÷"))
        self.Button_7.setText(_t("MainWindow", "7"))
        self.Button_8.setText(_t("MainWindow", "8"))
        self.Button_9.setText(_t("MainWindow", "9"))
        self.multiplyButton.setText(_t("MainWindow", "×"))
        self.Button_4.setText(_t("MainWindow", "4"))
        self.Button_5.setText(_t("MainWindow", "5"))
        self.Button_6.setText(_t("MainWindow", "6"))
        self.minusButton.setText(_t("MainWindow", "−"))
        self.Button_1.setText(_t("MainWindow", "1"))
        self.Button_2.setText(_t("MainWindow", "2"))
        self.Button_3.setText(_t("MainWindow", "3"))
        self.plusButton.setText(_t("MainWindow", "+"))
        self.plusMinusButton.setText(_t("MainWindow", "+/−"))
        self.zeroButton.setText(_t("MainWindow", "0"))
        self.decimalPointButton.setText(_t("MainWindow", "."))
        self.equalButton.setText(_t("MainWindow", "="))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())