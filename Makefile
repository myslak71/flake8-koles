coverage_html:  ## create html coverage report and open it in the default browser
	coverage html
	xdg-open htmlcov/index.html

flake8:  ## run flake8
	flake8 flake8_koles/

lint: mypy flake8 yamllint  # run all linters

mypy:  ## run mypy
	mypy flake8_koles

safety:  ## run safety check
	safety check -r requirements-dev.txt

unittests:  ## run pytest with coverage and -s flag for debugging
	pytest --cov=flake8_koles.checker tests/ --cov-branch

yamllint:  # run yamllint
	yamllint .


