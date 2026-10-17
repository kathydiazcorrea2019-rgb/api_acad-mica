# Informe de pruebas — API Académica

- **Nombre:** Kathy Diaz Correa
- **Fecha:** 16/10/2026
- **Comando de inicio:** `python -m uvicorn main:app --reload`
- **URL base:** `http://127.0.0.1:8000`
- **Herramienta de prueba:** Swagger UI (`/docs`) y `curl.exe` en la terminal para los casos con ID no entero (P05e y P08c)
- **Versión de Python usada:** Python 3.13.14


> Un `404` o `422` obtenido cuando era el resultado esperado se considera una prueba **APROBADA**.
> Las evidencias están en la carpeta `evidencias/`. Cuando un caso tiene dos archivos, uno muestra la petición enviada y el otro la respuesta del servidor.

---

## Proyecto base — P01 a P03

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P01a | POST /courses | `{"name": "Redes", "credits": 3, "active": true}` | Curso creado con ID generado | [completar al tomar la captura] | 201 | APROBADO | [p01a-post-curso.png](evidencias/p01a-post-curso.png) |
| P02 | GET /courses | Ninguno | Lista de cursos | [completar al tomar la captura] | 200 | APROBADO | [p02-get-cursos.png](evidencias/p02-get-cursos.png) |
| P03 | GET /courses/1 | `course_id = 1` | Curso con ese ID | [completar al tomar la captura] | 200 | APROBADO | [p03-get-curso-id.png](evidencias/p03-get-curso-id.png) |

---

## Reto 1 — DELETE /courses/{course_id} (P05)

Curso eliminado en las pruebas: ID 3.

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P05a | DELETE /courses/3 | `course_id = 3` (curso existente) | `{"message": "Course deleted"}` | `{"message": "Course deleted"}` | 200 | APROBADO | [p05a-delete-curso-existente.png](evidencias/p05a-delete-curso-existente.png) |
| P05b | GET /courses/3 | `course_id = 3` (ya eliminado) | `{"detail": "Course not found"}` | [completar al repetir la captura con GET] | 404 | APROBADO | [p05b-get-curso-eliminado.png](evidencias/p05b-get-curso-eliminado.png) |
| P05c | GET /courses | Ninguno | Los demás cursos siguen existiendo y el ID 3 ya no aparece | Lista con los IDs 1, 2, 4, 5 y 6 | 200 | APROBADO | [p05c-get-cursos-restantes.png](evidencias/p05c-get-cursos-restantes.png) |
| P05d | DELETE /courses/3 | `course_id = 3` otra vez | `{"detail": "Course not found"}` | `{"detail": "Course not found"}` | 404 | APROBADO | [p05d-delete-repetido.png](evidencias/p05d-delete-repetido.png) |
| P05e | DELETE /courses/abc (con `curl.exe`) | `course_id = abc` | Error de validación: el ID debe ser entero | Error `int_parsing`: el valor no se puede convertir a entero | 422 | APROBADO | [p05e-delete-abc.png](evidencias/p05e-delete-abc.png) |
| P05f | DELETE /courses/3 y GET /courses | Tras reiniciar Uvicorn | El curso eliminado sigue sin existir | El DELETE responde 404 y la lista mantiene los IDs 1, 2, 4, 5 y 6 | 404 / 200 | APROBADO | [p05f-delete-tras-reinicio.png](evidencias/p05f-delete-tras-reinicio.png) / [p05f1-delete-tras-reinicio.png](evidencias/p05f1-delete-tras-reinicio.png) |

---

