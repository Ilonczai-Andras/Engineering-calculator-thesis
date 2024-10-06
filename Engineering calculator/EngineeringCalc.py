from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QComboBox,
    QToolBar,
    QStackedWidget,
)
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
import os
import sys
from GUI.CalculusWindow import Window as CalculusWindow  # Import CalculusWindow
from GUI.EqualityWindow import Window as EqualityWindow  # Import EqualityWindow
from GUI.MainWindow import Window as Mainwindow  # Import MainWindow
from GUI.DifferentialEquationWindow import (
    Window as DifferentialEquationWindow,  # Import DifferentialEquationWindow
)
from GUI.ProbabilityAndStatisticsWindow import (
    Window as ProbabilityAndStatisticsWindow,  # Import ProbabilityAndStatisticsWindow
)
from GUI.ProgrammerCalculatorWindow import Window as ProgrammerCalculatorWindow
from Helpers import ConfigHelper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Calculator")
        self.setMinimumSize(800, 600)

        # Load saved mode from config
        self.current_mode = (
            ConfigHelper.load_mode() or "Basic"
        )  # Default to "Basic" if no mode is saved

        # ToolBar létrehozása
        self.toolBar = QToolBar("Navigation Toolbar")
        self.toolBar.setMovable(False)
        self.toolBar.setStyleSheet(
            "        QToolBar {\n"
            "            background-color: #3E3E3E;\n"
            "            border: none;\n"
            "            font-family: 'Courier New', Courier, monospace;\n"
            "        }"
        )
        self.addToolBar(self.toolBar)

        # Combo box hozzáadása a ToolBar-hoz
        font = QFont()
        font.setPointSize(12)
        self.combo = QComboBox()
        self.combo.setFont(font)
        self.combo.setStyleSheet(
            "QComboBox {\n"
            "background-color: #4E4E4E;\n"
            "font-family: 'Courier New', Courier, monospace;\n"
            "color: #FFFFFF;\n"
            "border: 1px solid #555555;\n"
            "border-radius: 5px;\n"
            "padding: 5px;\n"
            "}"
            "QComboBox QAbstractItemView {\n"
            "background-color: #4E4E4E;\n"
            "selection-background-color: #5E5E5E;\n"
            "color: #FFFFFF;\n"
            "font-family: 'Courier New', Courier, monospace;\n"
            "}\n"
        )
        self.combo.addItems(
            [
                "Basic",
                "Calculus",
                "Equality",
                "Differential Equations",
                "Probability and Statistics",
                "Programmer Calculator",
            ]
        )
        # Set the combo box to the saved mode
        saved_index = self.combo.findText(self.current_mode)
        if saved_index != -1:
            self.combo.setCurrentIndex(saved_index)

        self.toolBar.addWidget(self.combo)

        # QStackedWidget létrehozása
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Oldalak hozzáadása a StackedWidget-hez
        self.main_page = Mainwindow()  # A main page where you can add custom content
        self.calculus_page = (
            CalculusWindow()
        )  # A Calculus ablak helyettesítése a másik ablak osztályával
        self.equality_page = (
            EqualityWindow()
        )  # Az Equality ablak helyettesítése a másik ablak osztályával
        self.differential_equations_page = DifferentialEquationWindow()
        self.probability_and_statistics_page = ProbabilityAndStatisticsWindow()
        self.programmer_calculator = ProgrammerCalculatorWindow()

        # Add pages to QStackedWidget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.calculus_page)
        self.stacked_widget.addWidget(self.equality_page)
        self.stacked_widget.addWidget(self.differential_equations_page)
        self.stacked_widget.addWidget(self.probability_and_statistics_page)
        self.stacked_widget.addWidget(self.programmer_calculator)

        # Combo box változtatásának kezelése
        self.combo.currentIndexChanged.connect(self.change_page)

        # Állítsuk be kezdeti nézetet
        self.change_page(saved_index)

    def change_page(self, index):
        """Change the page displayed in the stacked widget based on combobox selection."""
        self.stacked_widget.setCurrentIndex(index)
        current_widget = self.stacked_widget.currentWidget()

        # Save the selected mode in the config file
        selected_mode = self.combo.currentText()
        ConfigHelper.update_mode(selected_mode)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowIcon(
        QIcon(os.path.join(os.path.dirname(__file__), "icon.ico"))
    )  # Ensure this path is correct
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
