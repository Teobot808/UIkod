import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from host.driver_ui_form import Ui_MainWindow  # Adjust path if needed

class MockDriverUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Timer to simulate data updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mock_data)
        self.timer.start(100)  # every 100 ms

        self.elapsed_seconds = 0
        self.laps = 0

    def update_mock_data(self):
        speed = random.randint(0, 80)
        voltage = round(random.uniform(11.5, 13.0), 2)
        pwm = random.randint(0, 100)

        # Simple lap counter based on time
        self.elapsed_seconds += 1
        if self.elapsed_seconds % 60 == 0:
            self.laps += 1

        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60

        # Update UI
        self.ui.speed_value.setText(f"{speed} km/h")
        self.ui.voltage_value.setText(f"{voltage:.2f} V")
        self.ui.laps_value.setText(f"Laps: {self.laps}")
        self.ui.time_value.setText(f"{minutes:02}:{seconds:02}")
        self.ui.PWM_bar.setValue(pwm)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MockDriverUI()
    window.showFullScreen()
    sys.exit(app.exec())
