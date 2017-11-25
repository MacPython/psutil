PYTHON = python

download-unix-wheels:  ## download unix wheels
	$(PYTHON) scripts/download_unix_wheels.py

help: ## display callable targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
