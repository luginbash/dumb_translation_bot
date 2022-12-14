REGISTRY := ghcr.io
USER := luginbash
VERSION := $(shell git rev-parse --abbrev-ref HEAD)
NAME := dumb_translation_bot
IMAGE_NAME := $(REGISTRY)/$(USER)/$(NAME):$(VERSION)



all: image

requirements.txt:
	pipenv lock -r > requirements.txt

image: requirements.txt
	docker build -t $(IMAGE_NAME) .

clean:
	rm -f requirements.txt
