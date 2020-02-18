ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

DATABASE_DOCKER_NAME="docapi-postgres"
TIKA_DOCKER_NAME="docapi-tika"
BACKEND_DOCKER_NAME="docapi-backend"
FRONTEND_DOCKER_NAME="docapi-frontend"
NGINX_DOCKER_NAME="docapi-nginx"

DOCAPI_DEV_DB="postgres://postgres:password@$(DATABASE_DOCKER_NAME)/dev"
DOCAPI_TEST_DB="postgres://postgres:password@$(DATABASE_DOCKER_NAME)/test"
DOCAPI_PROD_DB="postgres://postgres:password@$(DATABASE_DOCKER_NAME)/postgres"
DOCAPI_SECRET_KEY="123456"
DOCAPI_TIKA_URL="http://$(TIKA_DOCKER_NAME)"

.PHONY: kubernetes

build: frontend_build backend_build_push kubernetes

frontend_pull_image:
	docker pull node:10

frontend_install: frontend_pull_image
	docker run -it --rm  --name $(FRONTEND_DOCKER_NAME) -v $(ROOT_DIR)/doc_frontend:/app -w /app node:10 npm install

frontend_dev: frontend_install
	docker run -it --rm  --name $(FRONTEND_DOCKER_NAME) -v $(ROOT_DIR)/doc_frontend:/app -w /app node:10 npm run dev

frontend_build: frontend_install
	docker run -it --rm  --name $(FRONTEND_DOCKER_NAME) -v $(ROOT_DIR)/doc_frontend:/app -w /app node:10 npm run build
	mkdir -p $(ROOT_DIR)/storage/frontend/
	cp -a $(ROOT_DIR)/doc_frontend/public/* $(ROOT_DIR)/storage/frontend/

tika_pull_image:
	docker pull logicalspark/docker-tikaserver

tika_run: tika_pull_image
	docker run -it --rm --name $(TIKA_DOCKER_NAME) logicalspark/docker-tikaserver

postgres_pull_image:
	docker pull postgres:10-alpine

postgres_database: postgres_pull_image
	docker run -it --rm --name $(DATABASE_DOCKER_NAME)\
		-v $(ROOT_DIR)/storage/database:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD=password -p 5432:5432 \
		postgres:10-alpine

postgres_database_create: postgres_pull_image
	docker run -it --rm --name $(DATABASE_DOCKER_NAME)\
		-v $(ROOT_DIR)/storage/database:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD=password -p 5432:5432 \
		postgres:10-alpine
		psql -c "CREATE DATABASE dev; CREATE DATABASE test; CREATE DATABASE prod";

backend_build_image:
	docker build -t euroska/test $(ROOT_DIR)/doc_api/

backend_build_push: backend_build_image
	docker push euroska/test

backend_run_dev_image:
	docker run -it --rm  --name $(BACKEND_DOCKER_NAME) -p 5000:5000 \
		--link $(DATABASE_DOCKER_NAME):$(DATABASE_DOCKER_NAME) \
		--link $(TIKA_DOCKER_NAME):$(TIKA_DOCKER_NAME) \
		-e DOCAPI_TIKA_URL=http://$(TIKA_DOCKER_NAME):9998 \
		-e DOCAPI_DEV_DB=$(DOCAPI_DEV_DB)\
		euroska/test /bin/bash -c \
		"python manage.py db upgrade head && python manage.py run"

backend_run_test_image:
	docker run -it --rm  --name $(BACKEND_DOCKER_NAME) -p 5000:5000 \
		--link $(DATABASE_DOCKER_NAME):$(DATABASE_DOCKER_NAME) \
		doc_api/backend /bin/bash -c \
		"python manage.py test && python manage run"

nginx_pull_image:
	docker pull nginx

nginx_run: # nginx_pull_image
	docker run -it --rm --name $(NGINX_DOCKER_NAME) -p 8080:80 \
	--link $(BACKEND_DOCKER_NAME):$(BACKEND_DOCKER_NAME) \
	-v $(ROOT_DIR)/storage/nginx:/etc/nginx/conf.d \
	-v $(ROOT_DIR)/storage/frontend/:/var/www \
	-v /tmp/client_body/:/var/lib/nginx/tmp/client_body/ \
	-v /tmp:/var/log/nginx \
	nginx

kubernetes:
	kubectl apply -f  kubernetes/docapi-postgres.yaml
	kubectl apply -f  kubernetes/docapi-tika.yaml
	kubectl apply -f  kubernetes/docapi-backend.yaml
	kubectl apply -f  kubernetes/docapi-nginx.yaml
