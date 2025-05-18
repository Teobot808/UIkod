import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt, QRectF
from host.driver_ui_form_widget import Ui_Form

class ScaledWidgetUI(QMainWindow):
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080

    def __init__(self):
        super().__init__()

        # Create and set up your designed QWidget
        self.ui_widget = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.ui_widget)

        # Put it into a QGraphicsScene
        self.scene = QGraphicsScene()
        self.proxy = self.scene.addWidget(self.ui_widget)

        # Wrap it with a QGraphicsView
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Set initial size and minimum
        self.resize(1280, 720)
        self.setMinimumSize(800, 450)

        # Set up scene rect to base size for scaling
        self.view.setSceneRect(QRectF(0, 0, self.BASE_WIDTH, self.BASE_HEIGHT))
        self.view.setAlignment(Qt.AlignCenter)

        # Trigger initial scaling
        self.scale_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scale_ui()

    def scale_ui(self):
        # Scale content proportionally to window size
        view_width = self.view.viewport().width()
        view_height = self.view.viewport().height()

        scale_x = view_width / self.BASE_WIDTH
        scale_y = view_height / self.BASE_HEIGHT
        scale = min(scale_x, scale_y)

        self.view.resetTransform()
        self.view.scale(scale, scale)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScaledWidgetUI()
    window.setWindowTitle("Driver UI - Scaled")
    window.show()
    sys.exit(app.exec())
