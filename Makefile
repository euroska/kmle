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

frontend_pull_image:
	docker pull node:10

frontend_install: frontend_pull_image
	docker run -it --rm  --name $(FRONTEND_DOCKER_NAME) -v $(ROOT_DIR)/doc_frontend:/app -w /app node:10 npm install

frontend_dev: frontend_install
	docker run -it --rm  --name $(FRONTEND_DOCKER_NAME) -v $(ROOT_DIR)/doc_frontend:/app -w /app node:10 npm run dev

frontend_build: frontend_install
	docker run -it --rm  --name $(FRONTEND_DOCKER_NAME) -v $(ROOT_DIR)/doc_frontend:/app -w /app node:10 npm run build
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
		-e POSTGRES_PASSWORD=password\
		postgres:10-alpine

backend_build_image:
	docker build -t doc_api/backend $(ROOT_DIR)/doc_api/

backend_run_dev_image:
	docker run -it --rm  --name $(BACKEND_DOCKER_NAME) -p 5000:5000 \
		--link $(DATABASE_DOCKER_NAME):$(DATABASE_DOCKER_NAME) \
		--link $(TIKA_DOCKER_NAME):$(TIKA_DOCKER_NAME) \
		-e DOCAPI_TIKA_URL=http://$(TIKA_DOCKER_NAME):9998 \
		-e DOCAPI_DEV_DB=$(DOCAPI_DEV_DB)\
		doc_api/backend /bin/bash -c \
		"python manage.py db upgrade head && python manage.py run"

backend_run_test_image:
	docker run -it --rm  --name $(BACKEND_DOCKER_NAME) -p 5000:5000 \
		--link $(DATABASE_DOCKER_NAME):$(DATABASE_DOCKER_NAME) \
		-w /app doc_api/backend /bin/bash -c \
		"python manage.py test && python manage run"

nginx_pull_image:
	docker pull matriphe/alpine-nginx

nginx_run:
	docker run -it --rm --name $(NGINX_DOCKER_NAME) -p 8080:80 \
	--link $(BACKEND_DOCKER_NAME):$(BACKEND_DOCKER_NAME) \
	-v $(ROOT_DIR)/storage/nginx:/etc/nginx/conf.d \
	-v $(ROOT_DIR)/storage/frontend/:/var/www \
	-v /tmp:/var/log/nginx \
	matriphe/alpine-nginx
