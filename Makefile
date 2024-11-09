prepare:
	python -m pip install -r requirements.txt
	python src/download_data.py

run-research:
	python src/research.py $(N)