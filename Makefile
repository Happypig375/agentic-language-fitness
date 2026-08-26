.PHONY: install test doctor validate pilot clean

install:
	python -m pip install -e .

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

doctor:
	python scripts/alf.py doctor --strict

validate:
	python scripts/alf.py validate

pilot:
	python scripts/alf.py matrix --agent scripted --output results/pilot
	python scripts/alf.py summarize results/pilot

clean:
	rm -rf results .venv src/*.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
