import sys
import zmq
import json
import threading
from collections import deque
from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg


class TelemetryUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telemetry Subscriber - ZMQ")
        self.resize(1000, 600)

        self.plot_speed = pg.PlotWidget(title="Speed (km/h)")
        self.plot_speed.setYRange(0, 100)
        self.speed_curve = self.plot_speed.plot(pen='y')

        self.plot_voltage = pg.PlotWidget(title="Voltage (V)")
        self.plot_voltage.setYRange(10, 14)
        self.voltage_curve = self.plot_voltage.plot(pen='g')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plot_speed)
        layout.addWidget(self.plot_voltage)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.speed_data = deque(maxlen=200)
        self.voltage_data = deque(maxlen=200)
        self.latest_data = {}

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_graphs)
        self.timer.start(50)

        # Start ZMQ listener in background
        threading.Thread(target=self.start_zmq_listener, daemon=True).start()

    def update_graphs(self):
        if self.latest_data:
            self.speed_data.append(self.latest_data.get("speed", 0))
            self.voltage_data.append(self.latest_data.get("voltage", 0))

            self.speed_curve.setData(list(self.speed_data))
            self.voltage_curve.setData(list(self.voltage_data))

    def start_zmq_listener(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5555")  # Change IP if needed
        socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics

        while True:
            try:
                message = socket.recv_json()
                self.latest_data = message
            except Exception as e:
                print(f"[ZMQ receive error] {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TelemetryUI()
    window.show()
    sys.exit(app.exec())
