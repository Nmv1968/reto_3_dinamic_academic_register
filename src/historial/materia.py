"""Modelo de materia para el historial académico.

Este módulo define la estructura básica de una materia registrada dentro de un
semestre académico.
"""

from dataclasses import dataclass


@dataclass
class Materia:
    """Representa una materia cursada en un semestre.

    Attributes:
        cod (str): Código identificador de la materia.
        nombre (str): Nombre de la materia.
        nota (float): Calificación obtenida.
    """

    cod: str
    nombre: str
    nota: float

    @classmethod
    def desde_dict(cls, datos):
        """Crea una materia a partir de un diccionario.

        Args:
            datos (dict): Datos serializados de la materia.

        Returns:
            Materia: Instancia reconstruida desde un diccionario.
        """

        return cls(str(datos["cod"]), str(datos["nombre"]), float(datos["nota"]))

    def to_dict(self):
        """Convierte la materia a un diccionario serializable.

        Returns:
            dict: Representación lista para persistencia.
        """

        return {"cod": self.cod, "nombre": self.nombre, "nota": self.nota}

    def __str__(self):
        """Devuelve una representación legible de la materia.

        Returns:
            str: Texto descriptivo de la materia y su nota.
        """

        return f"{self.cod} {self.nombre} | Nota: {self.nota}"