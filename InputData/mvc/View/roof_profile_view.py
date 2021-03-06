import os
from functools import partial

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QSpinBox, QShortcut

from InputData.mvc.Controller.edit_plot_modes import ModeStatus
from InputData.mvc.Controller.qt_matplotlib_connector import EditorRoofProfileController
from InputData.mvc.Model.lithological_model import LithologicalModel
from res.strings import main_icon, TitleName


class RoofProfileEditWindow(QMainWindow):
    def __init__(self, lithological_model: LithologicalModel):
        super(RoofProfileEditWindow, self).__init__()
        uic.loadUi(os.environ['project'] + '/ui/roof_profile_edit.ui', self)

        self.setWindowTitle(TitleName.RoofProfileEditWindow)
        self.setWindowIcon(QIcon(main_icon()))

        self.lithological_model = lithological_model
        self.editor = EditorRoofProfileController(lithological_model=lithological_model,
                                                  parent=self.draw_polygon_frame)

        self.handlers()
        self.set_default_value()
        self.editor.update_plot()
        self.addDot.click()

    def handlers(self):
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.chooseDot.clicked.connect(lambda: self.change_mode(ModeStatus.ChooseDot))
        self.interpolateMethodComboBox.currentTextChanged.connect(self.method_change)
        self.threeDButton.clicked.connect(self.editor.plot.show3d)
        self.heightSpinBox.editingFinished.connect(self.change_height)

        self.llCornerSpinBox.editingFinished.connect(
            partial(self.change_high_corner_point, 'll', self.llCornerSpinBox))
        self.ulCornerSpinBox.editingFinished.connect(
            partial(self.change_high_corner_point, 'ul', self.ulCornerSpinBox))
        self.lrCornerSpinBox.editingFinished.connect(
            partial(self.change_high_corner_point, 'lr', self.lrCornerSpinBox))
        self.urCornerSpinBox.editingFinished.connect(
            partial(self.change_high_corner_point, 'ur', self.urCornerSpinBox))

    def set_default_value(self):
        corners = self.lithological_model.roof_profile.values_corner_points
        self.llCornerSpinBox.setValue(corners['ll'])
        self.ulCornerSpinBox.setValue(corners['ul'])
        self.lrCornerSpinBox.setValue(corners['lr'])
        self.urCornerSpinBox.setValue(corners['ur'])

    def change_high_corner_point(self, corner: str, spinbox: QSpinBox):
        if self.lithological_model.roof_profile.values_corner_points.get(corner) is not None:
            self.lithological_model.roof_profile.values_corner_points[corner] = spinbox.value()
        self.editor.update_plot()

    def method_change(self):
        roof_profile = self.lithological_model.roof_profile
        roof_profile.interpolate_method = self.interpolateMethodComboBox.currentText()
        self.editor.update_plot()

    def change_height(self):
        if self.editor.plot.nearest_dot_index is None:
            return
        if len(self.lithological_model.roof_profile.points) > self.editor.plot.nearest_dot_index:
            self.lithological_model.roof_profile.points[self.editor.plot.nearest_dot_index].z \
                = self.heightSpinBox.value()
        self.editor.update_plot()

    def change_mode(self, mode: ModeStatus):
        self.modeNameLabel.setText(f": {str(mode).replace('ModeStatus.', '')}")
        self.editor.set_mode(mode)
        self.editor.update_plot()
