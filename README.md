# Electric Tariffs App - README.md

## Descripción del proyecto ⚡️📘
Aplicación de escritorio para registrar lecturas eléctricas, calcular consumo y costo por tramos tarifarios y mantener un historial por usuario. Pensada para uso offline con almacenamiento local en SQLite, autenticación segura y un diseño modular compatible con PyQt (MVVM + Repository + Clean Architecture).

## Tecnología utilizada
- **Lenguaje**: Python 3.13.x  
- **Framework GUI**: PyQt (PyQt6 o PyQt5 según compatibilidad)  
- **Persistencia**: SQLite (módulo builtin sqlite3)  
- **Seguridad**: bcrypt para hashing de contraseñas  
- **Empaquetado opcional**: PyInstaller para generar ejecutables  
Emojis decorativos: ⚡️ 🔐 🧭

---

## Estructura principal del repositorio
Resumen rápido de carpetas clave:
- app/ o main.py — Punto de entrada y configuración de la app  
- presentation/ or ui/ — Vistas PyQt, ventanas y estilos QSS  
- domain/, application/, infrastructure/ — Capas de negocio, casos de uso y repositorios  
- data/ o database/ — Modelos y conexión SQLite  
- logs/ — archivos de auditoría CSV

---

## Requisitos previos
- Python 3.13.x instalado y accesible desde la línea de comandos  
- pip actualizado  
- Git (para clonar el repositorio)  
- En Windows o macOS: display/X server soportado (PyQt se abre en entorno gráfico)

---

## Pasos para obtener el proyecto y ejecutarlo localmente

#### 1. Clonar el repositorio
```bash
git clone https://github.com/carlosdanielclark/electric_tariffs_app.git
cd electric_tariffs_app
```

#### 2. Crear y activar entorno virtual
Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Windows (cmd):
```bash
python -m venv venv
.venv\Scripts\activate
```

#### 3. Instalar dependencias
Si el repositorio incluye `requirements.txt`:
```bash
pip install -r requirements.txt
```
Si no existe `requirements.txt`, instalar las dependencias mínimas recomendadas:
```bash
pip install pyqt6 bcrypt
```
Nota: si la app fue desarrollada con PyQt5 reemplazar `pyqt6` por `pyqt5`.

#### 4. Configurar base de datos inicial (si aplica)
Si el proyecto incluye scripts de migración o un archivo de inicialización, ejecutarlos:
```bash
# ejemplo genérico si existe script init_db.py
python scripts/init_db.py
```
Si no hay script, la primera ejecución de la aplicación debe crear las tablas automáticamente; si no, revisar `data/database` o `infrastructure/database` para instrucciones.

#### 5. Variables de configuración
Revisar `app/config/settings.py` o `config/settings.py` y ajustar valores clave como:
- ruta de la base de datos SQLite
- ruta de logs
- parámetros de seguridad y tiempo de sesión
Si no existen archivos, la app suele usar valores por defecto.

#### 6. Iniciar la aplicación localmente
Ejecutar el punto de entrada principal. Puede ser `main.py` en la raíz o `app/main.py`:
```bash
python main.py
# o si está dentro de la carpeta app
python app/main.py
```
La ventana de login debería aparecer. Crear un usuario administrador si se proporciona un comando o interfaz para ello, o comprobar si existe un usuario por defecto documentado.

---

## Instalación de dependencias detallada
- PyQt6 (o PyQt5) para la interfaz gráfica:
  ```bash
  pip install pyqt6
  ```
- bcrypt para hashing de contraseñas:
  ```bash
  pip install bcrypt
  ```
- Opcionales útiles:
  ```bash
  pip install pyinstaller   # para generar ejecutables
  pip install python-dotenv # si usa .env para configuraciones
  ```

---

## Cómo empaquetar la aplicación
Generar ejecutable con PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
El ejecutable resultante aparecerá en `dist/`. Ajustar parámetros de PyInstaller para incluir recursos (QSS, iconos, DB, logs).

---

## Notas y recomendaciones finales 🔐🧭
- Mantener copia de seguridad de la base de datos SQLite antes de pruebas destructivas.  
- Verificar compatibilidad PyQt5 vs PyQt6; instalar la que el proyecto requiera.  
- Revisar y ajustar rutas en `settings.py` para logs y base de datos si la app falla al iniciar.  
- Para desarrollo, habilitar logging detallado y lanzar la app desde terminal para ver errores.  

---
