
help: ## help: Show this help message.
	@echo "usage: make [target] ..."
	@echo ""
	@echo "targets:"
	@grep -Eh '^.+:(\w+)?\ ##\ .+' ${MAKEFILE_LIST} | cut -d ' ' -f '3-' | column -t -s ':'

build: ## build: Build app containers.
	cp docker/api/* .
	docker build -t pyse2018-api .
	rm Dockerfile entrypoint*.sh
	cp docker/worker/* .
	docker build -t pyse2018-worker .
	rm Dockerfile entrypoint*.sh

clean: ## clean: Cleanup.
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	rm -Rf htmlcov/
	rm -Rf .coverage

coverage: ## coverage: Coverage.
	CONFIG_FILE=config/test.ini py.test --cov=sample --cov-report term-missing tests/unit

coverage-html: ## coverage-html: Coverage with HTML report.
	CONFIG_FILE=config/test.ini py.test --cov=sample --cov-report html tests/unit
	xdg-open htmlcov/index.html &

integration: ## integration: Run continuous integration.
	cp config/ci.ini docker-config.ini
	make build
	cp docker/ci/* .
	docker build -t pyse2018-ci .
	rm Dockerfile entrypoint*.sh docker-compose.yml
	docker-compose -f docker/ci/docker-compose.yml up integration

test:  ## Run tests.
	make unit
	make coverage

unit: ## unit: Unit tests.
	CONFIG_FILE=config/test.ini py.test tests/unit
