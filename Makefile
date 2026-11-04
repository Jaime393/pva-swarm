repro:
	python3 app.py --snapshot

reproduce:
	python3 app.py --snapshot

dev:
	python3 app.py --serve

test:
	python3 -m unittest discover -s tests -v
