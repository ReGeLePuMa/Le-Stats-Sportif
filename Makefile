.PHONY: build clean

build:
	docker compose up

clean:
	docker rmi -f le-stats-sportif-frontend le-stats-sportif-backend