#!/usr/bin/env python3
# pva-swarm V202 flexible — sin pydantic — stdlib fallback para py3.14
import os, sys, json, pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

DB = pathlib.Path("papers.json")
if not DB.exists():
    DB.write_text("[]")

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_GET(self):
        p = urlparse(self.path)
        if p.path in ("/","/api"):
            self.send_html("<h1>pva-swarm V202 flexible rho>0</h1><p>GET /api/papers</p><p>POST /api/papers doi=...&title=...</p>")
        elif p.path == "/api/papers":
            try: data = json.loads(DB.read_text())
            except: data=[]
            self.send_json({"papers": data, "rho": ">0", "mode": "stdlib-flex"})
        else:
            self.send_json({"error":"not found"},404)
    def do_POST(self):
        p = urlparse(self.path)
        length = int(self.headers.get('content-length',0))
        body = self.rfile.read(length).decode() if length else ""
        data = parse_qs(body)
        if self.headers.get('content-type','').startswith('application/json'):
            try:
                j = json.loads(body) if body else {}
                data = {k:[str(v)] for k,v in j.items()}
            except: pass
        def get(k,d=""): return (data.get(k,[d])[0] if data.get(k) else d)
        if p.path == "/api/papers":
            doi = get("doi"); title = get("title")
            try: papers = json.loads(DB.read_text())
            except: papers=[]
            papers.append({"doi": doi, "title": title})
            DB.write_text(json.dumps(papers, indent=2))
            self.send_json({"registered": {"doi": doi, "title": title}, "total": len(papers), "rho": ">0"})
        else:
            self.send_json({"error":"not found"},404)
    def send_json(self,obj,code=200):
        self.send_response(code); self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(json.dumps(obj, indent=2).encode())
    def send_html(self,html,code=200):
        self.send_response(code); self.send_header("Content-Type","text/html"); self.end_headers()
        self.wfile.write(html.encode())

def run(port=8000):
    print(f"[flex] pva-swarm stdlib :{port} rho>0")
    HTTPServer(("0.0.0.0",port), Handler).serve_forever()

if __name__ == "__main__":
    run(int(os.getenv("PORT","8000")))
