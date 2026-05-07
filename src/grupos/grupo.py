"""Modelo de grupo para exposiciones académicas.

Este módulo define la estructura de un grupo, su tema, tutor y la lista de
identificadores de estudiantes que lo integran.
"""

from dataclasses import dataclass, field


@dataclass
class Grupo:
    """Representa un grupo de exposición dentro del sistema.

    Attributes:
        nombre_grupo (str): Nombre identificador del grupo.
        tutor (str): Docente o tutor asignado al grupo.
        tema (str): Tema que expondrá el grupo.
        integrantes_ids (list[str]): IDs de los estudiantes integrantes.
    """

    nombre_grupo: str
    tutor: str
    tema: str
    integrantes_ids: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Normaliza la lista de integrantes después de inicializar el grupo."""

        self.integrantes_ids = [str(integrante).strip() for integrante in self.integrantes_ids]

    @classmethod
    def desde_dict(cls, datos):
        """Crea un grupo a partir de un diccionario.

        Args:
            datos (dict): Datos serializados del grupo.

        Returns:
            Grupo: Instancia reconstruida desde un diccionario.
        """

        return cls(
            str(datos["nombre_grupo"]),
            str(datos["tutor"]),
            str(datos["tema"]),
            datos.get("integrantes_ids", []),
        )

    def to_dict(self):
        """Convierte el grupo a un diccionario serializable.

        Returns:
            dict: Representación del grupo lista para exportación.
        """

        return {
            "nombre_grupo": self.nombre_grupo,
            "tutor": self.tutor,
            "tema": self.tema,
            "integrantes_ids": self.integrantes_ids,
        }

    def __str__(self):
        """Devuelve una representación legible del grupo.

        Returns:
            str: Texto descriptivo del grupo y su cantidad de integrantes.
        """

        return (
            f"Grupo: {self.nombre_grupo} | Tutor: {self.tutor} | Tema: {self.tema} "
            f"| Integrantes: {len(self.integrantes_ids)}"
        )