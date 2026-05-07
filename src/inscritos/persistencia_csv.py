"""Funciones de persistencia CSV para estudiantes inscritos.

Este módulo concentra la exportación e importación de la lista simple de
inscritos usando archivos CSV con codificación UTF-8.
"""

import csv

from .estudiante import Estudiante


CAMPOS_INSCRITOS = ("id", "ci_estudiante", "nombres", "correo")


def exportar_inscritos_csv(lista, ruta):
	"""Exporta los inscritos de una lista simple a un archivo CSV.

	Args:
		lista (ListaSimple): Lista simple con los estudiantes a exportar.
		ruta (str): Ruta del archivo CSV de salida.
	"""

	with open(ruta, "w", newline="", encoding="utf-8") as archivo:
		escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_INSCRITOS)
		escritor.writeheader()
		for inscrito in lista.recorrer():
			escritor.writerow(inscrito.to_dict())


def importar_inscritos_csv(ruta, lista=None):
	"""Importa inscritos desde un archivo CSV.

	Args:
		ruta (str): Ruta del archivo CSV de entrada.
		lista (ListaSimple | None): Lista destino opcional para reutilizar.

	Returns:
		ListaSimple: Lista simple cargada con los estudiantes importados.
	"""

	from .lista_simple import ListaSimple

	destino = lista if lista is not None else ListaSimple()
	destino.limpiar()

	with open(ruta, "r", newline="", encoding="utf-8") as archivo:
		lector = csv.DictReader(archivo)
		for fila in lector:
			destino.insertar_final(Estudiante.desde_dict(fila))

	return destino