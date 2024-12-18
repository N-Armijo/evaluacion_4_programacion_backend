# evaluacion_4_programacion_backend
# Sistema de Organización de Eventos

Sistema web que permite gestionar eventos, categorías y participantes a través de una API REST desarrollada con Django REST Framework y una interfaz de usuario construida en Vue.js.
## Capturas del Sistema

### Estructura del Proyecto
![Estructura del Proyecto](/images/estructura_proyecto.png)
*Estructura del proyecto mostrando la organización de archivos y carpetas*

### Panel de Administración
![Login Panel](/images/admin_login.png)
*Panel de inicio de sesión del administrador*

![Panel de Administración](/images/admin_panel.png)
*Panel de administración de Django mostrando las opciones de gestión*

### API REST
![API Eventos](/images/api_eventos.png)
*Vista de la API mostrando la lista de eventos disponibles*

![API Categorías](/images/api_categorias.png)
*Vista de la API mostrando las categorías del sistema*

![API Participantes](/images/api_participantes.png)
*Vista de la API mostrando la lista de participantes registrados*



##Características

- Gestión completa de eventos (CRUD)
- Categorización de eventos
- Sistema de registro de participantes
- API RESTful con autenticación JWT
- Protección de datos sensibles (emails)
- Validaciones para evitar registros duplicados
- Interfaz administrativa Django
- Frontend en Vue.js (en desarrollo)

## Requisitos Previos

Asegúrate de tener instalados:
- **Python 3.12.x** o superior
- **Node.js** y **npm** (v16+ recomendado)
- **Virtualenv** para crear entornos virtuales


## Instalación

### Backend (Django)

1. Clonar el repositorio
```bash
git clone https://github.com/N-Armijo/evaluacion_4_programacion_backend.git
cd backend
```

2. Crear y activar entorno virtual
- En Windows:
     ```bash
     python -m venv entorno
     entorno\Scripts\activate
     ```
     En Windows PowerShell:
   ```powershell
     python -m venv env
   ```
    Activar permisos de ejecucion de scripts que viene desactivada por defecto. Cuidado con los parametros. En este caso el -Scope de ejecucion es solo proceso
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```
    Activar el entorno virtual:
   ```powershell
   ./env/Scripts/activate
   ```
  
   - En Linux/Mac:
     ```bash
     python -m venv entorno
     source entorno/bin/activate
     ```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Realizar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario
```bash
python manage.py createsuperuser
```

6. Iniciar servidor
```bash
python manage.py runserver
```
7. El backend estará disponible tipicamente en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Frontend (Vue.js)

#### Características del Frontend
- Interfaz de usuario intuitiva para gestión de eventos
- Sistema de autenticación para usuarios
- Visualización de eventos por categorías
- Registro de participantes en eventos
- Vista de participantes por evento

#### Funcionalidades Principales
1. **Gestión de Eventos**
   - Lista de eventos disponibles
   - Filtrado por categorías
   - Detalles de cada evento

2. **Sistema de Usuarios**
   - Registro de usuarios
   - Login/Logout
   - Perfil de usuario

3. **Participantes**
   - Registro en eventos
   - Lista de participantes
   - Estado de inscripciones

#### Tecnologías Utilizadas
- Vue.js 3
- Axios para peticiones HTTP
- Vue Router para navegación
- Vuex para gestión de estado

#### Instalación Frontend
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


## Modelos

### Categoria
```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
```

### Evento
```python
class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
```

### Participante
```python
class Participante(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
```

## API Endpoints

### Autenticación
- `POST /api/register/` - Registro de nuevos usuarios
- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Refrescar token JWT

### Eventos
- `GET /api/eventos/` - Listar eventos
- `POST /api/eventos/` - Crear evento
- `GET /api/eventos/{id}/` - Obtener evento específico
- `PUT /api/eventos/{id}/` - Actualizar evento
- `DELETE /api/eventos/{id}/` - Eliminar evento
- `GET /eventos-inscritos/` - Eventos del usuario actual

### Participantes
- `GET /api/participantes/` - Listar participantes
- `POST /api/participantes/` - Registrarse en evento
- `DELETE /api/participantes/{id}/` - Cancelar registro

### Categorías
- `GET /api/categorias/` - Listar categorías
- `POST /api/categorias/` - Crear categoría (admin)
- `PUT /api/categorias/{id}/` - Actualizar categoría (admin)
- `DELETE /api/categorias/{id}/` - Eliminar categoría (admin)

### Documentacion de la API

1. Accediendo a la siguiente ruta para mayor información de la API [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/).

## Características de Seguridad

- Autenticación JWT
- Protección de datos sensibles
- Validación de registros duplicados
- Permisos basados en roles
- Control de acceso para operaciones CRUD

## Ejemplos de Uso

### Obtener Token de Acceso
```bash
POST /api/token/
{
    "username": "usuario",
    "password": "contraseña"
}
```

### Crear Evento (Admin)
```bash
POST /api/eventos/
{
    "titulo": "Conferencia Tech 2024",
    "fecha": "2024-12-20",
    "hora": "15:00",
    "ubicacion": "Centro de Eventos",
    "descripcion": "Conferencia sobre nuevas tecnologías",
    "categoria": 1
}
```

### Registrarse en Evento
```bash
POST /api/participantes/
{
    "evento": 1
}
```

## Equipo de Desarrollo

- Norma Armijo - Backend 
- Camilo Zamora - Frontend 
- Ester Godoy - Documentation


