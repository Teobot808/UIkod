# qt_compat.py

try:
    import PySide6
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QGraphicsScene, QGraphicsView
    )
    from PySide6.QtCore import Qt, QRectF, QTimer
    backend = "PySide6"
except ImportError:
    try:
        import PyQt5
        from PyQt5 import QtWidgets, QtCore, QtGui
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QGraphicsScene, QGraphicsView
        )
        from PyQt5.QtCore import Qt, QRectF, QTimer
        backend = "PyQt5"
    except ImportError:
        raise ImportError("Neither PySide6 nor PyQt5 is installed.")

# Optionally expose the selected backend for logging/debugging
__all__ = [
    "QtWidgets", "QtCore", "QtGui",
    "QApplication", "QMainWindow", "QGraphicsScene", "QGraphicsView",
    "Qt", "QRectF", "QTimer", "backend"
]
