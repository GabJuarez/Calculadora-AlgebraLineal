# Calculadora Álgebra Lineal

Calculadora web desarrollada con Flask para realizar operaciones fundamentales de álgebra lineal.

## Funcionalidades principales
- Operaciones con matrices (suma, resta, multiplicación)
- Cálculo de determinantes (incluye método de Sarrus)
- Obtención de la matriz inversa
- Resolución de sistemas de ecuaciones:
  - Método de Gauss-Jordan
  - Eliminación Gaussiana
  - Regla de Cramer
- Verificación de independencia lineal de vectores
- Próximamente: análisis numérico

## Instalación y uso

> **Nota:** Próximamente la calculadora estará disponible públicamente y accesible para todos en internet. Por ahora, puedes instalar y ejecutar el proyecto localmente siguiendo estos pasos:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/Calculadora-AlgebraLineal.git
   cd Calculadora-AlgebraLineal
   ```

2. **Instala las dependencias con Poetry:**
   ```bash
   poetry install
   poetry shell
   ```

3. **Inicia la aplicación Flask:**
   ```bash
   python main.py
   ```

4. **Accede a la calculadora:**
   Abre tu navegador y visita [http://localhost:5000](http://localhost:5000)

## Estructura del proyecto

```
Calculadora-AlgebraLineal/
├── app/
│   ├── logic/           # Lógica y operaciones matemáticas
│   ├── templates/       # Plantillas HTML
│   ├── static/          # Archivos estáticos (CSS, JS)
│   ├── routes.py        # Rutas web
│   └── __init__.py      # Inicialización de Flask
├── main.py              # Punto de entrada
├── pyproject.toml       # Configuración de Poetry
└── README.md            # Información del proyecto
```
---