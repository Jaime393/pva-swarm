# pva-swarm

Registro local de papers declarados, con IDs por contenido, snapshot y HTTP opcional de loopback. No implementa validación adversarial distribuida, SQLite, FastAPI ni autenticación de validadores.

```bash
python3 app.py --snapshot
python3 app.py --serve
python3 app.py --serve --allow-write --db papers.json
python3 -m unittest discover -s tests -v
```

La ejecución predeterminada solo lee. El servidor escucha en `127.0.0.1`, es de solo lectura salvo opt-in y acepta JSON acotado en `POST /api/papers`; el código no se despliega en esta revisión.

Los registros permanecen `reported_unverified`. Un DOI con sintaxis plausible no fue resuelto, el registro local no implica publicación remota y un alta no aumenta una métrica de credibilidad.

Las altas idénticas son idempotentes y las escrituras usan reemplazo atómico. Un archivo corrupto se bloquea: nunca se sustituye silenciosamente por una lista vacía. El lock solo coordina este proceso, no varios servidores distribuidos.
