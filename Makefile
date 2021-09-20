.PHONY: openapi-fr.json openapi-en.json
openapi-fr.json openapi-en.json: openapi.yaml Makefile splityaml.py schemas/*
	python3 splityaml.py openapi.yaml fr openapi-fr.json
	python3 splityaml.py openapi.yaml en openapi-en.json

	openapi-spec-validator openapi-en.json
	openapi-spec-validator openapi-fr.json


.PHONY: schema
schema:
	python3 dataset_schema.py fr > schemas/dataset-fr.json
	python3 dataset_schema.py en > schemas/dataset-en.json
	python3 resource_multipart_schema.py fr > schemas/resource-multipart-fr.json
	python3 resource_multipart_schema.py en > schemas/resource-multipart-en.json
