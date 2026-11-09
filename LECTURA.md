# LECTURA — pva-swarm

Repo: `Jaime393/pva-swarm`, rama `main`.
Leído en vivo: 2026-11-09 ~07:40 -05 (los 9 archivos, íntegros).

## Qué dice el README (texto íntegro)

> `# pva-swarm V202 — rho(x)>0`
>
> `Plataforma validacion adversarial distribuida — FastAPI + SQLite + HTMX.`
>
> `- POST /api/papers publica paper con codigo/datos`
> `- Cualquier usuario se registra como validador`
> `- Intenta contraejemplo: fail_refutation ↑ credibilidad, counterexample ↓`
> `- Tablero publico estado validacion`
>
> ```bash
> `pip install -r requirements.txt`
> `uvicorn app:app --reload --port 8000`
> `# abre http://localhost:8000`
> ```
>
> `Deploy: Fly.io free tier o Oracle 4 OCPU forever (que ya tienes).`
>
> `Parte de PVA ecosistema — Bloque 3 validacion adversarial — referencia Pilcrow Vivum.`

## Qué dice el código (`app.py`, íntegro en la lectura)

- Cabecera: `pva-swarm V202 flexible — sin pydantic — stdlib fallback para py3.14`.
- Importa solo stdlib: `os, sys, json, pathlib`, `http.server`, `urllib.parse`. No importa `fastapi`, `uvicorn`, `sqlite3` ni `requests`.
- La "base de datos" es `papers.json` en disco (`DB = pathlib.Path("papers.json")`; si no existe, escribe `"[]"`).
- `GET /` y `GET /api` devuelven una cadena HTML de una línea: `<h1>pva-swarm V202 flexible rho>0</h1><p>GET /api/papers</p><p>POST /api/papers doi=...&title=...</p>`.
- `GET /api/papers` devuelve `{"papers": [...], "rho": ">0", "mode": "stdlib-flex"}`.
- `POST /api/papers` añade `{"doi": ..., "title": ...}` a `papers.json` y devuelve `{"registered": {...}, "total": N, "rho": ">0"}`. Acepta formulario y JSON. Sin validación, sin deduplicación, sin autenticación.
- No hay registro de validadores, ni lógica de `fail_refutation` / `counterexample`, ni tablero.
- `run(port=8000)` levanta `HTTPServer` en `0.0.0.0`. Esa es la única vía de arranque que existe en el código.

## Qué dice `papers.json` (íntegro)

```json
[
  {"doi":"10.5281/zenodo.7525945","title":"Credito inmutable rho>0"},
  {"doi":"10.5281/zenodo.8432022","title":"MAPA CONTRASTABLE TEORIA EMPIRICA Phi 9158.79 Ki banda [0.55,0.62] beta 0.5"}
]
```

2 papers, 195 B.

## Qué dicen los archivos de soporte (citas literales)

- `Dockerfile`: `FROM python:3.11-slim`, `RUN pip install -r requirements.txt`, `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`.
- `Makefile`: `repro` y `reproduce` hacen `python -c "import app; print('swarm ok')"`; `dev` hace `uvicorn app:app --reload`; `test` hace `python -m py_compile app.py`.
- `requirements.txt` (íntegro, salvo el comentario): `# flexible — sin pydantic — py3.14 OK` y `requests`.
- `.gitignore` (íntegro): `*.tar.gz`, `swarm.db`, `__pycache__/`.
- `.github/workflows/pva.yml` (íntegro): job `pva` en `ubuntu-latest`, en cada `push`: `pip install fastapi uvicorn python-multipart` y `python -m py_compile app.py`.

## NO SÉ

- **NO SÉ — si los 2 DOI de `papers.json` resuelven.** Están escritos en el archivo; no se verificó en esta minería si existen en Zenodo.
- **NO SÉ — qué es "Pilcrow Vivum".** El README lo cita como referencia; no aparece en ningún otro archivo del repo.
