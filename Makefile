run:
	python run.py
lint: test
	pylint gbf_bot	
test:
	pytest -v
