import sys
import zmq
import json
import threading
import platform

from qt_compat import get_qt_modules
QtWidgets, QtCore, QtGui, QApplication, QMainWindow, QGraphicsScene, QGraphicsView, Qt, QRectF, QTimer = get_qt_modules()

if platform.system() == "Windows":
    from host.driver_ui_form_widget_windows import Ui_Form
else:
    from host.driver_ui_form_widget import Ui_Form

class DriverViewWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pit Crew - Driver View")
        self.resize(1280, 720)

        # Load UI from .ui-generated class
        self.ui = Ui_Form()
        self.central_widget = QtWidgets.QWidget()
        self.ui.setupUi(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # ZMQ setup
        self.latest_data = {}
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)
        threading.Thread(target=self.zmq_listener, daemon=True).start()

    def zmq_listener(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5555")
        socket.setsockopt_string(zmq.SUBSCRIBE, "")

        while True:
            try:
                msg = socket.recv_json()
                self.latest_data = msg
            except Exception as e:
                print(f"[ZMQ DriverView Error] {e}")

    def update_ui(self):
        data = self.latest_data
        if not data:
            return

        # Apply updates to the UI elements
        self.ui.speed_value.setText(f"{data.get('speed', 0)} km/h")
        self.ui.voltage_value.setText(f"{data.get('voltage', 0):.2f} V")
        self.ui.laps_value.setText(f"Laps: {data.get('laps', 0)}")
        elapsed = int(data.get("time", 0))
        self.ui.time_value.setText(f"{elapsed // 60:02}:{elapsed % 60:02}")
        self.ui.PWM_bar.setValue(data.get("pwm", 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DriverViewWindow()
    window.show()
    sys.exit(app.exec())
