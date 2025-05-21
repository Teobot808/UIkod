# client/websocket_client.py
import sys
import json
import asyncio
import websockets
import threading
from collections import deque
from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg


class PitCrewUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pit Crew UI - Live Telemetry")
        self.resize(1000, 600)

        self.plot_widget = pg.PlotWidget(title="Speed (km/h)")
        self.plot_widget.setYRange(0, 100)
        self.speed_curve = self.plot_widget.plot(pen='y')

        self.voltage_plot = pg.PlotWidget(title="Battery Voltage (V)")
        self.voltage_plot.setYRange(10, 14)
        self.voltage_curve = self.voltage_plot.plot(pen='g')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.voltage_plot)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.max_points = 200
        self.speed_data = deque(maxlen=self.max_points)
        self.voltage_data = deque(maxlen=self.max_points)
        self.latest_data = {}

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(100)

        # Start WebSocket in background
        threading.Thread(target=self.start_websocket, daemon=True).start()

    def update_plots(self):
        if self.latest_data:
            self.speed_data.append(self.latest_data.get("speed", 0))
            self.voltage_data.append(self.latest_data.get("voltage", 0))

            self.speed_curve.setData(list(self.speed_data))
            self.voltage_curve.setData(list(self.voltage_data))

    def start_websocket(self):
        asyncio.run(self.websocket_loop())

    async def websocket_loop(self):
        uri = "ws://localhost:8765"
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to server.")
                async for message in websocket:
                    data = json.loads(message)
                    self.latest_data = data
                    self.speed_data.append(data.get("speed", 0))
                    self.voltage_data.append(data.get("voltage", 0))

                    self.speed_curve.setData(list(self.speed_data))
                    self.voltage_curve.setData(list(self.voltage_data))
        except Exception as e:
            print(f"Connection failed: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PitCrewUI()
    window.show()
    sys.exit(app.exec())
