from __future__ import annotations

from dataclasses import dataclass, field

from .materia import Materia


@dataclass
class Semestre:
    anio: int
    term: int
    materias: list[Materia] = field(default_factory=list)
    estudiante_id: str = ""

    def __post_init__(self):
        self.anio = int(self.anio)
        self.term = int(self.term)
        self.estudiante_id = str(self.estudiante_id).strip()
        self.materias = [
            materia if isinstance(materia, Materia) else Materia.desde_dict(materia)
            for materia in self.materias
        ]

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            datos["anio"],
            datos["term"],
            datos.get("materias", []),
            datos.get("estudiante_id", ""),
        )

    def to_dict(self):
        return {
            "anio": self.anio,
            "term": self.term,
            "materias": [materia.to_dict() for materia in self.materias],
            "estudiante_id": self.estudiante_id,
        }

    def __str__(self):
        if len(self.materias) == 0:
            return (
                f"Estudiante ID: {self.estudiante_id or 'Sin asignar'} "
                f"| Año: {self.anio} | Término: {self.term} | Sin materias registradas"
            )

        materias = ", ".join(str(materia) for materia in self.materias)
        return (
            f"Estudiante ID: {self.estudiante_id or 'Sin asignar'} "
            f"| Año: {self.anio} | Término: {self.term} | Materias: {materias}"
        )