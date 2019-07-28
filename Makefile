mypy:  ## run mypy
	mypy flake8_koles

flake8:  ## run flake8
	flake8 flake8_koles/

yamllint:  # run yamllint
	yamllint .

lint: mypy flake8 yamllint  # run all linters

unittests:  ## run pytest with coverage and -s flag for debugging
	pytest --cov=flake8_koles.checker tests/ --cov-branch

coverage_report:  ## display pytest coverage report
	coverage report

coverage_html:  ## create html coverage report and open it in the default browser
	coverage html
	xdg-open htmlcov/index.html



