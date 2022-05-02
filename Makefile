.PHONY: build_dev_images bundled


bundled: build_dev_images
	docker-compose up

bundled_dev: build_dev_images opensearch opensearch_dashboards postgres setup

bundled_off:
	docker-compose down

build_dev_images:
	docker build -t swiple-api ./backend/
	docker build -t swiple-ui ./frontend/

swiple_ui_install:
	npm install --preifx ./frontend/

swiple_ui_dev:
	npm start --preifx ./frontend/

swiple_api_dev:
	python3 ./backend/main.py

opensearch:
	docker-compose up -d opensearch-node1

postgres:
	docker-compose up -d postgres

opensearch_dashboards:
	docker-compose up -d opensearch-dashboards

setup:
	docker-compose up -d setup

install_pip_dep:
	pip install -r ./backend/requirements.txt


deploy:
	#aws cloudformation update-stack --stack-name swiple-certificate --template-body file://.github/templates/certificate.yaml
	#aws cloudformation update-stack --stack-name swiple-website --template-body file://.github/templates/website.yaml
	aws cloudformation update-stack --stack-name github-oidc-provider --template-body file://./github-actions-oidc-provider.yaml --capabilities CAPABILITY_NAMED_IAM

sync:
	aws s3 sync ./docs/build/ s3://swiple.io/
	#aws s3 sync ./docs/build/ s3://www.swiple.io/