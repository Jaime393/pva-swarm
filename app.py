#!/usr/bin/env python3
# pva-swarm V202 — Validacion adversarial distribuida — rho(x)>0
# FastAPI + SQLite + HTMX ligero — sin React pesado
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3, pathlib, json, datetime

DB = "swarm.db"
app = FastAPI(title="pva-swarm")

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS papers (id INTEGER PRIMARY KEY, doi TEXT, hash TEXT, title TEXT, cred REAL DEFAULT 0.5, created TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS validations (id INTEGER PRIMARY KEY, paper_id INT, validator TEXT, result TEXT, note TEXT, created TEXT)")
    con.commit()

init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    con = sqlite3.connect(DB)
    papers = con.execute("SELECT * FROM papers ORDER BY id DESC").fetchall()
    html = "<h1>pva-swarm V202 — rho(x)>0 — Validacion adversarial</h1><a href='/docs'>API</a><hr>"
    html += "<form method='post' action='/api/papers'><input name='doi' placeholder='DOI'><input name='title' placeholder='Titulo'><button>Publicar paper</button></form><hr>"
    for p in papers:
        html += f"<div><b>{p[3]}</b> DOI:{p[1]} cred:{p[4]} <form method='post' action='/api/validate'><input type='hidden' name='paper_id' value='{p[0]}'><input name='validator' placeholder='validador'><select name='result'><option>fail_refutation</option><option>counterexample</option></select><input name='note' placeholder='nota'><button>Validar</button></form></div><hr>"
    return html

@app.post("/api/papers")
def publish_paper(doi: str = Form(...), title: str = Form("")):
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO papers (doi, hash, title, cred, created) VALUES (?,?,?,?,?)", (doi, "sha256", title, 0.5, datetime.datetime.now().isoformat()))
    con.commit()
    # bayes: fail refutation -> cred up, counterexample -> cred down
    return {"ok": True, "doi": doi}

@app.post("/api/validate")
def validate(paper_id: int = Form(...), validator: str = Form(...), result: str = Form(...), note: str = Form("")):
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO validations (paper_id, validator, result, note, created) VALUES (?,?,?,?,?)", (paper_id, validator, result, note, datetime.datetime.now().isoformat()))
    # update credibility
    cur = con.execute("SELECT cred FROM papers WHERE id=?", (paper_id,)).fetchone()
    if cur:
        cred = cur[0]
        if result == "fail_refutation":
            cred = min(0.9999, cred + 0.05)  # aumenta
        else:
            cred = max(0.0001, cred - 0.2)  # disminuye
        con.execute("UPDATE papers SET cred=? WHERE id=?", (cred, paper_id))
    con.commit()
    return {"ok": True, "new_cred": cred if cur else None}

@app.get("/api/papers")
def list_papers():
    con = sqlite3.connect(DB)
    papers = con.execute("SELECT * FROM papers").fetchall()
    return {"papers": papers}
