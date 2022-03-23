#NAME ?= ecolley3

all: build run push

images:
	docker images | grep ecolley3

ps:
	docker ps -a | grep ecolley3

build:
	docker build -t ecolley3/iss-finder:Midterm .

run:
	docker run --name "iss-finder-c" -d -p 5009:5000 ecolley3/iss-finder:Midterm

push:
	docker push ecolley3/iss-finder:Midterm
