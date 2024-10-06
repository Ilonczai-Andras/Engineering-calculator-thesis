from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib as mpl
import re
import numpy as np
import math
import scipy.special as sp

mpl.rcParams["path.simplify_threshold"] = 1.0
mpl.rcParams["path.simplify"] = True
mpl.rcParams["agg.path.chunksize"] = 0
mplstyle.use("fast")


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.plotted_functions = []
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

        self.interval_x = [-10, 10]  # Initial x interval
        self.interval_y = [-10, 10]  # Initial y interval
        self.zoom_factor = 0.1  # Zoom factor
        self.df = False
        self.df_func = ""

        self.is_panning = False
        self.pan_start_x = None
        self.pan_start_y = None

    def f(self, x):
        return eval(self.text)

    def sec(self, x):
        return 1 / np.cos(x)

    def csc(self, x):
        return 1 / np.sin(x)

    def fact(self, x):
        if np.isscalar(x):
            return math.factorial(int(x))
        else:
            return np.array([math.factorial(int(i)) for i in x])

    def fresnelc(self, x):
        # Extracts the cosine integral from the Fresnel function
        return sp.fresnel(x)[1]

    def replace_numpy_funcs(self, func_str):
        replacements = {
            # log
            r"\blog\b": "np.log10",
            r"\bln\b": "np.log",
            # Inverse
            r"\barctan\b": "np.arctan",
            r"\barcsin\b": "np.arcsin",
            r"\barccos\b": "np.arccos",
            # Inverse hyperbolic
            r"\barcsinh\b": "np.arcsinh",
            r"\barccosh\b": "np.arccosh",
            r"\barctanh\b": "np.arctanh",
            # trig
            r"\bsin\b": "np.sin",
            r"\bcos\b": "np.cos",
            r"\btan\b": "np.tan",
            # hyperbolic
            r"\bsinh\b": "np.sinh",
            r"\bcosh\b": "np.cosh",
            r"\btanh\b": "np.tanh",
            # exp
            r"\bexp\(([^)]+)\)": r"np.exp(\1)",
            # abs
            r"\babs\b": "np.absolute",
            # sign(x)
            r"\bsign\b": "np.sign",
            # gyok
            r"\bsqrt\b": "np.sqrt",
            # szekánsok
            r"\bsec\b": "self.sec",
            r"\bcsc\b": "self.csc",
            r"\bpi\b": "np.pi",
            r"\be\b": "math.e",
            r"\bfactorial\b": "self.fact",
            r"\bgamma\b": "sp.gamma",
        }

        for pattern, replacement in replacements.items():
            func_str = re.sub(pattern, replacement, func_str)

        return func_str

    def check_for_large_jumps(self, y_vals, threshold):
        diff = np.abs(np.diff(y_vals))
        jumps = np.where(diff > threshold)[0]
        return jumps

    def clear(self, interval_x, interval_y):
        self.ax.clear()
        self.ax.set_xlim(interval_x[0], interval_x[1])
        self.ax.set_ylim(interval_y[0], interval_y[1])

    def plot_function(
        self,
        func_str,
        interval_x=None,
        interval_y=None,
        clear=True,
        C=None,
        df=False,
        df_func="",
        Color=None,
    ):
        if interval_x is None:
            print(interval_x)
            interval_x = self.interval_x
            x_vals = np.linspace(-100, 100, 100000)

        else:
            print(interval_x)
            x_vals = np.linspace(interval_x[0], interval_x[1], 100000)
        if interval_y is None:
            interval_y = self.interval_y

        self.interval_x = [interval_x[0], interval_x[1]]
        self.interval_y = [interval_y[0], interval_y[1]]

        self.func = func_str.replace("A", "a").replace("E", "e")
        func_str = (
            self.replace_numpy_funcs(func_str.replace("^", "**"))
            .replace("A", "a")
            .replace("E", "e")
            .replace("Si(x)", "np.sin(x)/x")
            .replace("fresnelc", "self.fresnelc")
        )
        print(func_str)
        self.text = func_str
        self.df = df
        self.df_func = df_func

        if C is not None:
            self.text = self.text.replace("C1", str(C[0]))
            self.text = self.text.replace("C2", str(C[1]))
            self.text = self.text.replace("C3", str(C[2]))

        if "fact" in func_str:
            x_vals = np.linspace(0, 15, 100)

        y_vals = 0

        if func_str.isdigit():
            y_vals = np.full_like(x_vals, int(func_str))
        else:
            y_vals = np.zeros_like(x_vals)
            for i, x in enumerate(x_vals):
                try:
                    y_vals[i] = self.f(x)
                except:
                    return False
        threshold = 10
        if "tan" in func_str or "sec" in func_str or "csc" in func_str:
            large_jumps = self.check_for_large_jumps(y_vals, threshold)
            for idx in large_jumps:
                y_vals[idx] = np.nan
            self.ax.set_ylim(interval_y[0], interval_y[1])
        else:
            pass

        if clear:
            self.ax.clear()

        color_to_use = Color if Color is not None else "black"

        self.ax.plot(x_vals, y_vals, color=color_to_use, label=f"y = {self.func}")
        self.ax.set_xlabel("x")
        self.ax.set_xlim(interval_x[0], interval_x[1])
        self.ax.set_ylim(interval_y[0], interval_y[1])
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True)
        self.ax.legend(loc="lower right")
        self.fig.canvas.draw()
        if df:
            self.direction_field(df_func, clear=False)

    def direction_field(self, func_str, clear=True):
        text = func_str.split("=")[1]
        func = func_str.split("=")[1]
        func = self.replace_numpy_funcs(func)

        nt, nv = 1, 1
        t = np.arange(-50, 50, nt)
        v = np.arange(-50, 50, nv)
        y, x = np.meshgrid(t, v)

        dv = eval(func)
        dt = np.ones(dv.shape)

        arrow_scale = 100  # Controls the length of the arrows
        arrow_width = 0.002  # Controls the thickness of the arrows

        if clear:
            self.ax.clear()

        self.ax.quiver(
            x,
            y,
            dt,
            dv,
            color="b",
            label=f"y'(t) = {text}",
            scale=arrow_scale,
            width=arrow_width,
        )
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_ylim(self.interval_y[0], self.interval_y[1])
        self.ax.set_xlim(self.interval_x[0], self.interval_x[1])
        self.ax.set_title("Íránymező " + text)
        self.ax.legend(loc="lower right")
        self.fig.canvas.draw()

    def store_function(
        self, func_str, interval_x, interval_y, C=None, df=False, df_func=""
    ):
        # Check if the function is already in the list
        for existing_func in self.plotted_functions:
            if existing_func[0] == func_str:
                print(f"Function {func_str} is already plotted.")
                return

        self.plotted_functions.append(
            (func_str, interval_x, interval_y, C, df, df_func)
        )

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:  # Scroll up
            self.interval_x = [
                self.interval_x[0] * (1 + self.zoom_factor),
                self.interval_x[1] * (1 + self.zoom_factor),
            ]
            self.interval_y = [
                self.interval_y[0] * (1 + self.zoom_factor),
                self.interval_y[1] * (1 + self.zoom_factor),
            ]
        else:  # Scroll down
            self.interval_x = [
                self.interval_x[0] / (1 + self.zoom_factor),
                self.interval_x[1] / (1 + self.zoom_factor),
            ]
            self.interval_y = [
                self.interval_y[0] / (1 + self.zoom_factor),
                self.interval_y[1] / (1 + self.zoom_factor),
            ]

        self.ax.set_xlim(self.interval_x)
        self.ax.set_ylim(self.interval_y)
        self.fig.canvas.draw_idle()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_panning = True
            self.pan_start_x = event.x()
            self.pan_start_y = event.y()

    def mouseMoveEvent(self, event):
        if self.is_panning:
            dx = (event.x() - self.pan_start_x) / self.width()
            dy = (event.y() - self.pan_start_y) / self.height()

            x_range = self.interval_x[1] - self.interval_x[0]
            y_range = self.interval_y[1] - self.interval_y[0]

            self.interval_x[0] -= dx * x_range
            self.interval_x[1] -= dx * x_range
            self.interval_y[0] += dy * y_range
            self.interval_y[1] += dy * y_range

            self.ax.set_xlim(self.interval_x)
            self.ax.set_ylim(self.interval_y)
            self.fig.canvas.draw_idle()

            self.pan_start_x = event.x()
            self.pan_start_y = event.y()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_panning = False

    def plot_area_between_functions(self, x_intervals):
        if len(self.plotted_functions) < 2:
            print("Not enough functions to plot the area between them.")
            return

        func1_str, interval_x1, interval_y1, _, _, _ = self.plotted_functions[0]
        func2_str, interval_x2, interval_y2, _, _, _ = self.plotted_functions[1]

        func1 = self.replace_numpy_funcs(func1_str.replace("^", "**")).replace("A", "a")
        func2 = self.replace_numpy_funcs(func2_str.replace("^", "**")).replace("A", "a")

        print(f"Plotting area with intervals: {x_intervals}")  # Debug statement

        # Ensure x_intervals has pairs of intervals
        if len(x_intervals) % 2 != 0:
            print(f"Invalid number of intervals: {x_intervals}")  # Debug statement
            return

        x_vals = np.linspace(-100, 100, 1000)
        y_vals_func1 = np.array([eval(func1) for x in x_vals])
        y_vals_func2 = np.array([eval(func2) for x in x_vals])

        for i in range(0, len(x_intervals), 2):
            start = x_intervals[i]
            end = x_intervals[i + 1]
            mask = (x_vals >= start) & (x_vals <= end)

            self.ax.fill_between(
                x_vals,
                y_vals_func1,
                y_vals_func2,
                where=mask,
                color="red",
                alpha=0.5,
                label=f"Terület az {func1_str} és a {func2_str} között.",
            )

        self.ax.legend(loc="lower right")
        self.fig.canvas.draw()
