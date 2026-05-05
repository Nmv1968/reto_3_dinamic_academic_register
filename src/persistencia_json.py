import json


def exportar_historial_json(lista, ruta):
	datos = lista.recorrer_adelante()
	with open(ruta, "w", encoding="utf-8") as archivo:
		json.dump(datos, archivo, indent=2, ensure_ascii=False)


def importar_historial_json(ruta, lista=None):
	from lista_doble import ListaDoble

	destino = lista if lista is not None else ListaDoble()
	destino.limpiar()

	with open(ruta, "r", encoding="utf-8") as archivo:
		contenido = archivo.read().strip()

	if contenido == "":
		return destino

	datos = json.loads(contenido)
	for semestre in datos:
		destino.insertar_ordenado(semestre)

	return destino


def exportar_grupos_json(lista, ruta):
	datos = lista.recorrer()
	with open(ruta, "w", encoding="utf-8") as archivo:
		json.dump(datos, archivo, indent=2, ensure_ascii=False)


def importar_grupos_json(ruta, lista=None):
	from lista_circular import ListaCircular

	destino = lista if lista is not None else ListaCircular()
	destino.limpiar()

	with open(ruta, "r", encoding="utf-8") as archivo:
		contenido = archivo.read().strip()

	if contenido == "":
		return destino

	datos = json.loads(contenido)
	for grupo in datos:
		destino.insertar(grupo)

	return destino
