
help: ## help: Show this help message.
	@echo "usage: make [target] ..."
	@echo ""
	@echo "targets:"
	@grep -Eh '^.+:(\w+)?\ ##\ .+' ${MAKEFILE_LIST} | cut -d ' ' -f '3-' | column -t -s ':'

clean: ## clean: Cleanup.
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	rm -Rf htmlcov/
	rm -Rf .coverage

coverage: ## coverage: Coverage.
	CONFIG_FILE=config/test.ini py.test --cov=sample --cov-report term-missing

coverage-html: ## coverage-html: Coverage with HTML report.
	CONFIG_FILE=config/test.ini py.test --cov=sample --cov-report html
	xdg-open htmlcov/index.html &

integration: ## integration: Run continuous integration.
	docker -f docker/api/Dockerfile
	docker -f docker/worker/Dockerfile
	docker -f docker/tests/Dockerfile

	docker-compose up integration

test:  ## Run tests.
	make unit
	make coverage

unit: ## unit: Unit tests.
	CONFIG_FILE=config/test.ini py.test
