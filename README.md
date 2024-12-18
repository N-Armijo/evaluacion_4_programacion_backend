# evaluacion_4_programacion_backend

## Documentación del Proyecto: Sistema de Gestión de Eventos

## Objetivo del Proyecto
El objetivo de este proyecto es desarrollar un sistema de gestión de eventos con funcionalidades para administrar **participantes**, **eventos** y **usuarios**. La aplicación cuenta con un backend desarrollado en **Django Rest Framework** (DRF) y un frontend en **Vue.js**.

---

## Estructura del Proyecto
```
.
|-- backend/            # Backend (API REST con Django)
|   |-- entorno/        # Entorno virtual
|   |-- mi_api/         # Proyecto Django
|   |-- api/            # Aplicación principal
|   |-- db.sqlite3      # Base de datos SQLite
|   `-- manage.py       # Comando principal de Django
|
|-- frontend/           # Frontend (Vue.js con Vite)
|   |-- eva4/           # Proyecto Vue.js
|   |-- node_modules/   # Dependencias de Node.js
|   |-- public/         # Archivos públicos
|   |-- src/            # Código fuente de Vue.js
|   |-- package.json    # Configuración de dependencias
|   `-- vite.config.js  # Configuración de Vite
|
`-- README.md           # Documentación del proyecto
```

---

## Configuración y Ejecución del Proyecto

### 1. Requisitos previos
Asegúrate de tener instalados:
- **Python 3.12.x** o superior
- **Node.js** y **npm** (v16+ recomendado)
- **Virtualenv** para crear entornos virtuales

### 2. Configuración del Backend
1. Accede a la carpeta **backend**:
   ```bash
   cd backend
   ```
2. Crea y activa el entorno virtual:
   - En Windows:
     ```bash
     python -m venv entorno
     entorno\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
     python -m venv entorno
     source entorno/bin/activate
     ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Realiza las migraciones y crea la base de datos:
   ```bash
   python manage.py migrate
   ```
5. Crea un superusuario para acceder al panel de administración:
   ```bash
   python manage.py createsuperuser
   ```
6. Ejecuta el servidor local de Django:
   ```bash
   python manage.py runserver
   ```
   El backend estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 3. Configuración del Frontend
1. Accede a la carpeta **frontend/eva4**:
   ```bash
   cd frontend/eva4
   ```
2. Instala las dependencias del proyecto Vue.js:
   ```bash
   npm install
   ```
3. Ejecuta el servidor local de desarrollo:
   ```bash
   npm run dev
   ```
   El frontend estará disponible en: [http://localhost:5173](http://localhost:5173).

### 4. Probar el Proyecto
1. Accede a la URL del frontend: [http://localhost:5173](http://localhost:5173).
2. Desde el frontend, puedes interactuar con la API del backend configurada en [http://127.0.0.1:8000](http://127.0.0.1:8000).
3. Usa las siguientes funcionalidades:
   - Administrar **participantes** (crear, actualizar, listar y eliminar).
   - Administrar **eventos** y filtrar por categoría.
   - Gestionar **usuarios** registrados.

---

## Descripción de Modelos y Endpoints

### Modelos Principales
1. **Evento**: Representa un evento registrado en el sistema.
   - Campos: `id`, `titulo`, `descripcion`, `fecha`, `categoria`.
2. **Participante**: Representa a una persona inscrita en un evento.
   - Campos: `id`, `nombre`, `correo`, `evento` (relación con el modelo Evento).
3. **Usuario**: Usuarios registrados con permisos de acceso.

### Endpoints de la API
| Método | URL                       | Descripción                       |
|---------|---------------------------|-----------------------------------|
| GET     | `/api/eventos/`           | Listar eventos                   |
| POST    | `/api/eventos/`           | Crear un nuevo evento            |
| GET     | `/api/participantes/`     | Listar participantes             |
| POST    | `/api/participantes/`     | Crear un participante            |
| PUT     | `/api/participantes/{id}/`| Actualizar un participante       |
| DELETE  | `/api/participantes/{id}/`| Eliminar un participante         |
| POST    | `/api/register/`          | Registrar un nuevo usuario       |
| POST    | `/api/token/`             | Obtener un token JWT             |
| POST    | `/api/token/refresh/`     | Refrescar un token JWT           |

### Ejemplos de Uso de la API

#### Obtener un Token JWT
**Solicitud**:
```http
POST /api/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña"
}
```
**Respuesta**:
```json
{
  "access": "<TOKEN_DE_ACCESO>",
  "refresh": "<TOKEN_DE_REFRESH>"
}
```

#### Crear un Participante
**Solicitud**:
```http
POST /api/participantes/
Authorization: Bearer <TOKEN_DE_ACCESO>
Content-Type: application/json

{
  "nombre": "Juan Perez",
  "correo": "juanperez@example.com",
  "evento": 1
}
```
**Respuesta**:
```json
{
  "id": 1,
  "nombre": "Juan Perez",
  "correo": "juanperez@example.com",
  "evento": 1
}
```

---

## Herramientas y Tecnologías
- **Backend**: Python, Django Rest Framework (DRF), JWT para autenticación.
- **Frontend**: Vue.js 3 con Vite, Bootstrap 5.
- **Base de datos**: SQLite (entorno de desarrollo).
- **Servidor local**: Django Development Server y Vite Dev Server.

---

## Autores
- **Nombre del autor**: Camilo Zamora - Ester Godoy - Norma Armijo

---

#

