.PHONY: test

default:
	python3 -i -c 'import music_dl; print("music-dl %s\n>>> import music_dl" % music_dl.__version__)'

test:
	python3 setup.py test

coverage:
	py.test --cov-report term --cov-report html --cov=music_dl tests

flake8:
	flake8 --ignore=E501,F401,W503 music_dl

clean:
	rm -fr build dist .egg pymusic_dl.egg-info
	find . | grep __pycache__ | xargs rm -fr
	find . | grep .pyc | xargs rm -f

install:
	python3 setup.py install

publish:
	pip3 install 'twine>=1.5.0'
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build .egg requests.egg-info
