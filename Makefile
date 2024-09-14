include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## clean the working dir	
	rm -rf cdk.out

init: ## cdk bootstrap
	pip install -r requirements.txt

plan: ## plan
	cdk diff

apply: ## apply terraform
	cdk deploy

version: ##	show version
	cdk --version

upgrade: ## upgrade CDK
	brew install aws-cdk
	pip install --upgrade -r requirements.txt
