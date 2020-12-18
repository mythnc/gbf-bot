run:
	python run.py
lint: test
	pylint gbf_bot	
test:
	pytest -v
black:
	black -l 120 gbf_bot/ tests/
