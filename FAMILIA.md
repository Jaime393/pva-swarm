# FAMILIA — pva-swarm

Repo: `Jaime393/pva-swarm`, rama `main`.
Leído en vivo: 2026-11-09 ~07:40 -05.

## Ecosistema PVA

El README ubica el repo así: `Parte de PVA ecosistema — Bloque 3 validacion adversarial`.

Hermanos PVA (todos `Jaime393`, todos con README V202 y marca `rho(x)>0`):

| Repo | Bloque / papel según su README | Estado |
|---|---|---|
| `pva-docker-template` | Plantilla de reproducibilidad (Docker + Make) | Minado, ola 4 tanda 1 (2026-11-09) |
| `pva-ledger` | Registro inmutable (Arweave + Zenodo DOI) | Pendiente de minar (ola 4 tanda 2) |
| `pva-lean-bridge` | Puente LaTeX → Lean 4 | Pendiente de minar (ola 4 tanda 2) |
| `pva-orchestrator` | Orquestador (encadena lint + docker + lean + ledger + swarm con `pva.yml`) | Pendiente de minar (ola 4 tanda 2) |
| `pva-lint` | Linter PVA (score 0-1) | Pendiente de minar (ola 4 tanda 3) |
| `pva-api` | API flexible (FastAPI o stdlib según entorno) | Pendiente de minar (ola 4 tanda 3) |
| `pva-swarm` | **Este repo — Bloque 3, validación adversarial** | Minado aquí |

## Cruces con los hermanos (solo SÉ)

- **El orquestador lo describe como FastAPI.** El README de `pva-orchestrator` (leído en el muestreo del 2026-11-09 ~07:03 -05) lista su MVP como `pva-swarm FastAPI`. Contra el código de este repo, eso es falso: `app.py` es stdlib sin FastAPI. La descripción del hermano no coincide con el código.
- **Los 2 DOI se repiten en la familia.** `10.5281/zenodo.7525945` y `10.5281/zenodo.8432022` son los 2 papers de `papers.json`; los mensajes de commit de este repo los llaman "2 creditos inmutables" y el segundo es el "MAPA CONTRASTABLE TEORIA EMPIRICA". El `pva-ledger` (según su README) es el que registraría ese tipo de créditos — el cruce entre ambos repos es temático, no de código: ningún archivo de este repo importa ni cita a `pva-ledger`.
- **El patrón V202 se repite.** Los 7 repos llevan la marca V202 y `rho(x)>0`; los commits de este repo son todos del 2026-09-10, igual que los heads de los 7 pva (todos 2026-09-10 según el censo de commits del 2026-11-09 ~07:03 -05). Un solo día de construcción para la familia entera.
- **`pva.yml` del orquestador.** El `pva-orchestrator` promete encadenar `pva.yml`; este repo tiene su propio `.github/workflows/pva.yml` (CI, no orquestación). No hay evidencia en este repo de que el orquestador lo haya ejecutado jamás.

## Fuera de PVA

- El README cita "referencia Pilcrow Vivum" sin más. NO SÉ qué es; no aparece en ningún archivo del repo ni de los hermanos leídos en el muestreo.
- Ningún archivo cita repos MIU fuera de PVA (ni `miu-agents`, ni `FranBot`, ni `MIU_V14`).

## NO SÉ

- **NO SÉ — si algún hermano consume realmente a este repo.** Ningún archivo de este repo registra consumidores; los hermanos solo lo nombran en sus README.
- **NO SÉ — qué es "Pilcrow Vivum".**
