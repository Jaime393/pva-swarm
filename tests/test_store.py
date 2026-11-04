import importlib.util
import json
from pathlib import Path
import tempfile
import threading
from http.server import HTTPServer
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("swarm", ROOT / "app.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "papers.json"
        self.store = MODULE.Store(self.path)
        self.paper = {"doi": "10.1234/example", "title": "Reported, not validated"}

    def test_missing_snapshot_does_not_create(self):
        r = self.store.snapshot()
        self.assertFalse(r["store_present"])
        self.assertFalse(self.path.exists())

    def test_add_and_idempotence(self):
        self.assertTrue(self.store.add(self.paper)["created"])
        self.assertFalse(self.store.add(self.paper)["created"])
        r = self.store.snapshot()
        self.assertEqual(r["count"], 1)
        self.assertFalse(r["distributed_validation_verified"])
        self.assertEqual(r["papers"][0]["evidence_state"], "reported_unverified")

    def test_corruption_is_not_reset(self):
        self.path.write_text("{bad")
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.store.add(self.paper)
        self.assertEqual(self.path.read_bytes(), before)

    def test_legacy_is_read_without_rewrite(self):
        self.path.write_text(json.dumps([self.paper]))
        before = self.path.read_bytes()
        self.assertEqual(self.store.snapshot()["count"], 1)
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_paper_and_id(self):
        for p in ({"doi": "bad", "title": "x"}, {**self.paper, "record_id": "forged"}):
            with self.assertRaises(ValueError):
                self.store.add(p)

    def server(self, writable):
        server = HTTPServer(("127.0.0.1", 0), MODULE.make_handler(self.store, writable))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_port}/api/papers"

    def test_http_readonly(self):
        url = self.server(False)
        with self.assertRaises(HTTPError) as error:
            urlopen(Request(url, data=json.dumps(self.paper).encode(),
                            headers={"Content-Type": "application/json"}), timeout=3)
        self.assertEqual(error.exception.code, 403)
        error.exception.close()
        self.assertFalse(self.path.exists())

    def test_http_local_opt_in_and_bad_json(self):
        url = self.server(True)
        with urlopen(Request(url, data=json.dumps(self.paper).encode(),
                             headers={"Content-Type": "application/json"}), timeout=3) as response:
            self.assertTrue(json.load(response)["created"])
        with urlopen(url, timeout=3) as response:
            self.assertEqual(json.load(response)["count"], 1)
        with self.assertRaises(HTTPError) as error:
            urlopen(Request(url, data=b"{invalid", headers={"Content-Type": "application/json"}), timeout=3)
        self.assertEqual(error.exception.code, 400)
        error.exception.close()
        self.assertEqual(self.store.snapshot()["count"], 1)


if __name__ == "__main__":
    unittest.main()
