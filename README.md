# AlgebraX

![AlgebraX](https://img.shields.io/badge/Python-AlgebraX-6EC6CA?style=for-the-badge&logo=python&logoColor=white)

---

**AlgebraX es una calculadora web interactiva con lógica desarrollada en python
para resolver y visualizar paso a paso los principales problemas de álgebra lineal
y análisis numérico**


---

## Funcionalidades principales

- Operaciones con matrices: suma, resta, multiplicación y escalares
- Cálculo de determinantes (Sarrus y triangularización)
- Obtención de la matriz inversa con pasos detallados
- Resolución de sistemas de ecuaciones lineales:
  - Gauss-Jordan
  - Eliminación Gaussiana
  - Regla de Cramer
- Verificación de independencia lineal de vectores
- Cálculo aproximado de raices de polinomios mediante el metodo de bisección
- Interfaz intuitiva y responsiva para una experiencia de usuario óptima

---

## Tecnologías utilizadas

<table>
  <tr>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40"/><br>Python</td>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="40"/><br>Flask</td>
    <td align="center"><img src="https://cdn.simpleicons.org/jinja/black" width="40"/><br>Jinja2</td>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="40"/><br>HTML5</td>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="40"/><br>CSS3</td>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="40"/><br>JavaScript</td>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/poetry/poetry-original.svg" width="40"/><br>Poetry</td>
  </tr>
</table>

- **Python**: Lógica y backend principal
- **Flask**: Framework web ligero
- **Jinja2**: Plantillas HTML dinámicas
- **HTML5/CSS3**: Estructura y estilos responsivos
- **JavaScript**: Interactividad en formularios y matrices
- **Poetry**: Gestión de dependencias y entorno virtual

---

## Instalación rápida

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/GabJuarez/Calculadora-AlgebraLineal.git
   cd Calculadora-AlgebraLineal
   ```

2. **Instala dependencias con Poetry:**

   ```bash
   poetry install
   poetry shell
   ```

3. **Ejecuta la aplicación:**

   ```bash
   python main.py
   ```

4. **Abre tu navegador:**

   [http://localhost:5000](http://localhost:5000)

---

## Estructura del proyecto

```text
AlgebraX/
├── app/
│   ├── logic/           # Lógica y operaciones matemáticas
│   ├── templates/       # Plantillas HTML (Jinja2)
│   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   ├── routes.py        # Rutas web principales
│   └── __init__.py      # Inicialización de Flask
├── main.py              # Punto de entrada
├── pyproject.toml       # Configuración de Poetry
└── README.md            # Información del proyecto
```

---

## Características visuales

- Interfaz moderna, minimalista y responsiva
- Paneles y menús laterales para navegación intuitiva
- Resultados y pasos resaltados con notación matemática clara
- Paleta de colores suave y agradable a la vista

---

