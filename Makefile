openapi-fr.json openapi-en.json : openapi.yaml
	python3 splityaml.py openapi.yaml fr openapi-fr.json
