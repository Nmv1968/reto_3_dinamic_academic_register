"""Modelo de estudiante para el módulo de inscritos.

Este módulo define la entidad Estudiante, encargada de validar la cédula,
generar el identificador interno y convertir la información desde o hacia
estructuras serializables.
"""

import uuid


class Estudiante:
    """Representa a un estudiante inscrito en el sistema.

    Attributes:
        nombres (str): Nombres completos del estudiante.
        correo (str): Correo electrónico del estudiante.
        ci_estudiante (str): Cédula validada de 10 dígitos.
        id_estudiante (str): Identificador interno generado con UUID.
    """

    def __init__(self, nombres, correo, ci_estudiante):
        """Inicializa un estudiante con sus datos principales.

        Args:
            nombres (str): Nombres completos del estudiante.
            correo (str): Correo electrónico del estudiante.
            ci_estudiante (str): Cédula del estudiante.
        """

        self.nombres = nombres
        self.correo = correo
        self.ci_estudiante = self._validar_ci(ci_estudiante)
        self.id_estudiante = str(uuid.uuid4())

    @staticmethod
    def _validar_ci(ci_estudiante):
        """Valida que la cédula tenga exactamente 10 dígitos.

        Args:
            ci_estudiante (str): Cédula a validar.

        Returns:
            str: Cédula limpia y validada.

        Raises:
            ValueError: Si la cédula no tiene 10 dígitos numéricos.
        """

        ci_limpio = str(ci_estudiante).strip()
        if len(ci_limpio) != 10 or not ci_limpio.isdigit():
            raise ValueError("La cédula debe tener exactamente 10 dígitos.")
        return ci_limpio

    @classmethod
    def desde_dict(cls, datos):
        """Crea un estudiante a partir de un diccionario.

        Args:
            datos (dict): Datos serializados del estudiante.

        Returns:
            Estudiante: Instancia reconstruida desde un diccionario.
        """

        estudiante = cls(
            datos["nombres"],
            datos["correo"],
            datos.get("ci_estudiante") or datos.get("id") or "",
        )

        id_estudiante = datos.get("id")
        if id_estudiante is not None and str(id_estudiante).strip() != "":
            estudiante.id_estudiante = str(id_estudiante).strip()

        return estudiante

    def to_dict(self):
        """Convierte el estudiante a un diccionario serializable.

        Returns:
            dict: Representación del estudiante lista para exportación.
        """

        return {
            "id": self.id_estudiante,
            "ci_estudiante": self.ci_estudiante,
            "nombres": self.nombres,
            "correo": self.correo,
        }

    def __str__(self):
        """Devuelve una representación legible del estudiante.

        Returns:
            str: Texto descriptivo del estudiante.
        """

        return (
            f"{self.nombres} | Correo: {self.correo} "
            f"| CI: {self.ci_estudiante} | ID: {self.id_estudiante}"
        )