# INVENTARIO — pva-swarm

Repo: `Jaime393/pva-swarm`, rama `main`.
Leído en vivo: 2026-11-09 ~07:40 -05. Todos los archivos leídos íntegros (raíz + `.github/workflows/`).
Fuente de los tamaños: listado de GitHub (`get_file_contents`, path `""`).

## Archivos (9, 3.844 B en total)

| Archivo | Tamaño | Qué es |
|---|---|---|
| `README.md` | 587 B | Descripción del proyecto y uso |
| `app.py` | 2.426 B | Servidor HTTP (stdlib, sin FastAPI) |
| `papers.json` | 195 B | La "base de datos": 2 papers |
| `Dockerfile` | 170 B | Imagen `python:3.11-slim`, CMD uvicorn |
| `Makefile` | 173 B | Objetivos repro, reproduce, dev, test |
| `requirements.txt` | 51 B | Solo `requests` |
| `.gitignore` | 31 B | `*.tar.gz`, `swarm.db`, `__pycache__/` |
| `.github/workflows/pva.yml` | 211 B | Workflow CI (instala fastapi, compila app.py) |

Suma verificada: 587 + 2.426 + 195 + 170 + 173 + 51 + 31 + 211 = 3.844 B.

## Lo que NO hay

- No hay `tests/` ni ningún archivo de pruebas.
- No hay `LICENSE`.
- No hay `data/` ni ningún CSV o dataset.
- No hay archivo SQLite (`swarm.db` solo aparece en `.gitignore`; el código no lo crea).
- No hay ningún archivo HTMX, ni plantilla HTML más allá de la cadena de una línea en `app.py`.
- No hay ningún archivo FastAPI: `app.py` no importa `fastapi` ni define un objeto `app`.

## NO SÉ

- **NO SÉ — si existe algún despliegue en Fly.io u Oracle.** El README lo sugiere como opción; el repo no trae URL, ni configuración de despliegue más allá del `Dockerfile`.
- **NO SÉ — si `app.py` se ejecutó alguna vez en producción.** No hay logs ni resultados en el repo.
- **NO SÉ — por qué los commits son de Jaime363 si el dueño del repo es Jaime393.** Dato del historial, sin explicación en el repo.
