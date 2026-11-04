#!/usr/bin/env python3
"""Local reported-paper registry, not distributed adversarial validation."""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from urllib.parse import urlparse

DB = Path(__file__).resolve().parent / "papers.json"
MAX_BODY = 8192


def normalize(item):
    if not isinstance(item, dict):
        raise ValueError("paper must be an object")
    doi, title = item.get("doi"), item.get("title")
    if not isinstance(doi, str) or not re.fullmatch(r"10\.\d{4,9}/\S{1,240}", doi):
        raise ValueError("DOI syntax required, not resolution proof")
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 512:
        raise ValueError("bounded nonempty title required")
    payload = {"doi": doi, "title": title.strip()}
    rid = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False,
                                   separators=(",", ":")).encode()).hexdigest()
    if "record_id" in item and item["record_id"] != "sha256:" + rid:
        raise ValueError("record ID mismatch")
    return {**payload, "record_id": "sha256:" + rid, "evidence_state": "reported_unverified"}


class Store:
    def __init__(self, path=DB):
        self.path = Path(path)
        self.lock = threading.RLock()

    def _read(self):
        if not self.path.exists():
            return [], None
        if self.path.is_symlink() or self.path.stat().st_size > 1024 * 1024:
            raise ValueError("bounded regular registry required")
        raw = self.path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        if isinstance(data, dict):
            if data.get("schema") != "pva.local-paper-registry/v1":
                raise ValueError("unsupported registry schema")
            data = data.get("papers")
        if not isinstance(data, list) or len(data) > 1000:
            raise ValueError("invalid registry; never reset corrupt storage silently")
        return [normalize(item) for item in data], raw

    def read(self):
        return self._read()[0]

    def snapshot(self):
        with self.lock:
            papers, raw = self._read()
            digest = hashlib.sha256(raw).hexdigest() if raw is not None else None
            return {"schema": "pva.local-paper-registry/v1", "papers": papers, "count": len(papers),
                    "store_present": raw is not None, "store_sha256": digest,
                    "distributed_validation_verified": False, "doi_resolution_checked": False}

    def add(self, item):
        normalized = normalize(item)
        with self.lock:
            papers = self.read()
            if any(p["record_id"] == normalized["record_id"] for p in papers):
                return {"created": False, "paper": normalized, "count": len(papers)}
            if len(papers) >= 1000:
                raise ValueError("registry limit reached")
            papers.append(normalized)
            content = json.dumps({"schema": "pva.local-paper-registry/v1", "papers": papers,
                                  "distributed_validation_verified": False},
                                 ensure_ascii=False, sort_keys=True, indent=2)
            if len(content.encode()) > 1024 * 1024:
                raise ValueError("registry size limit")
            temporary = None
            try:
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent,
                                                 delete=False) as out:
                    temporary = Path(out.name)
                    out.write(content)
                    out.flush()
                    os.fsync(out.fileno())
                os.replace(temporary, self.path)
            finally:
                if temporary and temporary.exists():
                    temporary.unlink()
            return {"created": True, "paper": normalized, "count": len(papers)}


def make_handler(store, allow_write=False):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send_json(self, obj, status=200):
            body = json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if urlparse(self.path).path not in {"/", "/api", "/api/papers"}:
                return self.send_json({"error": "not_found"}, 404)
            try:
                self.send_json(store.snapshot())
            except (OSError, ValueError, TypeError):
                self.send_json({"error": "registry_unreadable_no_reset_performed"}, 500)

        def do_POST(self):
            if urlparse(self.path).path != "/api/papers":
                return self.send_json({"error": "not_found"}, 404)
            if not allow_write:
                return self.send_json({"error": "read_only_mode"}, 403)
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= MAX_BODY:
                    return self.send_json({"error": "body_size_limit"}, 413)
                if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                    return self.send_json({"error": "json_required"}, 415)
                item = json.loads(self.rfile.read(size).decode("utf-8"))
                self.send_json(store.add(item))
            except (OSError, ValueError, TypeError):
                self.send_json({"error": "invalid_input_or_store_no_reset_performed"}, 400)
    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB)
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--allow-write", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    store = Store(args.db)
    if args.serve:
        HTTPServer(("127.0.0.1", args.port), make_handler(store, args.allow_write)).serve_forever()
        return 0
    try:
        print(json.dumps(store.snapshot(), ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, TypeError):
        parser.exit(2, "Blocked: registry unreadable; no reset or creation performed.\n")


if __name__ == "__main__":
    raise SystemExit(main())
