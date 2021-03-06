from os import environ

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from matplotlib.backend_bases import MouseButton

from InputLogs.mvc.Controller.plot_controller import PlotTrendController
from InputLogs.mvc.Model.log_curves import Log
from res.strings import main_icon


class TrendView(QMainWindow):
    def __init__(self, log: Log):
        super(TrendView, self).__init__()
        uic.loadUi(environ['project'] + '/ui/trend_window.ui', self)

        self.setWindowIcon(QIcon(main_icon()))

        self.log = log
        self.controller = PlotTrendController(self.draw_polygon_frame)
        self.controller.on_click_observer.append(self.on_click)
        self.controller.draw_trend(self.log)
        self.dispersionSpinBox.editingFinished.connect(self.change_dispersion)
        self.dispersionSpinBox.setValue(self.log.dispersion)

    def change_dispersion(self):
        self.log.dispersion = self.dispersionSpinBox.value()

    def on_click(self, x: float, y: float, button: MouseButton):
        if button == MouseButton.LEFT:
            self.log.add_trend_point((x, y))
        else:
            self.log.del_trend_point((x, y))
        self.controller.draw_trend(log=self.log)
