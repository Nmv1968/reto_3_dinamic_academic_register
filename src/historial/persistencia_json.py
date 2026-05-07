"""Funciones de persistencia JSON para el historial académico.

Este módulo reúne las operaciones de exportación e importación de la lista
doble del historial académico usando archivos JSON.
"""

import json

from .semestre import Semestre


def exportar_historial_json(lista, ruta):
	"""Exporta el historial académico a un archivo JSON.

	Args:
		lista (ListaDoble): Lista doble que se desea exportar.
		ruta (str): Ruta del archivo JSON de salida.
	"""

	datos = [semestre.to_dict() for semestre in lista.recorrer_adelante()]
	with open(ruta, "w", encoding="utf-8") as archivo:
		json.dump(datos, archivo, indent=2, ensure_ascii=False)


def importar_historial_json(ruta, lista=None):
	"""Importa el historial académico desde un archivo JSON.

	Args:
		ruta (str): Ruta del archivo JSON de entrada.
		lista (ListaDoble | None): Lista destino opcional para reutilizar.

	Returns:
		ListaDoble: Lista doble cargada con los semestres importados.
	"""

	from .lista_doble import ListaDoble

	destino = lista if lista is not None else ListaDoble()
	destino.limpiar()

	with open(ruta, "r", encoding="utf-8") as archivo:
		contenido = archivo.read().strip()

	if contenido == "":
		return destino

	datos = json.loads(contenido)
	for semestre in datos:
		destino.insertar_ordenado(Semestre.desde_dict(semestre))

	return destino