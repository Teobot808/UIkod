import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt, QRectF
from host.driver_ui_form_widget import Ui_Form  # your new QWidget UI
from PySide6 import QtWidgets  # ✅ This is missing!


class ScaledWidgetUI(QMainWindow):
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080

    def __init__(self):
        super().__init__()

        # Step 1: Create the widget and apply UI
        self.ui_widget = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.ui_widget)

        # Step 2: Create the scene and view
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.ui_widget)

        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.showFullScreen()

        self.scale_ui()

    def scale_ui(self):
        screen_size = QApplication.primaryScreen().availableGeometry().size()
        scale_x = screen_size.width() / self.BASE_WIDTH
        scale_y = screen_size.height() / self.BASE_HEIGHT
        scale = min(scale_x, scale_y)

        self.view.resetTransform()
        self.view.scale(scale, scale)
        self.view.setSceneRect(QRectF(0, 0, self.BASE_WIDTH, self.BASE_HEIGHT))
        self.view.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScaledWidgetUI()
    window.show()
    sys.exit(app.exec())
