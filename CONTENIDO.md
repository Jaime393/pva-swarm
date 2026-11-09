# CONTENIDO — pva-swarm

Repo: `Jaime393/pva-swarm`, rama `main`.
Leído en vivo: 2026-11-09 ~07:40 -05. Todos los números abajo se leyeron de los archivos del repo, no de memoria.

## Qué hace (verificado en el código)

Un servidor HTTP mínimo en stdlib que guarda papers en un JSON:

- 2 rutas GET (`/` y `/api` → una línea HTML; `/api/papers` → el contenido de `papers.json`).
- 1 ruta POST (`/api/papers` → añade `{"doi","title"}` a `papers.json`).
- Estado actual: 2 papers registrados, 195 B.

## Discrepancias medidas (README y archivos contra el código)

1. **FastAPI + SQLite + HTMX, prometidos; stdlib + JSON, entregados.** El README anuncia FastAPI, SQLite y HTMX. `app.py` no importa ninguno de los tres: usa `http.server` y un archivo JSON. No hay ninguna tabla, ningún template HTMX.
2. **`uvicorn app:app` no puede arrancar.** El `Dockerfile` (CMD) y el `Makefile` (`dev`) y el README usan `uvicorn app:app`. `app.py` no define ningún objeto `app` (define `Handler`, `run`, `DB`). La única vía de arranque que existe es el servidor stdlib (`python app.py`, puerto 8000 por defecto).
3. **`requests` no se usa.** Es la única dependencia de `requirements.txt`; ningún archivo del repo la importa.
4. **No hay validación adversarial.** El README promete registro de validadores, `fail_refutation` / `counterexample` y tablero público. El código no tiene ninguna de las tres: el POST acepta cualquier `doi`/`title` (incluso vacíos, porque `get()` usa `""` por defecto), sin deduplicar, sin autenticar.
5. **`swarm.db` no existe.** `.gitignore` lo ignora y el commit inicial lo anuncia (SQLite), pero el código nunca crea una base SQLite.
6. **`test` no prueba nada.** El objetivo `test` del Makefile solo compila `app.py` (`py_compile`). No hay tests.
7. **El workflow instala lo que el código no usa.** `.github/workflows/pva.yml` instala `fastapi uvicorn python-multipart` y solo compila `app.py`. Compilaría bien, pero no ejecuta la aplicación.

## Números verificados

- 9 archivos, 3.844 B en total.
- 6 commits, todos el 2026-09-10, de 17:02:00Z a 21:22:34Z.
- 2 papers en `papers.json`.
- 0 tests, 0 LICENSE, 0 archivos FastAPI, 0 archivos SQLite, 0 archivos HTMX.
- 2 rutas GET con respuesta útil (`/api/papers`) y 1 ruta POST.

## NO SÉ

- **NO SÉ — si los 2 DOI resuelven en Zenodo.** No verificado en esta minería.
- **NO SÉ — si el servidor llegó a correr en algún lugar.** No hay logs, ni URL, ni resultados en el repo.
- **NO SÉ — qué valida el "PVA score" aquí.** El README no lo menciona; ningún archivo calcula un score.
