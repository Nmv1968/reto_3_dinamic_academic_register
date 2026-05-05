import uuid


class Estudiante:
    def __init__(self, nombres, correo, id_estudiante=None):
        self.nombres = nombres
        self.correo = correo
        if id_estudiante is None or str(id_estudiante).strip() == "":
            self.id_estudiante = str(uuid.uuid4())
        else:
            self.id_estudiante = str(id_estudiante)

    def to_dict(self):
        return {
            "id": self.id_estudiante,
            "nombres": self.nombres,
            "correo": self.correo,
        }

    def __str__(self):
        return f"{self.nombres} | Correo: {self.correo} | ID: {self.id_estudiante}"