from dataclasses import dataclass


@dataclass
class Materia:
    cod: str
    nombre: str
    nota: float

    @classmethod
    def desde_dict(cls, datos):
        return cls(str(datos["cod"]), str(datos["nombre"]), float(datos["nota"]))

    def to_dict(self):
        return {"cod": self.cod, "nombre": self.nombre, "nota": self.nota}

    def __str__(self):
        return f"{self.cod} {self.nombre} | Nota: {self.nota}"