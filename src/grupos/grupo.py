from dataclasses import dataclass


@dataclass
class Grupo:
    nombre_grupo: str
    tutor: str
    tema: str

    @classmethod
    def desde_dict(cls, datos):
        return cls(str(datos["nombre_grupo"]), str(datos["tutor"]), str(datos["tema"]))

    def to_dict(self):
        return {
            "nombre_grupo": self.nombre_grupo,
            "tutor": self.tutor,
            "tema": self.tema,
        }

    def __str__(self):
        return f"Grupo: {self.nombre_grupo} | Tutor: {self.tutor} | Tema: {self.tema}"