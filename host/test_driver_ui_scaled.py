import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView
)
from PySide6.QtCore import Qt, QRectF
from host.driver_ui_form import Ui_MainWindow

class ScaledMainWindow(QMainWindow):
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080

    def __init__(self):
        super().__init__()

        # Create a real QMainWindow and apply the UI to it
        self.inner_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.inner_window)

        # Grab the fully set up central widget (the real content)
        content_widget = self.inner_window.centralWidget()

        # Create a scene and view to scale it
        self.scene = QGraphicsScene()
        self.scene.addWidget(content_widget)

        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        self.showFullScreen()

        self.scale_ui()

    def scale_ui(self):
        screen_rect = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()

        scale_x = screen_width / self.BASE_WIDTH
        scale_y = screen_height / self.BASE_HEIGHT
        scale = min(scale_x, scale_y)

        self.view.resetTransform()
        self.view.scale(scale, scale)

        self.view.setSceneRect(QRectF(0, 0, self.BASE_WIDTH, self.BASE_HEIGHT))
        self.view.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScaledMainWindow()
    window.show()
    sys.exit(app.exec())
