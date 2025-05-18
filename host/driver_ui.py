import sys
import json
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt, QRectF, QTimer
from host.driver_ui_form_widget import Ui_Form
from host.serial_reader import SerialReader
from mock.mock_data_source import MockSerial
from common.logger import setup_logger


class DriverUI(QMainWindow):
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080

    def __init__(self):
        super().__init__()

        # Load UI
        self.ui_widget = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.ui_widget)

        # Scalable scene
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.ui_widget)

        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.view.setSceneRect(QRectF(0, 0, self.BASE_WIDTH, self.BASE_HEIGHT))
        self.view.setAlignment(Qt.AlignCenter)

        self.resize(1280, 720)
        self.setMinimumSize(800, 450)

        # Serial reader using mock
        logger = setup_logger("driver_ui")
        mock_serial = MockSerial()
        self.reader = SerialReader(mock_class=lambda: mock_serial, logger=logger)

        # Timer for polling serial
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_serial)
        self.timer.start(100)

        self.scale_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scale_ui()

    def scale_ui(self):
        view_width = self.view.viewport().width()
        view_height = self.view.viewport().height()
        scale = min(view_width / self.BASE_WIDTH, view_height / self.BASE_HEIGHT)
        self.view.resetTransform()
        self.view.scale(scale, scale)

    def poll_serial(self):
        try:
            line = self.reader.read_line()
            if line:
                data = json.loads(line)
                self.update_ui(data)
        except Exception as e:
            print(f"[poll_serial error] {e}")

    def update_ui(self, data):
        self.ui.speed_value.setText(f"{data.get('speed', 0)} km/h")
        self.ui.voltage_value.setText(f"{data.get('voltage', 0):.2f} V")
        self.ui.laps_value.setText(f"Laps: {data.get('laps', 0)}")

        elapsed = int(data.get('time', 0))
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.ui.time_value.setText(f"{minutes:02}:{seconds:02}")

        self.ui.PWM_bar.setValue(data.get('pwm', 0))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DriverUI()
    window.setWindowTitle("Driver UI")
    window.show()
    sys.exit(app.exec())
