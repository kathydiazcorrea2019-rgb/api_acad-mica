from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_session
from schemas.student import StudentCreate, StudentResponse

from services.student_service import (
    create_student,
    list_students,
    get_student
)

# Agrupa las rutas bajo /students y la etiqueta Estudiantes en Swagger.
router = APIRouter(
    prefix="/students",
    tags=["Estudiantes"]
)

# POST /students: recibe datos validados y responde con el estudiante creado (201).
@router.post(
    "",
    response_model=StudentResponse,
    status_code=201,
    summary="Crear estudiante",
    description="Registra un nuevo estudiante en la base de datos."
)
def create_student_endpoint(
    student: StudentCreate,
    session: Session = Depends(get_session)
):

    return create_student(
        student,
        session
    )

# GET /students: devuelve todos los estudiantes como una lista.
@router.get(
    "",
    response_model=list[StudentResponse],
    summary="Listar estudiantes",
    description="Devuelve todos los estudiantes registrados."
)
def list_students_endpoint(
    session: Session = Depends(get_session)
):
    return list_students(session)

# GET /students/{student_id}: toma el ID de la URL y lo valida como entero.
@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Consultar estudiante por su ID",
    description="Devuelve un estudiante segun su identificador."
)
def get_student_endpoint(
    student_id: int,
    session: Session = Depends(get_session)
):
    return get_student(
        student_id,
        session
    )
