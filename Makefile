include .env
export $(shell sed 's/=.*//' .env)
run:
	python3 redditparser ${params}
