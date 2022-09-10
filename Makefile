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

PYTHON := python3

.PHONY: install
install:
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: run
run:
	$(PYTHON) run.py

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

.PHONY: docker
docker:
	docker build -t flash_server .
	docker run -p 5000:5000 flash_server

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
