import sys
import json
import zmq
import platform
from collections import deque
from qt_compat import get_qt_modules
QtWidgets, QtCore, QtGui, QApplication, QMainWindow, Qt = get_qt_modules()
import pyqtgraph as pg

class TelemetryDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telemetry Dashboard")
        self.resize(1400, 800)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        self.left_panel = QtWidgets.QVBoxLayout()
        self.graph_area = QtWidgets.QVBoxLayout()
        self.right_panel = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.left_panel, 1)
        self.main_layout.addLayout(self.graph_area, 3)
        self.main_layout.addLayout(self.right_panel, 1)

        # Raw data display (left)
        self.value_labels = {}
        for label in ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "current", "temp1", "temp2", "temp3", "pwm", "rpm", "speed", "mode", "warning", "debug"]:
            l = QtWidgets.QLabel(f"{label}: ---")
            self.left_panel.addWidget(l)
            self.value_labels[label] = l

        # Right static values
        self.laps_label = QtWidgets.QLabel("Laps: ---")
        self.elapsed_label = QtWidgets.QLabel("Elapsed: 00:00")
        self.lap_time_label = QtWidgets.QLabel("Lap Time: 00:00")
        for w in [self.laps_label, self.elapsed_label, self.lap_time_label]:
            self.right_panel.addWidget(w)

        # Graphs
        self.graph_widgets = {}
        self.graph_data = {}
        self.max_points = 100
        for key in ["speed", "voltage", "current", "pwm"]:
            plot = pg.PlotWidget(title=key.capitalize())
            self.graph_widgets[key] = plot
            self.graph_data[key] = deque(maxlen=self.max_points)
            self.graph_area.addWidget(plot)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_graphs)
        self.timer.start(200)

        self.latest_data = {}
        self.setup_zmq()

    def setup_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:5555")  # Update with Pi's Tailscale IP if needed
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        self.zmq_timer = QtCore.QTimer()
        self.zmq_timer.timeout.connect(self.poll_zmq)
        self.zmq_timer.start(50)

    def poll_zmq(self):
        socks = dict(self.poller.poll(0))
        if self.socket in socks:
            try:
                msg = self.socket.recv_json(zmq.NOBLOCK)
                self.latest_data = msg
                self.update_values()
            except zmq.Again:
                pass

    def update_values(self):
        d = self.latest_data
        for key in self.value_labels:
            if key in d:
                self.value_labels[key].setText(f"{key}: {d[key]}")

        if "laps" in d:
            self.laps_label.setText(f"Laps: {d['laps']}")

        if "time" in d:
            minutes = int(d['time']) // 60
            seconds = int(d['time']) % 60
            self.elapsed_label.setText(f"Elapsed: {minutes:02}:{seconds:02}")

        if "lap_time" in d:
            minutes = int(d['lap_time']) // 60
            seconds = int(d['lap_time']) % 60
            self.lap_time_label.setText(f"Lap Time: {minutes:02}:{seconds:02}")

        # Append to graph buffers
        for key in ["speed", "voltage", "current", "pwm"]:
            if key in d:
                self.graph_data[key].append(d[key])

    def update_graphs(self):
        for key, plot in self.graph_widgets.items():
            data = list(self.graph_data[key])
            plot.clear()
            plot.plot(data, pen=pg.mkPen('c', width=2))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelemetryDashboard()
    window.show()
    sys.exit(app.exec())
