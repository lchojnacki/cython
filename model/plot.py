from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):

    __instance = None

    def __init__(self, parent=None, width=7, height=5, dpi=100):
        if type(self).__instance is None:
            fig = Figure(figsize=(width, height), dpi=dpi)
            self.ax = fig.add_subplot(111)
            self.ax.set_title("Time of function execution")
            self.ax.set_xlabel("Sample size")
            self.ax.set_ylabel("Time (s)")
            self.ax.grid(True)

            FigureCanvas.__init__(self, fig)
            self.setParent(parent)

            FigureCanvas.setSizePolicy(self,
                                       QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)

            self.plot()
            PlotCanvas.__instance = self
        else:
            self.get_instance()

    @staticmethod
    def get_instance():
        if PlotCanvas.__instance is not None:
            return PlotCanvas.__instance
        else:
            PlotCanvas.__instance = PlotCanvas()
            return PlotCanvas.__instance

    def plot(self):
        self.draw()

    def update_plot(self, x_data, y_data, ax_title):
        lines, names = self.ax.get_legend_handles_labels()
        if ax_title not in names:
            self.ax.plot(x_data, y_data, '-', label=ax_title)
            self.ax.plot(x_data, y_data, '.')
        else:
            pass
        self.ax.legend()
        self.plot()

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_title("Time of function execution")
        self.ax.set_xlabel("Sample size")
        self.ax.set_ylabel("Time (s)")
        self.ax.grid(True)
        self.plot()
