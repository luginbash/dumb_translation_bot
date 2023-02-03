REGISTRY := ghcr.io
USER := luginbash
VERSION := $(shell git rev-parse --abbrev-ref HEAD)
NAME := dumb_translation_bot
IMAGE_NAME := $(REGISTRY)/$(USER)/$(NAME):$(VERSION)



all: image

dist/*:
	poetry build

image:
	docker build -t $(IMAGE_NAME) .

clean:
	rm -f requirements.txt

.PHONY: push
push: image
	docker push $(IMAGE_NAME)
	# additionally push dockerhub
	docker tag $(IMAGE_NAME) $(USER)/$(NAME):latest
	docker push $(USER)/$(NAME):latest
