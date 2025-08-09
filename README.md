# Todo API - Django REST Framework

Una API REST completa para gestión de tareas construida con Django REST Framework, implementando el patrón Repository y autenticación JWT.

## 🚀 Características

- ✅ **Patrón Repository**: Implementación limpia usando interfaces y repositorios concretos
- 🔐 **Autenticación JWT**: Sistema completo de autenticación con tokens
- 📊 **CRUD Completo**: Operaciones completas para tareas y usuarios
- 🏗️ **Arquitectura Limpia**: Service layer con inyección de dependencias
- 🔍 **Validación Centralizada**: Manejo de errores y validaciones consistente
- 🎯 **API-Only**: Configuración optimizada para APIs sin componentes web

## 📋 Requisitos Previos

- Python 3.8+
- MySQL 5.7+ o 8.0+
- Git

## 🛠️ Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/christoper-codes/todo-list.git
cd todo-list
```

### 2. Crear Ambiente Virtual

```bash
python -m venv env
```

### 3. Activar Ambiente Virtual

**Windows (Terminal):**
```powershell
.\env\Scripts\activate
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# .env
DB_NAME=todo_db
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306

SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Crear Base de Datos

Crea una base de datos llamada `todo_db` en tu servidor MySQL:

```sql
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Cargar Datos Iniciales (Seed)

```bash
python run_seeder.py
```

### 9. Ejecutar el Servidor

```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000`

## 📚 Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Registrar nuevo usuario |
| POST | `/api/auth/login/` | Iniciar sesión |
| POST | `/api/auth/logout/` | Cerrar sesión |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/` | Listar todas las tareas |
| POST | `/api/tasks/` | Crear nueva tarea |
| PUT | `/api/tasks/{id}/` | Actualizar tarea completa |
| PATCH | `/api/tasks/{id}/` | Actualizar tarea parcial |
| DELETE | `/api/tasks/{id}/` | Eliminar tarea |


## 🔐 Autenticación

La API usa JWT (JSON Web Tokens) para autenticación. Para acceder a endpoints protegidos:

1. **Registrarse o iniciar sesión** para obtener tokens
2. **Incluir el token** en el header de autorización:

```http
Authorization: Bearer tu_access_token_aqui (access)
```

### Ejemplo de Registro

```json
POST /api/auth/register/
{
    "first_name": "Chris",
    "last_name": "Santos",
    "email": "chris@email.com",
    "password": "password123",
    "password_confirm": "password123"
}
```

### Ejemplo de Login

```json
POST /api/auth/login/
{
    "email": "chris@email.com",
    "password": "password123"
}
```

## 📝 Ejemplos de Uso

### Crear una Tarea

```json
POST /api/tasks/
Authorization: Bearer tu_access_token

{
    "title": "Completar documentación",
    "description": "Escribir README.md del proyecto",
    "status_id": 1,
    "user_id": 1
}
```

## 🏗️ Arquitectura del Proyecto

```
apps/
├── tasks/
│   ├── interfaces/      # contratos
│   ├── migrations/      # Migraciones de datos
│   ├── models/          # Modelos de datos
│   ├── repositories/    # repositorios acceso a datos
│   ├── services/        # Lógica de negocio
│   ├── serializers/     # Serialización de datos
│   ├── views/           # ViewSets de la API
│   └── seeders/         # Datos iniciales
│   └── urls.py          # URLs principales
├── users/
│   ├── interfaces/      # contratos
│   ├── migrations/      # Migraciones de datos
│   ├── models/          # Modelo de usuario personalizado
│   ├── repositories/    # Repositorio de autenticación
│   ├── services/        # Servicios de autenticación
│   ├── serializers/     # Serialización de datos
│   └── views/           # Vistas de auth
│   └── urls.py          # URLs principales
└── core/
    ├── settings.py      # Configuración principal
    └── middleware/      # Accesos
```

## 🧪 Testing con Postman

1. **Importar colección**: Puedes usar los endpoints documentados arriba
2. **Configurar ambiente**: Crear variables para `base_url` y `token`
3. **Flujo de prueba**:
   - Registrar usuario
   - Hacer login
   - Usar el token para crear/listar/actualizar tareas

## 🛠️ Tecnologías Utilizadas

- **Django REST Framework** - Framework para APIs REST
- **Django JWT** - Autenticación JWT
- **MySQL** - Base de datos
- **Python 3.10+** - Lenguaje de programación
