from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton


class EntradaMatrizWidget(QWidget):
    def __init__(self, filas=3, columnas=3, padre=None):
        super().__init__(padre)
        self.filas = filas
        self.columnas = columnas
        self.disenio = QVBoxLayout(self)
        self.etiqueta = QLabel(f"Ingrese los valores de una matriz {filas}x{columnas}:")
        self.disenio.addWidget(self.etiqueta)
        self.tabla = QTableWidget(filas, columnas)
        self.disenio.addWidget(self.tabla)
        self.setLayout(self.disenio)
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_matriz)
        self.disenio.addWidget(self.boton_limpiar)

    def obtener_matriz(self):
        matriz = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                item = self.tabla.item(i, j)
                valor = item.text() if item else ''
                try:
                    fila.append(float(valor))
                except ValueError:
                    fila.append(0.0)
            matriz.append(fila)
        return matriz

    def establecer_matriz(self, matriz):
        for i, fila in enumerate(matriz):
            for j, valor in enumerate(fila):
                if i < self.filas and j < self.columnas:
                    self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))

    def limpiar_matriz(self):
        self.tabla.clearContents()
