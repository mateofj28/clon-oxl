

---

## 🧭 **1. Crear un entorno virtual**

Desde tu terminal, navega hasta la carpeta raíz del proyecto y ejecuta:

```bash
python3 -m venv venv
```

Esto crea la carpeta `venv` que contendrá el entorno virtual.

---

## ⚡ **2. Activar el entorno virtual**

Según tu sistema operativo:

* **Linux/MacOS**:

  ```bash
  source venv/bin/activate
  ```
* **Windows (PowerShell)**:

  ```powershell
  venv\Scripts\Activate
  ```

Cuando esté activo, verás `(venv)` al inicio de tu terminal.

---

## 📦 **3. Instalar las dependencias necesarias**

Instalamos FastAPI, Uvicorn y demás paquetes que el proyecto necesita. Por ejemplo:

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic passlib[bcrypt] python-multipart pydantic-settings
```

*(Nota: Agregamos `pydantic-settings` para gestionar configuración, ya que Pydantic v2 movió las settings a ese paquete separado)*

---

## 📂 **4. Crear la estructura del proyecto**

La estructura típica que seguimos es algo así:

```
project/
├─ venv/
├─ app/
│  ├─ __init__.py
│  ├─ main.py           # Punto de entrada para Uvicorn
│  ├─ config.py         # Configuración con pydantic-settings
│  ├─ database.py       # Conexión a la base de datos
│  ├─ models.py         # Modelos SQLAlchemy
│  ├─ crud.py           # Operaciones de base de datos
│  ├─ schemas.py        # Pydantic (serialización)
│  ├─ routers/
│     ├─ __init__.py
│     ├─ users.py       # Rutas para usuarios
```

---

## 📝 **5. Llenar cada archivo con el código pertinente**

Ejemplos que vimos:

* **`main.py`**: Inicialización de FastAPI y conexión a routers.
* **`config.py`**: Usar `BaseSettings` para variables de entorno.
* **`database.py`**: Configuración de SQLAlchemy y `get_db()`.
* **`models.py`**: Declaración del modelo `User`.
* **`schemas.py`**: Esquemas Pydantic (`UserCreate`, `UserPublic`, etc.).
* **`crud.py`**: Funciones que acceden a la base de datos.
* **`routers/users.py`**: Rutas tipo `/users` (GET, POST, etc.).

---

## 🚀 **6. Encender el servidor**

Con todo listo, inicia Uvicorn apuntando a tu `main.py`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## 🧪 **7. Probar los endpoints en `/docs`**

Abre tu navegador en:

```
https://8080-firebase-clon-oxl-1750468974274.cluster-joak5ukfbnbyqspg4tewa33d24.cloudworkstations.dev/docs#/
```

Desde allí puedes probar automáticamente todos los endpoints que hayas definido (en `/users`, por ejemplo) gracias a la documentación automática que genera Swagger UI.

---

