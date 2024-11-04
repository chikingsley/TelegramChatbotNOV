.PHONY: build run stop clean test setup

build:
	docker-compose -f docker/docker-compose.yml build

run:
	docker-compose -f docker/docker-compose.yml up

stop:
	docker-compose -f docker/docker-compose.yml down

clean:
	docker-compose -f docker/docker-compose.yml down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

setup:
	chmod +x setup.sh
	./setup.sh

logs:
	docker-compose -f docker/docker-compose.yml logs -f

shell:
	docker-compose -f docker/docker-compose.yml exec bot bash 