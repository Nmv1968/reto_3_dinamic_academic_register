"""Modelo de semestre para el historial académico.

Este módulo define la estructura de un semestre, incluyendo el año, el término,
las materias registradas y el identificador del estudiante al que pertenece.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .materia import Materia


@dataclass
class Semestre:
    """Representa un semestre académico asociado a un estudiante.

    Attributes:
        anio (int): Año al que pertenece el semestre.
        term (int): Término académico dentro del año.
        materias (list[Materia]): Materias registradas en el semestre.
        estudiante_id (str): Identificador interno del estudiante asociado.
    """

    anio: int
    term: int
    materias: list[Materia] = field(default_factory=list)
    estudiante_id: str = ""

    def __post_init__(self):
        """Normaliza los valores del semestre después de inicializarlo."""

        self.anio = int(self.anio)
        self.term = int(self.term)
        self.estudiante_id = str(self.estudiante_id).strip()
        self.materias = [
            materia if isinstance(materia, Materia) else Materia.desde_dict(materia)
            for materia in self.materias
        ]

    @classmethod
    def desde_dict(cls, datos):
        """Crea un semestre a partir de un diccionario.

        Args:
            datos (dict): Datos serializados del semestre.

        Returns:
            Semestre: Instancia reconstruida desde un diccionario.
        """

        return cls(
            datos["anio"],
            datos["term"],
            datos.get("materias", []),
            datos.get("estudiante_id", ""),
        )

    def to_dict(self):
        """Convierte el semestre a un diccionario serializable.

        Returns:
            dict: Representación lista para persistencia.
        """

        return {
            "anio": self.anio,
            "term": self.term,
            "materias": [materia.to_dict() for materia in self.materias],
            "estudiante_id": self.estudiante_id,
        }

    def __str__(self):
        """Devuelve una representación legible del semestre.

        Returns:
            str: Texto descriptivo del semestre y sus materias.
        """

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