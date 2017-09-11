.PHONY: run shell test pep8 clean

run:
	manage runserver --reloader --debug

shell:
	manage shell

test: pep8
	FLASKPRESS_MODE=test py.test --cov=flaskpress -l --tb=short --maxfail=1 flaskpress/

pep8:
	@flake8 flaskpress --ignore=F403,E501,E731 --exclude=migrations

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
