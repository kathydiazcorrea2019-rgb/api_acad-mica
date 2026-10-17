from pydantic import BaseModel, Field

# Esquema de entrada: valida el cuerpo JSON antes de ejecutar el endpoint.
class StudentCreate(BaseModel):
    # El nombre debe tener entre 3 y 80 caracteres.
    name: str = Field(min_length=3, max_length=80)
    # El correo es obligatorio y no puede ir vacio.
    email: str = Field(min_length=1)
    #El semestre debe estar entre 1 y 10.
    semester: int = Field(ge=1,  le=10)

    # Si se omite, el estudiante queda activo.
    active: bool = True

# Esquema de salida: define los campos devueltos al cliente, incluido el ID.
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    semester: int
    active: bool
    