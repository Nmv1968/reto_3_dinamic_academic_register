import uuid


class Estudiante:
    def __init__(self, nombres, correo, ci_estudiante):
        self.nombres = nombres
        self.correo = correo
        self.ci_estudiante = self._validar_ci(ci_estudiante)
        self.id_estudiante = str(uuid.uuid4())

    @staticmethod
    def _validar_ci(ci_estudiante):
        ci_limpio = str(ci_estudiante).strip()
        if len(ci_limpio) != 10 or not ci_limpio.isdigit():
            raise ValueError("La cédula debe tener exactamente 10 dígitos.")
        return ci_limpio

    @classmethod
    def desde_dict(cls, datos):
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
        return {
            "id": self.id_estudiante,
            "ci_estudiante": self.ci_estudiante,
            "nombres": self.nombres,
            "correo": self.correo,
        }

    def __str__(self):
        return (
            f"{self.nombres} | Correo: {self.correo} "
            f"| CI: {self.ci_estudiante} | ID: {self.id_estudiante}"
        )