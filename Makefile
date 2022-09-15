#//////////////////////////////////////////////////////////////
#//   ____                                                   //
#//  | __ )  ___ _ __  ___ _   _ _ __   ___ _ __ _ __   ___  //
#//  |  _ \ / _ \ '_ \/ __| | | | '_ \ / _ \ '__| '_ \ / __| //
#//  | |_) |  __/ | | \__ \ |_| | |_) |  __/ |  | |_) | (__  //
#//  |____/ \___|_| |_|___/\__,_| .__/ \___|_|  | .__/ \___| //
#//                             |_|             |_|          //
#//////////////////////////////////////////////////////////////
#//                                                          //
#//  Website, 2022                                           //
#//  Created: 14, April, 2022                                //
#//  Modified: 28, August, 2022                              //
#//  file: -                                                 //
#//  -                                                       //
#//  Source:                                                 //
#//  OS: ALL                                                 //
#//  CPU: ALL                                                //
#//                                                          //
#//////////////////////////////////////////////////////////////

PYTHON := python

.PHONY: install
install:
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: run
run:
	$(PYTHON) wsgi.py

.PHONY: format
format:
	isort --multi-line=3 .
	black .

.PHONY: pygmentize
pygmentize:
	pygmentize -S emacs -f html -a .codehilite > project/static/css/style_code.css

.PHONY: lint
lint: 
	find . -name '*.py' -exec python -m pylint {} \;
	find . -name '*.py' -exec python -m flake8 --select=DUO {} \;

.PHONY: linkcheck
linkcheck:
	linkchecker http://127.0.0.1:5000

.PHONY: certificate
certificate:
	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=US/ST=France/L=Nantes/O=Bensuperpc/OU=Org/CN=localhost"

.PHONY: docker-start
docker-start:
	docker build -t flash_server .
	docker run -d -p 5000:5000 -v "$(shell pwd):/usr/src/app" --name flash_server flash_server

.PHONY: docker-stop
docker-stop:
	docker stop flash_server
	docker rm flash_server

.PHONY: docker-logs
docker-logs:
	docker logs flash_server

.PHONY: venv
venv:
	$(PYTHON) -m venv venv_dev
	@echo "Run: 'source ./venv_dev/bin/activate' to activate venv"
	@echo "Run: 'make install' to install the requirements INSIDE the venv"
	@echo "Run: 'deactivate ./venv_dev/bin/deactivate' to deactivate venv"

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '*.sqlite' -delete
