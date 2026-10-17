from sqlmodel import SQLModel, Field

# table=True convierte este modelo en la tabla student dentro de database.db.
class Student(SQLModel, table=True):
    # La clave primaria la asigna SQLite al insertar el registro.
    id: int | None = Field(
        default=None,
        primary_key=True
    )

    name: str

    email: str

    semester: int

    # Un estudiante nuevo queda activo si no se indica otro valor.
    active: bool = True
    