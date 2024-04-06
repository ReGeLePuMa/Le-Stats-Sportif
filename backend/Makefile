IS_VENV_ACTIVE=false
IS_DOCKER_ACTIVE=false
ifdef VIRTUAL_ENV
	IS_VENV_ACTIVE:=true
endif

ifdef DOCKER
	IS_DOCKER_ACTIVE:=true
endif

enforce_venv:
ifeq ($(and $(IS_VENV_ACTIVE),$(not $(IS_DOCKER_ACTIVE))),false)
    $(error You must activate your virtual environment or use Docker. Exiting...)
endif

create_venv:
	python -m venv venv

install: enforce_venv requirements.txt
	python -m pip install -r requirements.txt

run_server: enforce_venv
	flask run

run_tests: enforce_venv
	python checker/checker.py

run_my_tests: enforce_venv
	python unittests/TestWebserver.py

build_docker:
	docker build -t webserver .

run_docker:
	docker run -p 5000:5000 webserver

clean_docker:
	docker rmi -f webserver
