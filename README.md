# Reto 3 - Registros dinamicos academicos

Este proyecto implementa un sistema academico en consola usando estructuras enlazadas desarrolladas manualmente en Python. El sistema administra tres dominios relacionados entre si:

- Inscritos mediante una lista simple
- Historial academico mediante una lista doble
- Grupos mediante una lista circular

Ademas incluye validaciones, persistencia en CSV y JSON, y reportes para consultar la informacion administrada por cada estructura.

## Objetivo

Aplicar estructuras enlazadas en un caso mas cercano a un sistema real, donde varias estructuras deben coexistir y compartir informacion sin perder consistencia.

## Estructura actual

```text
/reto_3_registros_dinamicos_academicos_mesias_naim
	/data
		grupos.json
		historial.json
		inscritos.csv
	/src
		app.py
		/grupos
			__init__.py
			grupo.py
			lista_circular.py
			nodo_circular.py
			persistencia_json.py
		/historial
			__init__.py
			lista_doble.py
			materia.py
			nodo_doble.py
			persistencia_json.py
			semestre.py
		/inscritos
			__init__.py
			estudiante.py
			lista_simple.py
			nodo_simple.py
			persistencia_csv.py
	README.md
```

## Componentes principales

### Inscritos

- Usa una lista simple para registrar estudiantes
- Cada estudiante se representa con la clase `Estudiante`
- El sistema genera automaticamente `id_estudiante` con UUID
- La cedula se maneja como `ci_estudiante` y debe tener exactamente 10 digitos
- Permite insertar, buscar por ID o cedula, eliminar, recorrer, exportar e importar

### Historial academico

- Usa una lista doble para almacenar semestres ordenados
- Cada semestre se modela con la clase `Semestre`
- Cada materia se modela con la clase `Materia`
- Cada semestre guarda `estudiante_id` para relacionarse con inscritos
- Permite insertar ordenadamente, buscar, eliminar, recorrer en ambos sentidos y persistir en JSON

### Grupos

- Usa una lista circular para administrar grupos
- Cada grupo se modela con la clase `Grupo`
- Cada grupo guarda `integrantes_ids` con referencias a estudiantes inscritos
- Incluye insercion, eliminacion, recorrido, rotacion y busqueda recursiva
- La persistencia de grupos se realiza en JSON

## Relacion entre estructuras

El sistema no maneja las tres listas como bloques aislados. La integracion se realiza mediante `id_estudiante`:

- Un estudiante debe existir en inscritos antes de aparecer en historial
- Un estudiante debe existir en inscritos antes de ser agregado a un grupo
- El historial academico se consulta por estudiante
- Los grupos almacenan referencias a estudiantes ya registrados

Esto permite mantener consistencia entre estructuras y evita referencias invalidas.

## Funcionalidades destacadas

- Menus en consola con operaciones separadas por modulo
- Validacion de cedula, correo y entradas numericas
- Visualizacion de datos en formato legible para consola
- Persistencia manual en CSV y JSON
- Reportes de inscritos, historial y grupos

## Complejidad principal

- Insercion al final en lista simple: O(n)
- Busqueda y eliminacion en lista simple: O(n)
- Insercion ordenada en lista doble: O(n)
- Busqueda, eliminacion y recorridos en lista doble: O(n)
- Insercion, busqueda recursiva y eliminacion en lista circular: O(n)
- Rotacion en lista circular: O(k)

## Como ejecutar

Desde la raiz del proyecto:

```bash
.venv/bin/python src/app.py
```

## Archivos de datos

- `data/inscritos.csv` guarda los estudiantes inscritos
- `data/historial.json` guarda los semestres y materias por estudiante
- `data/grupos.json` guarda los grupos y sus integrantes

## Observaciones

- El proyecto fue organizado por paquetes para separar mejor cada dominio
- La implementacion prioriza claridad academica sobre optimizaciones avanzadas
- Una mejora futura natural seria agregar un puntero `cola` en la lista simple para llevar `insertar_final` de O(n) a O(1)
