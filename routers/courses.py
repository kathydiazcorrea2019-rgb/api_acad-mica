from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_session
from schemas.course import CourseCreate, CourseResponse, CourseUpdate

from services.course_service import (
    create_course,
    list_courses,
    get_course,
    update_course,
    delete_course
)


# Agrupa las rutas bajo /courses y la etiqueta Courses en Swagger.
router = APIRouter(
    prefix="/courses",
    tags=["Cursos"]
)


# POST /courses: recibe datos validados y responde con el curso creado (201).
@router.post(
    "",
    response_model=CourseResponse,
    status_code=201,
    summary="Crear curso",
    description="Registra un nuevo curso en la base de datos"
)
def create_course_endpoint(
    # FastAPI interpreta CourseCreate como el cuerpo JSON de la petición.
    course: CourseCreate,
    # Depends obtiene y libera la sesión mediante get_session.
    session: Session = Depends(get_session)
):

    return create_course(
        course,
        session
    )


# GET /courses: devuelve todos los cursos como una lista.
@router.get(
    "",
    response_model=list[CourseResponse],
    summary="Listar cursos",
    description="Devuelve todos los cursos registrados"
)
def list_courses_endpoint(
    # Depends obtiene y libera la sesión mediante get_session.
    session: Session = Depends(get_session)
):

    return list_courses(session)


# GET /courses/{course_id}: toma el ID de la URL y lo valida como entero.
@router.get(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Consultar curso por su ID",
    description="Devuelve un curso segun su identificador"
)
def get_course_endpoint(
    course_id: int,
    # Depends obtiene y libera la sesión mediante get_session.
    session: Session = Depends(get_session)
):

    return get_course(
        course_id,
        session
    )
# PUT /courses/{course_id}: reemplaza los tres campos del curso existente.
@router.put(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Actualizar curso",
    description="Actualizar por completo un curso existente conservando su ID."

)
def update_course_endpoint(
    course_id: int,
    # CourseUpdate exige name, credits y activate en el cuerpo JSON.
    course: CourseUpdate,
    session: Session = Depends(get_session)
):

    return update_course(
        course_id,
        course,
        session
    )

# DELETE /courses/{course_id}: elimina el curso y confirma con un mensaje.
@router.delete(
    "/{course_id}",
    summary="Eliminar curso",
    description="Elimina un curso segun su identificador."
)
def delete_course_endpoint(
    course_id: int,
    session: Session = Depends(get_session)
):
    return delete_course(
        course_id,
        session
    )