import sys
import zmq
import json
import threading
from collections import deque
from PySide6 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import math

class SpeedGaugeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speed = 0
        self.setMinimumSize(200, 200)

    def setSpeed(self, value):
        self.speed = max(0, min(value, 100))  # Clamp between 0–100
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect().adjusted(10, 10, -10, -10)

        # Draw background
        painter.setBrush(QtGui.QColor("#111"))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(rect)

        # Draw ticks
        painter.setPen(QtGui.QColor("#555"))
        for i in range(0, 101, 10):
            angle = 225 - (i * 270 / 100)
            rad = math.radians(angle)
            x = rect.center().x() + math.cos(rad) * rect.width() / 2 * 0.85
            y = rect.center().y() - math.sin(rad) * rect.height() / 2 * 0.85
            painter.drawText(QtCore.QPointF(x - 10, y + 5), str(i))

        # Draw needle
        angle = 225 - (self.speed * 270 / 100)
        rad = math.radians(angle)
        needle_length = rect.width() / 2 * 0.7
        x = rect.center().x() + math.cos(rad) * needle_length
        y = rect.center().y() - math.sin(rad) * needle_length

        painter.setPen(QtGui.QPen(QtGui.QColor("#0f0"), 4))
        painter.drawLine(rect.center(), QtCore.QPointF(x, y))


class TelemetryDashboardUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pit Crew Telemetry UI")
        self.resize(1600, 900)
        self.setStyleSheet("background-color: #121212; color: #eee;")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Left panel - raw values
        self.left_panel = QtWidgets.QVBoxLayout()
        self.labels = {}
        for key in ["Voltage", "Current", "PWM", "Throttle"]:
            lbl = QtWidgets.QLabel(f"{key}: --")
            lbl.setStyleSheet("font-size: 18px")
            self.left_panel.addWidget(lbl)
            self.labels[key] = lbl
        layout.addLayout(self.left_panel, 0, 0)

        # Center - graphs
        self.graphs_layout = QtWidgets.QVBoxLayout()
        self.graph_widgets = {}
        self.graph_data = {
            "Speed": deque(maxlen=200),
            "Voltage": deque(maxlen=200),
            "Current": deque(maxlen=200)
        }
        for key, color in [("Speed", "y"), ("Voltage", "g"), ("Current", "r")]:
            graph = pg.PlotWidget(title=key)
            graph.setBackground("#222")
            graph.plotItem.showGrid(x=True, y=True)
            curve = graph.plot(pen=color)
            self.graph_widgets[key] = curve
            self.graphs_layout.addWidget(graph)
        layout.addLayout(self.graphs_layout, 0, 1)

        # Right panel - static data
        self.right_panel = QtWidgets.QVBoxLayout()
        self.laps_label = QtWidgets.QLabel("Laps: 0")
        self.time_label = QtWidgets.QLabel("Time: 00:00")
        for w in [self.laps_label, self.time_label]:
            w.setStyleSheet("font-size: 18px")
            self.right_panel.addWidget(w)
        layout.addLayout(self.right_panel, 0, 2)

        # Bottom - warnings and speed gauge
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.warning_label = QtWidgets.QLabel("All systems normal")
        self.warning_label.setStyleSheet("font-size: 16px; color: lime;")
        self.bottom_layout.addWidget(self.warning_label)

        self.speed_gauge = SpeedGaugeWidget()
        self.bottom_layout.addWidget(self.speed_gauge)

        layout.addLayout(self.bottom_layout, 1, 0, 1, 3)
        self.setCentralWidget(central)

        # Start ZMQ listener
        self.latest_data = {}
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)
        threading.Thread(target=self.start_zmq_listener, daemon=True).start()

    def update_ui(self):
        if not self.latest_data:
            return

        # Update left labels
        for key in ["Voltage", "Current", "PWM", "Throttle"]:
            value = self.latest_data.get(key.lower(), "--")
            self.labels[key].setText(f"{key}: {value}")

        # Update graphs
        for key in ["Speed", "Voltage", "Current"]:
            value = self.latest_data.get(key.lower(), None)
            if value is not None:
                self.graph_data[key].append(value)
                self.graph_widgets[key].setData(list(self.graph_data[key]))

        # Update right panel
        self.laps_label.setText(f"Laps: {self.latest_data.get('laps', 0)}")
        t = int(self.latest_data.get("time", 0))
        self.time_label.setText(f"Time: {t // 60:02}:{t % 60:02}")

        # Speed gauge
        self.speed_gauge.setSpeed(int(self.latest_data.get("speed", 0)))

        # Warnings
        if self.latest_data.get("status") == "warning":
            self.warning_label.setText("Warning: Check vehicle status!")
            self.warning_label.setStyleSheet("font-size: 16px; color: orange;")
        else:
            self.warning_label.setText("All systems normal")
            self.warning_label.setStyleSheet("font-size: 16px; color: lime;")

    def start_zmq_listener(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5555")
        socket.setsockopt_string(zmq.SUBSCRIBE, "")

        while True:
            try:
                msg = socket.recv_json()
                self.latest_data = msg
            except Exception as e:
                print(f"[ZMQ error] {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TelemetryDashboardUI()
    window.show()
    sys.exit(app.exec())
