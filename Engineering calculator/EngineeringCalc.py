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
from GUI.CalculusWindow import Window as CalculusWindow
from GUI.EqualityWindow import Window as EqualityWindow
from GUI.MainWindow import Window as BasicWindow
from GUI.DifferentialEquationWindow import Window as DifferentialEquationWindow
from GUI.ProbabilityAndStatisticsWindow import Window as ProbabilityAndStatisticsWindow
from GUI.ProgrammerCalculatorWindow import Window as ProgrammerCalculatorWindow
from Helpers import ConfigHelper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Calculator")
        self.setMinimumSize(800, 600)

        self.current_mode = (
            ConfigHelper.load_mode() or "Basic"
        )

        self.toolBar = QToolBar("Navigation Toolbar")
        self.toolBar.setMovable(False)
        self.toolBar.setStyleSheet("""
            QToolBar {
                background-color: #3E3E3E;
                border: none;
                font-family: 'Courier New', Courier, monospace;
            }
        """)
        self.addToolBar(self.toolBar)

        font = QFont()
        font.setPointSize(12)
        self.combo = QComboBox()
        self.combo.setFont(font)
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #4E4E4E;
                font-family: 'Courier New', Courier, monospace;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #4E4E4E;
                selection-background-color: #5E5E5E;
                color: #FFFFFF;
                font-family: 'Courier New', Courier, monospace;
            }
        """)

        self.pages_config = {
            "Basic": BasicWindow,
            "Calculus": CalculusWindow,
            "Equality": EqualityWindow,
            "Differential Equations": DifferentialEquationWindow,
            "Probability and Statistics": ProbabilityAndStatisticsWindow,
            "Programmer Calculator": ProgrammerCalculatorWindow,
        }
        
        self.combo.addItems(list(self.pages_config.keys()))

        saved_index = self.combo.findText(self.current_mode)
        saved_index = saved_index if saved_index != -1 else 0
        self.combo.setCurrentIndex(saved_index)

        self.toolBar.addWidget(self.combo)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        for mode_name, WindowClass in self.pages_config.items():
            self.stacked_widget.addWidget(WindowClass())

        self.combo.currentIndexChanged.connect(self.change_page)

        self.change_page(saved_index)

    def change_page(self, index):
        """Change the page displayed in the stacked widget based on combobox selection."""
        self.stacked_widget.setCurrentIndex(index)

        selected_mode = self.combo.currentText()
        ConfigHelper.update_mode(selected_mode)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowIcon(
        QIcon(os.path.join(os.path.dirname(__file__), "icon.ico"))
    )
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
