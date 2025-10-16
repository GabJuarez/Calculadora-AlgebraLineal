from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QSpinBox, \
    QMessageBox


class EntradaMatrizWidget(QWidget):
    def __init__(self, padre=None):
        super().__init__(padre)
        #creando el layout para poder aniadir los widgets a la ventana
        self.disenio = QVBoxLayout(self)

        #creando los spinbox para seleccionar el numero de filas y
        # columnas que corresponden al tamanio de la matriz
        self.spinbox_filas = QSpinBox(self, minimum=1, maximum=10, value=3)
        self.spinbox_columnas = QSpinBox(self, minimum=1, maximum=10, value =3)
        self.disenio.addWidget(QLabel("Número de filas:"))
        self.disenio.addWidget(self.spinbox_filas)
        self.disenio.addWidget(QLabel("Número de columnas:"))
        self.disenio.addWidget(self.spinbox_columnas)
        self.spinbox_columnas.valueChanged.connect(lambda _: self.actualizar_tabla())
        self.spinbox_filas.valueChanged.connect(lambda _: self.actualizar_tabla())
        self.filas = self.spinbox_filas.value()
        self.columnas = self.spinbox_columnas.value()

        # creando la tabla para ingresar los valores de la matriz
        self.etiqueta = QLabel(f"Ingrese los valores de una matriz {self.filas}x{self.columnas}:")
        self.disenio.addWidget(self.etiqueta)
        self.tabla = QTableWidget(self.filas, self.columnas)
        # ocultando los encabezados de la tabla
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setVisible(False)
        self.disenio.addWidget(self.tabla)
        self.setLayout(self.disenio)

        # creando el boton para limpiar la matriz
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
                    QMessageBox.critical(self, "Error", f"Valor inválido en la posición ({i+1}, {j+1}): '{valor}' ")
                    return []
            matriz.append(fila)
        return matriz

    def establecer_matriz(self, matriz):
        for i, fila in enumerate(matriz):
            for j, valor in enumerate(fila):
                if i < self.filas and j < self.columnas:
                    self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))

    def limpiar_matriz(self):
        self.tabla.clearContents()
        for i in range(self.filas):
            for j in range(self.columnas):
                self.tabla.setItem(i, j, QTableWidgetItem(""))

    def actualizar_tabla(self):
        self.filas = self.spinbox_filas.value()
        self.columnas = self.spinbox_columnas.value()
        self.tabla.setColumnCount(self.columnas)
        self.tabla.setRowCount(self.filas)
        self.etiqueta.setText(f"Ingrese los valores de una matriz {self.filas}x{self.columnas}:")