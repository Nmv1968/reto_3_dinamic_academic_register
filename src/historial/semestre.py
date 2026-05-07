from __future__ import annotations

from dataclasses import dataclass, field

from .materia import Materia


@dataclass
class Semestre:
    anio: int
    term: int
    materias: list[Materia] = field(default_factory=list)

    def __post_init__(self):
        self.anio = int(self.anio)
        self.term = int(self.term)
        self.materias = [
            materia if isinstance(materia, Materia) else Materia.desde_dict(materia)
            for materia in self.materias
        ]

    @classmethod
    def desde_dict(cls, datos):
        return cls(datos["anio"], datos["term"], datos.get("materias", []))

    def to_dict(self):
        return {
            "anio": self.anio,
            "term": self.term,
            "materias": [materia.to_dict() for materia in self.materias],
        }

    def __str__(self):
        if len(self.materias) == 0:
            return f"Año: {self.anio} | Término: {self.term} | Sin materias registradas"

        materias = ", ".join(str(materia) for materia in self.materias)
        return f"Año: {self.anio} | Término: {self.term} | Materias: {materias}"