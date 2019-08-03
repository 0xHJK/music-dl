.PHONY: test

ci:
	py.test --junitxml=report.xml

test:
	python3 setup.py test

coverage:
	py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=music_dl --junitxml=report.xml tests

flake8:
	flake8 --ignore=E501,F401,W503 music_dl

clean:
	rm -fr build dist .egg pymusic_dl.egg-info
	rm -fr *.mp3 .pytest_cache coverage.xml report.xml htmlcov
	find . | grep __pycache__ | xargs rm -fr
	find . | grep .pyc | xargs rm -f

install:
	python3 setup.py install

publish:
	pip3 install 'twine>=1.5.0'
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build .egg requests.egg-info
