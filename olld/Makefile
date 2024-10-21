#//////////////////////////////////////////////////////////////
#//                                                          //
#//  Zola, 2024                                  		     //
#//  Created: 14, April, 2022                                //
#//  Modified: 19, October, 2024                             //
#//  file: -                                                 //
#//  -                                                       //
#//  Source:                                                 //
#//  OS: ALL                                                 //
#//  CPU: ALL                                                //
#//                                                          //
#//////////////////////////////////////////////////////////////

SERVER_DIRECTORY := satisfactory

ZOLA_EXEC := zola

.PHONY: build all
all: start

.PHONY: build
build:
	$(ZOLA_EXEC) build

.PHONY: serve
serve:
	$(ZOLA_EXEC) serve

.PHONY: run
run: serve

PHONY: docker-build
docker-build:
	docker build -t my_website:latest .
	docker run --rm -p 8000:80 my_website:latest
