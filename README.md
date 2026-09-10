# pva-swarm V202 — rho(x)>0

Plataforma validacion adversarial distribuida — FastAPI + SQLite + HTMX.

- POST /api/papers publica paper con codigo/datos
- Cualquier usuario se registra como validador
- Intenta contraejemplo: fail_refutation ↑ credibilidad, counterexample ↓
- Tablero publico estado validacion

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
# abre http://localhost:8000
```

Deploy: Fly.io free tier o Oracle 4 OCPU forever (que ya tienes).

Parte de PVA ecosistema — Bloque 3 validacion adversarial — referencia Pilcrow Vivum.
