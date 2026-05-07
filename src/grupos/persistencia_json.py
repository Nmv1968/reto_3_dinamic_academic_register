"""Funciones de persistencia JSON para grupos de exposición.

Este módulo reúne las operaciones de exportación e importación de la lista
circular de grupos usando archivos JSON.
"""

import json

from .grupo import Grupo


def exportar_grupos_json(lista, ruta):
	"""Exporta los grupos a un archivo JSON.

	Args:
		lista (ListaCircular): Lista circular con los grupos a exportar.
		ruta (str): Ruta del archivo JSON de salida.
	"""

	datos = [grupo.to_dict() for grupo in lista.recorrer()]
	with open(ruta, "w", encoding="utf-8") as archivo:
		json.dump(datos, archivo, indent=2, ensure_ascii=False)


def importar_grupos_json(ruta, lista=None):
	"""Importa grupos desde un archivo JSON.

	Args:
		ruta (str): Ruta del archivo JSON de entrada.
		lista (ListaCircular | None): Lista destino opcional para reutilizar.

	Returns:
		ListaCircular: Lista circular cargada con los grupos importados.
	"""

	from .lista_circular import ListaCircular

	destino = lista if lista is not None else ListaCircular()
	destino.limpiar()

	with open(ruta, "r", encoding="utf-8") as archivo:
		contenido = archivo.read().strip()

	if contenido == "":
		return destino

	datos = json.loads(contenido)
	for grupo in datos:
		destino.insertar(Grupo.desde_dict(grupo))

	return destino