from dataclasses import dataclass, field


@dataclass
class Grupo:
    nombre_grupo: str
    tutor: str
    tema: str
    integrantes_ids: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.integrantes_ids = [str(integrante).strip() for integrante in self.integrantes_ids]

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            str(datos["nombre_grupo"]),
            str(datos["tutor"]),
            str(datos["tema"]),
            datos.get("integrantes_ids", []),
        )

    def to_dict(self):
        return {
            "nombre_grupo": self.nombre_grupo,
            "tutor": self.tutor,
            "tema": self.tema,
            "integrantes_ids": self.integrantes_ids,
        }

    def __str__(self):
        return (
            f"Grupo: {self.nombre_grupo} | Tutor: {self.tutor} | Tema: {self.tema} "
            f"| Integrantes: {len(self.integrantes_ids)}"
        )