import sys

from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Algebra Lineal")
        self.setStyleSheet("background-color: black;")
        self.showMaximized()


# aplicacion y ventana principal
app = QApplication(sys.argv)
window = MainWindow()

# agregando titulo y distintos recursos a la ventana principal
fuente_titulo = QFont("Calibri", 45)
fuente_titulo.setBold(True)
titulo = QLabel("Calculadora de Álgebra Lineal", window)
titulo.setFont(fuente_titulo)
titulo.setStyleSheet("color: white;")

#imagen menu principal
imagen = QLabel()
pixmap = QPixmap("resources/images/logo.png")
imagen.setPixmap(pixmap)
imagen.setScaledContents(True)
imagen.setFixedSize(700, 400)

# descripcion
fuente_descripcion = QFont("Calibri", 20)
descripcion = QLabel("Resuelve problemas de álgebra lineal paso a paso, operaciones con matrices, \n"
                     "resolución de sistemas de ecuaciones, vectores, etc.", window)
descripcion.setFont(fuente_descripcion)
descripcion.setStyleSheet("color: white;")

# agregando widgets a la ventana principal
central_widget = QWidget()
layout = QVBoxLayout()
layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(imagen, alignment=Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(descripcion, alignment=Qt.AlignmentFlag.AlignHCenter)
central_widget.setLayout(layout)

#aniadiando el central widget despues de haber aniadido las etiquetas al layout
window.setCentralWidget(central_widget)

# mostrando la ventana y ejecutando la aplicacion
window.show()
sys.exit(app.exec())


