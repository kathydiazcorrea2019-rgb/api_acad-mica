# API Académica

API REST para gestionar **cursos** y **estudiantes**, construida con FastAPI, SQLModel y SQLite. El proyecto sigue una arquitectura por responsabilidades (router, schema, service, model y base de datos) y guarda los datos de forma persistente en un archivo SQLite.

## Tecnologías

- Python 3.13.14
- FastAPI
- Uvicorn
- SQLModel
- Pydantic
- SQLite

## Funcionalidades implementadas

**Cursos (CRUD completo)**

- Crear un curso (`POST`).
- Listar todos los cursos y consultar uno por su ID (`GET`).
- Actualizar un curso por completo conservando su ID (`PUT`).
- Eliminar un curso (`DELETE`).

**Estudiantes**

- Crear un estudiante (`POST`), con `active` en `true` por defecto.
- Listar todos los estudiantes y consultar uno por su ID (`GET`).

**Aspectos generales**

- Validación de los datos de entrada con schemas de Pydantic.
- Códigos HTTP correctos: `200`, `201`, `404` y `422`.
- Persistencia en SQLite: los datos se conservan al reiniciar el servidor.
- Las tablas `course` y `student` conviven en el mismo archivo `database.db`.
- Documentación interactiva con Swagger en `/docs`.

## Cómo ejecutar el proyecto

### 1. Obtener el proyecto

```bash
git clone https://github.com/kathydiazcorrea2019-rgb/api_acad-mica.git
cd api_acad-mica
```

### 2. Crear y activar el entorno virtual

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea el script, ejecuta una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Iniciar el servidor

Desde la carpeta raíz del proyecto:

```bash
python -m uvicorn main:app --reload
```

### 5. Abrir la documentación

- Swagger UI: <http://127.0.0.1:8000/docs>

El archivo `database.db` se crea automáticamente la primera vez que se inicia la aplicación. Ejecuta siempre Uvicorn desde la carpeta raíz, porque la ruta de la base de datos es relativa.

## Endpoints disponibles

### Cursos

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| POST | `/courses` | Crear un curso | `201`, `422` |
| GET | `/courses` | Listar los cursos | `200` |
| GET | `/courses/{course_id}` | Consultar un curso por ID | `200`, `404`, `422` |
| PUT | `/courses/{course_id}` | Actualizar un curso por completo | `200`, `404`, `422` |
| DELETE | `/courses/{course_id}` | Eliminar un curso | `200`, `404`, `422` |

### Estudiantes

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| POST | `/students` | Crear un estudiante | `201`, `422` |
| GET | `/students` | Listar los estudiantes | `200` |
| GET | `/students/{student_id}` | Consultar un estudiante por ID | `200`, `404`, `422` |

## Reglas de validación

**Curso** (`POST` y `PUT`)

| Campo | Regla |
|---|---|
| `name` | Texto de 3 a 80 caracteres |
| `credits` | Entero entre 1 y 6 |
| `active` | Booleano. En `POST` es `true` por defecto; en `PUT` es obligatorio |

**Estudiante** (`POST`)

| Campo | Regla |
|---|---|
| `name` | Texto de 3 a 80 caracteres |
| `email` | Texto obligatorio y no vacío |
| `semester` | Entero entre 1 y 10 |
| `active` | Booleano, `true` por defecto |

## Ejemplos

**Crear un curso**

```http
POST /courses
```

```json
{
  "name": "Desarrollo Web II",
  "credits": 3,
  "active": true
}
```

Respuesta `201 Created`:

```json
{
  "id": 1,
  "name": "Desarrollo Web II",
  "credits": 3,
  "active": true
}
```

**Actualizar un curso**

```http
PUT /courses/1
```

```json
{
  "name": "Programación II",
  "credits": 4,
  "active": false
}
```

Respuesta `200 OK`: el curso con el mismo `id` y los datos nuevos.

**Eliminar un curso**

```http
DELETE /courses/1
```

Respuesta `200 OK`:

```json
{
  "message": "Course deleted"
}
```

**Crear un estudiante**

```http
POST /students
```

```json
{
  "name": "Ana Pérez",
  "email": "ana@universidad.edu",
  "semester": 4
}
```

Respuesta `201 Created`:

```json
{
  "id": 1,
  "name": "Ana Pérez",
  "email": "ana@universidad.edu",
  "semester": 4,
  "active": true
}
```

**Errores**

| Situación | Código | Cuerpo |
|---|---|---|
| Curso inexistente | `404` | `{"detail": "Course not found"}` |
| Estudiante inexistente | `404` | `{"detail": "Student not found"}` |
| Datos inválidos o ID no entero | `422` | Detalle de validación generado por FastAPI |

## Estructura del proyecto

```
api_acad-mica/
│
├── main.py                    # Punto de entrada: registra routers y crea las tablas
│
├── database/
│   └── database.py            # Motor SQLite, creación de tablas y get_session
│
├── models/
│   ├── course.py              # Tabla Course (table=True)
│   └── student.py             # Tabla Student (table=True)
│
├── schemas/
│   ├── course.py              # CourseCreate, CourseUpdate, CourseResponse
│   └── student.py             # StudentCreate, StudentResponse
│
├── services/
│   ├── course_service.py      # Lógica de cursos (crear, listar, consultar, actualizar, eliminar)
│   └── student_service.py     # Lógica de estudiantes (crear, listar, consultar)
│
├── routers/
│   ├── courses.py             # Endpoints /courses
│   └── students.py            # Endpoints /students
│
├── entrega-pruebas/
│   ├── informe-pruebas.md     # Informe de pruebas
│   └── evidencias/            # Capturas de Swagger y de la terminal
│
├── README.md
├── docs.md
├── ejercicio.md
└── requirements.txt
```

## Arquitectura

Cada petición recorre las capas en este orden:

```
Cliente → Router → Schema → Service → Model → Session → SQLite
```

| Capa | Responsabilidad |
|---|---|
| Router | Recibe la petición HTTP y llama al service |
| Schema | Valida los datos de entrada y define los de salida |
| Service | Ejecuta la lógica de negocio y las operaciones con la base de datos |
| Model | Representa la tabla en la base de datos |
| Session | Realiza las operaciones sobre la base de datos (`add`, `commit`, `refresh`, `delete`) |
| SQLite | Guarda los datos de forma persistente en `database.db` |

## Pruebas

Las pruebas se realizaron manualmente con Swagger y quedaron documentadas en [`entrega-pruebas/informe-pruebas.md`](entrega-pruebas/informe-pruebas.md), con sus capturas en [`entrega-pruebas/evidencias/`](entrega-pruebas/evidencias/). Cubren las operaciones de cursos y estudiantes, las validaciones, los códigos `200`, `201`, `404` y `422`, y la persistencia de los datos tras reiniciar Uvicorn.

## Notas

- `venv/` y `database.db` no se incluyen en el repositorio (están en `.gitignore`).
- Los mensajes de error se mantienen en inglés (`Course not found`, `Course deleted`, `Student not found`) porque forman parte del contrato de la API.
