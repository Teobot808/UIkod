import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from host.driver_ui_form import Ui_MainWindow  # Adjust if your form uses a different class name

class DriverUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # This is the class from your .ui file
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.centralwidget)  # critical!

        # Make central widget expand fully
        self.ui.centralwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Optional: remove fixed size constraints
        self.ui.centralwidget.setMinimumSize(0, 0)
        self.ui.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))

        # If your main container inside centralwidget is a frame, also expand it:
        self.ui.centralwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Show maximized/fullscreen
        self.showFullScreen()


        # Example: Set initial values
        self.ui.speed_value.setText("0 km/h")
        self.ui.voltage_value.setText("12.6 V")
        self.ui.laps_value.setText("Laps: 0")
        self.ui.time_value.setText("00:00")
        self.ui.PWM_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DriverUI()
    window.show()
    sys.exit(app.exec())
