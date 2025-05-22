# qt_compat.py

try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QGraphicsScene, QGraphicsView
    )
    from PySide6.QtCore import Qt, QRectF, QTimer
except ImportError:
    from PyQt5 import QtWidgets, QtCore, QtGui
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QGraphicsScene, QGraphicsView
    )
    from PyQt5.QtCore import Qt, QRectF, QTimer

# Ensure everything is accessible directly from qt_compat
__all__ = [
    "QtWidgets", "QtCore", "QtGui",
    "QApplication", "QMainWindow", "QGraphicsScene", "QGraphicsView",
    "Qt", "QRectF", "QTimer"
]
