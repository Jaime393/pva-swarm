repro:
	python -c "import app; print('swarm ok')"

reproduce:
	python -c "import app; print('swarm ok')"

dev:
	uvicorn app:app --reload

test:
	python -m py_compile app.py
