.PHONY: build_dev_images up

up: build_dev_images
	docker compose up

bundled_dev: build_dev_images opensearch opensearch_dashboards postgres setup

down:
	docker compose down

build_dev_images:
	docker build -t swiple-api ./backend/
	docker build -t swiple-ui ./frontend/

swiple_api_dev_install:
	cd ./backend && poetry install --with postgres,redshift,mysql,trino,athena,snowflake,aws-secrets,gcp,azure-secrets,dev && cd ..

swiple_ui_install:
	npm install --preifx ./frontend/

swiple_ui_dev:
	npm start --preifx ./frontend/

swiple_api_dev:
	python3 ./backend/main.py

swiple_api_test:
	cd ./backend && PRODUCTION='False' \
	SECRET_KEY=DphzRvbm3ICHH2t1_Xj5NTUVEpqjz5KOHxuF77udndQ= \
	ADMIN_EMAIL=admin@email.com \
	ADMIN_PASSWORD=admin \
	poetry run pytest --cov app/ --cov-report=xml && cd ..

demo:
	docker compose run demo

opensearch:
	docker compose up -d opensearch-node1

postgres:
	docker compose up -d postgres

opensearch_dashboards:
	docker compose up -d opensearch-dashboards

setup:
	docker compose up -d setup

push_swiple_api_to_aws_ecr:
	# Prerequisites: Repository has been created in AWS ECR
	# Example: make push_swiple_api_to_aws_ecr AWS_ACCOUNT_ID=012345678910 REPOSITORY=swiple-api TAG=latest REGION=us-east-1
	docker build -t $(REPOSITORY):$(TAG) ./backend/
	$(eval IMAGE_ID=$(shell sh -c 'docker images --filter=reference=$(REPOSITORY):$(TAG) --format "{{.ID}}"'))
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
	docker tag $(IMAGE_ID) $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPOSITORY)
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPOSITORY):$(TAG)

push_swiple_ui_to_aws_ecr:
	# Prerequisites: Repository has been created in AWS ECR
	# Example: make push_swiple_ui_to_aws_ecr AWS_ACCOUNT_ID=012345678910 REPOSITORY=swiple-ui TAG=latest REGION=us-east-1
	docker build -t $(REPOSITORY):$(TAG) -f ./frontend/Dockerfile.prod ./frontend
	$(eval IMAGE_ID=$(shell sh -c 'docker images --filter=reference=$(REPOSITORY):$(TAG) --format "{{.ID}}"'))
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
	docker tag $(IMAGE_ID) $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPOSITORY)
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPOSITORY):$(TAG)
