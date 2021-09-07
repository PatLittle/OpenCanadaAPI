openapi-fr.json openapi-en.json : openapi.yaml Makefile splityaml.py schemas/*
	python3 splityaml.py openapi.yaml fr openapi-fr.json
	python3 splityaml.py openapi.yaml en openapi-en.json

	openapi-spec-validator openapi-en.json
	openapi-spec-validator openapi-fr.json

schema :
	python3 dataset_schema.py fr > schemas/dataset-fr.json
	python3 dataset_schema.py en > schemas/dataset-en.json
