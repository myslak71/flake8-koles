black:  ## run black formatter
	black flake8_koles -S

black-check:  ## run black check
	black flake8_koles -S --check

coverage_html:  ## create html coverage report and open it in the default browser
	coverage html
	xdg-open htmlcov/index.html

flake8:  ## run flake8
	flake8 flake8_koles/ --ignore=KOL001,KOL002

isort: ## run isort
	isort flake8_koles -rc

isort-check: ## run isort check
	isort flake8_koles -rc

lint: flake8 yamllint black-check isort-check mypy   # run all linters

mypy:  ## run mypy
	mypy flake8_koles

safety:  ## run safety check
	safety check -r requirements-dev.txt

unittests:  ## run pytest with coverage and -s flag for debugging
	pytest --cov=flake8_koles.checker tests/ --cov-branch -s

yamllint:  # run yamllint
	yamllint .


