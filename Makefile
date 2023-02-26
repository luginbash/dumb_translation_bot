REGISTRY := ghcr.io
USER := ${GITHUB_ACTOR}
VERSION := $(shell git describe --tags --abbrev=0)
NAME := dumb_translation_bot
IMAGE_NAME := $(REGISTRY)/$(USER)/$(NAME):$(VERSION)

all: image

.PHONY: dist
dist:
	poetry build

image:
	docker build -t $(IMAGE_NAME) .

.PHONY: push
push:
	docker push $(IMAGE_NAME)
	# additionally push dockerhub
	docker tag $(IMAGE_NAME) $(USER)/$(NAME):latest
	docker push $(USER)/$(NAME):latest

.PHONY: clean
clean:
	rm dist/*
