start: # start target executes unicorn server into docker container
	docker run --rm -d --name quiz -p 8082:8082 quiz_game

build: # build tag builds a image docker with fast api app
	docker build -t quiz_game .

stop: # stop target stop docker container
	docker stop quiz