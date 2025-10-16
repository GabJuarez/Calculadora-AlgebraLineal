from app.gui.common_widgets import EntradaMatrizWidget
from app.operations import gauss_jordan, imprimir_resultados
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit, QMessageBox


class GaussJordanWindow(QDialog):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.setWindowTitle("Gauss-Jordan")
        self.layout = QVBoxLayout(self)
        self.entrada_matriz = EntradaMatrizWidget()
        self.layout.addWidget(self.entrada_matriz)
        self.boton_resolver = QPushButton("Resolver")
        self.boton_resolver.clicked.connect(self.resolver)
        self.layout.addWidget(self.boton_resolver)
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.layout.addWidget(self.resultado_texto)
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: white;")

    def resolver(self):
        matriz = self.entrada_matriz.obtener_matriz()
        if len(matriz) == 0:
            QMessageBox.critical(None, "Error", "Hubo un error al obtener los valores de la matriz")
            return
        try:
            n_vars = len(matriz[0]) - 1
            variables = [f"x{i+1}" for i in range(n_vars)]
            from app.operations.gauss_jordan import analizar_solucion
            matriz_transformada, pivotes, procedimiento = gauss_jordan(matriz)
            tipo, soluciones, libres = analizar_solucion(matriz_transformada, variables, pivotes)
            resultado = imprimir_resultados(tipo, soluciones, variables, libres, pivotes)
            texto_final = "\n".join(procedimiento) + "\n\n" + resultado
            self.resultado_texto.setText(texto_final)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al resolver: {e}")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = GaussJordanWindow()
    ventana.showMaximized()
    ventana.show()
    sys.exit(app.exec())
