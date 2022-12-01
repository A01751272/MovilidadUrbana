# Movilidad Urbana

### Instituto Tecnológico y de Estudios Superiores de Monterrey (Campus CEM)
### Modelación de sistemas multiagentes con gráficas computacionales (TC2008B - Grupo 301)
### Equipo: 4

# Integrantes del equipo:
- Aleny Sofia Arévalo Magdaleno |  A01751272
- Luis Humberto Romero Pérez | A01752789
- Valeria Martínez Silva | A01752167
- Pablo González de la Parra | A01745096

# Manejo de archivos
## Backend (Python, MESA, Flask)
```
LogicaMultiagentes/
```
## Frontend (Unity)
```
SimulacionMultiagentes/
```

# Instrucciones de utilización
Existen dos archivos principales los cuales permiten la visualización de nuestra simulación.
## MESA
1. Visualización web
```
model_viz.py
```
Permite la visualización de la simulación el navegador web de preferencia. Al correr el archivo, el modelo y su funcionamiento se encuentra disponible en el siguiente url.
```
http://localhost:8521/
```
2. API
```
server.py
```
Permite el enlace entre MESA y Unity al actuar como un API que manda la información de los agentes, al igual que determina los pasos de esta. Al correr el archivo, se debe mostrar una respuesta de conexión exitosa en el siguiente url.
```
http://localhost:8585/
```

## Unity
Para observar la visualización final de nuestra simulación, abrir la carpeta de ```SimulacionMultiagentes```, y entrar a la escena de ```Simulacion```. Finalmente, correr el programa.
> Nota: Cabe recalcar que es requisito que el servidor mencionado previamente se encuentre activo al momento de comenzar la simulación en Unity.

# Guía de instalación, configuración y ejecución detallada
Para poder entender con más detalle el proceso de instalación y ejecución de nuestra simulación (o solución a la situación problema) de manera local, observar los siguientes dos videos.
* Instalación, configuración y ejecución de la simulación
```
https://youtu.be/qSi-w2LYf4c
```
* Funcionalidad y ejecución de simulación
```
https://youtu.be/vao5CNTz0x8
```