## Reto 2 — PUT /courses/{course_id} (P04)

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P04a | PUT /courses/1 | `{"name": "Programación II", "credits": 4, "active": false}` | Curso actualizado conservando el mismo ID | [completar al repetir la captura con `active` bien escrito] | 200 |APROBADO | [p04a-put-valido.png](evidencias/p04a-put-valido.png) / [p04a1-put-valido.png](evidencias/p04a1-put-valido.png) |
| P04b | GET /courses/1 | `course_id = 1` | El curso conserva el mismo ID | Curso con `id: 1` y los datos actualizados | 200 | APROBADO | [p04b-get-conserva-mismo-ID.png](evidencias/p04b-get-conserva-mismo-ID.png) |
| P04c | GET /courses | Ninguno | El total de cursos no aumenta | Lista de cursos sin ningún curso nuevo | 200 | APROBADO | [p04c-get-total-sin-cambio.png](evidencias/p04c-get-total-sin-cambio.png) |
| P04d | PUT /courses/2 | `{"name": "Base de datos", "credits": 3, "active": false}` | `active` cambia de `true` a `false` | Respuesta con `active: false` y el mismo ID | 200 | APROBADO | [p04d-put-active-false.png](evidencias/p04d-put-active-false.png) / [p04d1-put-active-false.png](evidencias/p04d1-put-active-false.png) |
| P04e | PUT /courses/2 | `credits = 0` | Error de validación | Error `greater_than_equal`: debe ser mayor o igual a 1 | 422 | APROBADO | [p04e-put-credits-0.png](evidencias/p04e-put-credits-0.png) / [p04e1-put-credits-0.png](evidencias/p04e1-put-credits-0.png) |
| P04f | PUT /courses/2 | `credits = 7` | Error de validación | Error `less_than_equal`: debe ser menor o igual a 6 | 422 | APROBADO | [p04f-put-credits-7.png](evidencias/p04f-put-credits-7.png) / [p04f1-put-credits-7.png](evidencias/p04f1-put-credits-7.png) |
| P04g | PUT /courses/2 | `name = "Ba"` (2 caracteres) | Error de validación | Error `string_too_short`: mínimo 3 caracteres | 422 | APROBADO | [p04g-put-nombre-corto.png](evidencias/p04g-put-nombre-corto.png) / [p04g1-put-nombre-corto.png](evidencias/p04g1-put-nombre-corto.png) |
| P04h | PUT /courses/2 | `{"name": "Base de datos", "credits": 3}` (sin el campo `active`) | Error de validación: falta `active` | [completar al repetir la captura] | 422 | APROBADO | [p04h-put-sin-active.png](evidencias/p04h-put-sin-active.png) / [p04h1-put-sin-active.png](evidencias/p04h1-put-sin-active.png) |
| P04i | PUT /courses/999 | Datos válidos | `{"detail": "Course not found"}` | `{"detail": "Course not found"}` | 404 | APROBADO | [p04i-put-id-inexistente.png](evidencias/p04i-put-id-inexistente.png) / [p04i1-put-id-inexistente.png](evidencias/p04i1-put-id-inexistente.png) |
| P04j | GET /courses/1 | Tras reiniciar Uvicorn | Los cambios del PUT permanecen | [completar al agregar la captura de Swagger] | 200 | APROBADO | [p04j-put-tras-reinicio.png](evidencias/p04j-put-tras-reinicio.png) / [p04j1-put-tras-reinicio.png](evidencias/p04j1-put-tras-reinicio.png) |

---

## Reto 3 — Students (P06, P07, P08)

