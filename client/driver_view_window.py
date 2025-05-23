import sys
import json
import threading
import zmq
import platform
from qt_compat import get_qt_modules
QtWidgets, QtCore, QtGui, QApplication, QMainWindow, QGraphicsScene, QGraphicsView, Qt, QRectF, QTimer = get_qt_modules()

if platform.system() == "Windows":
    from host.driver_ui_form_widget_windows import Ui_Form
else:
    from host.driver_ui_form_widget import Ui_Form


class DriverViewWindow(QMainWindow):
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pit Crew - Driver View")
        self.resize(1280, 720)
        self.setMinimumSize(800, 450)

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)

        threading.Thread(target=self.start_zmq_listener, daemon=True).start()

        self.latest_data = {}
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

    def start_zmq_listener(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://100.92.87.111:5555")  # Replace with Tailscale IP if needed
        socket.setsockopt_string(zmq.SUBSCRIBE, "")

        while True:
            try:
                msg = socket.recv_json()
                self.latest_data = msg
            except Exception as e:
                print(f"[ZMQ listener error] {e}")

    def update_ui(self):
        data = self.latest_data
        if not data:
            return

        self.ui.speed_value.setText(f"{data.get('speed', 0)} km/h")
        self.ui.voltage_value.setText(f"{data.get('voltage', 0):.2f} V")
        self.ui.laps_value.setText(f"Laps: {data.get('laps', 0)}")

        elapsed = int(data.get('time', 0))
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.ui.time_value.setText(f"{minutes:02}:{seconds:02}")

        self.ui.PWM_bar.setValue(data.get('pwm', 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DriverViewWindow()
    window.show()
    sys.exit(app.exec())
