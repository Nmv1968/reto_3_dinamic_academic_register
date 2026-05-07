import json

from .grupo import Grupo


def exportar_grupos_json(lista, ruta):
	datos = [grupo.to_dict() for grupo in lista.recorrer()]
	with open(ruta, "w", encoding="utf-8") as archivo:
		json.dump(datos, archivo, indent=2, ensure_ascii=False)


def importar_grupos_json(ruta, lista=None):
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