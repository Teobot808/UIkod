import sys
import json
import asyncio
import threading
import requests
import uuid
import time
import queue
from datetime import datetime
import os
import zmq
from qt_compat import get_qt_modules
QtWidgets, QtCore, QtGui, QApplication, QMainWindow, QGraphicsScene, QGraphicsView, Qt, QRectF, QTimer = get_qt_modules()


from host.driver_ui_form_widget import Ui_Form
from host.serial_reader import SerialReader
from mock.mock_data_source import MockSerial
from common.logger import setup_logger
from host.websocket_server import WebSocketServer
from common.config import autodetect_serial_port


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
        try:
             serial_port = autodetect_serial_port()
             logger.info(f"Using real serial port: {serial_port}")
             self.reader = SerialReader(port=serial_port, logger=logger)
        except Exception as e:
             logger.warning(f"No serial port found, using mock serial. ({e})")
             mock_serial = MockSerial()
             self.reader = SerialReader(mock_class=lambda: mock_serial, logger=logger)

        context = zmq.Context()
        self.zmq_socket = context.socket(zmq.PUB)
        self.zmq_socket.bind("tcp://*:5555")  # port 5555 for telemetry

        # Timer for polling serial
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_serial)
        self.timer.start(100)

        self.scale_ui()
        # Shared queue for WebSocket server

        self.broadcast_queue = asyncio.Queue()
        # Start WebSocket server in background thread

        threading.Thread(target=self.start_websocket_server, daemon=True).start()

        self.influx_url = "http://100.117.215.100:8086/write?db=telemetry"  # ← change IP
        self.run_id = str(uuid.uuid4())  # Unique ID per program run
        self.data_log_file = create_data_logger()

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

        # Compute battery voltage from V1 + V2
        v1 = data.get("V1", 0)
        v2 = data.get("V2", 0)
        total_voltage = v1 + v2
        self.ui.voltage_value.setText(f"{total_voltage:.2f} V")

        self.ui.laps_value.setText(f"Laps: {data.get('laps', 0)}")

        elapsed = int(data.get('time', 0))
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.ui.time_value.setText(f"{minutes:02}:{seconds:02}")

        self.ui.PWM_bar.setValue(data.get('pwm', 0))
        try:
            self.broadcast_queue.put_nowait(data)
        except Exception as e:
            print(f"[websocket queue error] {e}")
        try:
             self.zmq_socket.send_json(data)
        except Exception as e:
             print(f"[ZMQ send error] {e}")


            # Send to InfluxDB
        try:
            fields = []
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    fields.append(f"{key}={value}")
            if fields:
                line = f"telemetry,run_id={self.run_id} " + ",".join(fields)
                requests.post(self.influx_url, data=line.encode('utf-8'), timeout=1)
        except Exception as e:
            print(f"[InfluxDB error] {e}")

        try:
            timestamp = datetime.now().isoformat()
            logged_data = {"timestamp": timestamp, **data}
            json.dump(logged_data, self.data_log_file)
            self.data_log_file.write("\n")
            self.data_log_file.flush()
        except Exception as e:
            print(f"[data log error] {e}")


    def start_websocket_server(self):
        asyncio.run(self._websocket_task())

    async def _websocket_task(self):
        server = WebSocketServer(data_queue=self.broadcast_queue)
        await server.run_server()


def apply_dark_theme(app):
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #ffffff;
        }

        QFrame {
            background-color: #1e1e1e;
            border: 1px solid #444;
        }

        QLabel {
            color: #ffffff;
        }

        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            background-color: #222;
            text-align: center;
            color: white;
        }

        QProgressBar::chunk {
            background-color: #05B8CC;
            width: 20px;
        }
    """
    app.setStyleSheet(dark_stylesheet)

def create_data_logger(name="driver_ui_data"):
    os.makedirs("logs", exist_ok=True)
    index = 1
    while True:
        filename = f"logs/{name}_{index:03}.jsonl"
        if not os.path.exists(filename):
            break
        index += 1
    return open(filename, "w", encoding="utf-8")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_dark_theme(app)
    window = DriverUI()
    window.setWindowTitle("Driver UI")
    window.show()
    sys.exit(app.exec())