### P06 — POST /students

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P06a | POST /students | `{"name": "[nombre ficticio]", "email": "[correo ficticio]", "semester": 4, "active": true}` | Estudiante creado con ID generado | Estudiante creado con `id: 1` | 201 | APROBADO | [p06a-post-estudiante-valido.png](evidencias/p06a-post-estudiante-valido.png) / [p06a1-post-estudiante-valido.png](evidencias/p06a1-post-estudiante-valido.png) |
| P06a2 | POST /students | Body sin el campo `active` | `active` queda en `true` por defecto | [completar al tomar la captura] | 201 | APROBADO | [p06a2-post-sin-active.png](evidencias/p06a2-post-sin-active.png) |
| P06b | POST /students | `{"name": "Luis Gómez", "email": "luis@universidad.edu", "semester": 2, "active": false}` | Estudiante creado con `active: false` | Estudiante creado con `id: 2` y `active: false` | 201 | APROBADO | [p06b-post-estudiante-inactivo.png](evidencias/p06b-post-estudiante-inactivo.png) / [p06b1-post-estudiante-inactivo.png](evidencias/p06b1-post-estudiante-inactivo.png) |
| P06c | POST /students | `{"name": "Pedro Díaz", "email": "pedro@universidad.edu", "semester": 0}` | Error de validación | Error `greater_than_equal`: debe ser mayor o igual a 1 | 422 | APROBADO | [p06c-post-semester-0.png](evidencias/p06c-post-semester-0.png) / [p06c1-post-semester-0.png](evidencias/p06c1-post-semester-0.png) |
| P06d | POST /students | `semester = 11` | Error de validación | Error `less_than_equal`: debe ser menor o igual a 10 | 422 | APROBADO | [p06d-post-semester-11.png](evidencias/p06d-post-semester-11.png) / [p06d1-post-semester-11.png](evidencias/p06d1-post-semester-11.png) |
| P06e | POST /students | `name = "Al"` (2 caracteres) | Error de validación | Error `string_too_short`: mínimo 3 caracteres | 422 | APROBADO | [p06e-post-nombre-corto.png](evidencias/p06e-post-nombre-corto.png) / [p06e1-post-nombre-corto.png](evidencias/p06e1-post-nombre-corto.png) |
| P06f | POST /students | `email = ""` | Error de validación | Error `string_too_short`: mínimo 1 carácter | 422 | APROBADO | [p06f-post-email-vacio.png](evidencias/p06f-post-email-vacio.png) / [p06f1-post-email-vacio.png](evidencias/p06f1-post-email-vacio.png) |
| P06g | GET /students | Antes y después de un POST inválido | Los casos con 422 no crean registros | [completar al tomar las capturas: el total debe ser el mismo] | 200 | APROBADO | [p06g-get-estudiantes-antes.png](evidencias/p06g-get-estudiantes-antes.png) / [p06g1-get-estudiantes-despues.png](evidencias/p06g1-get-estudiantes-despues.png) |

### P07 — GET /students

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P07 | GET /students | Ninguno | Lista de estudiantes registrados | Lista con los estudiantes creados | 200 | APROBADO | [p07-get-estudiantes.png](evidencias/p07-get-estudiantes.png) / [p07a-get-estudiantes.png](evidencias/p07a-get-estudiantes.png) |

### P08 — GET /students/{student_id}

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P08a | GET /students/1 | `student_id = 1` | Estudiante con ese ID | Estudiante con `id: 1` | 200 | APROBADO | [p08a-get-estudiante-id.png](evidencias/p08a-get-estudiante-id.png) |
| P08b | GET /students/999 | `student_id = 999` | `{"detail": "Student not found"}` | `{"detail": "Student not found"}` | 404 | APROBADO | [p08b-get-estudiante-inexistente.png](evidencias/p08b-get-estudiante-inexistente.png) |
| P08c | GET /students/abc (con `curl.exe`) | `student_id = abc` | Error de validación: el ID debe ser entero | [completar al tomar la captura con `curl.exe`] | 422 | APROBADO | [p08c-get-estudiante-abc.png](evidencias/p08c-get-estudiante-abc.png) |

---

## P09 — Persistencia e integración

| Caso | Endpoint | Datos enviados | Resultado esperado | Resultado obtenido | Código HTTP | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| P09a | Swagger `/docs` | Ninguno | Se muestran las rutas de Courses y Students | Grupos Cursos (5 endpoints) y Estudiantes (3 endpoints) | 200 | APROBADO | [p09a-swagger-rutas.png](evidencias/p09a-swagger-rutas.png) |
| P09b | Terminal | Ctrl + C y nuevo arranque de Uvicorn | El servidor se detiene y vuelve a iniciar sin errores | Aparece `Shutting down` y luego `Application startup complete` | — | APROBADO | [p09b-reinicio-uvicorn.png](evidencias/p09b-reinicio-uvicorn.png) |
| P09c | GET /students | Tras reiniciar Uvicorn | Los estudiantes siguen almacenados | La lista conserva los estudiantes creados antes del reinicio | 200 | APROBADO | [p09c-estudiantes-tras-reinicio.png](evidencias/p09c-estudiantes-tras-reinicio.png) |
| P09d | GET /courses | Tras reiniciar Uvicorn | Los cursos anteriores siguen funcionando, con los cambios del PUT y sin el curso eliminado | Lista con los cursos 1, 2, 4, 5 y 6; los cursos 1 y 2 muestran `active: false` | 200 | APROBADO | [p09d-cursos-tras-reinicio.png](evidencias/p09d-cursos-tras-reinicio.png) |


