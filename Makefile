.PHONY: default clean install publish

default:
	python -i -c 'import music_dl; print("music-dl %s\n>>> import music_dl" % music_dl.__version__)'

flake8:
	flake8 --ignore=E501,F401,W503 music_dl

clean:
	rm -fr build dist .egg pymusic_dl.egg-info
	find . | grep __pycache__ | xargs rm -fr
	find . | grep .pyc | xargs rm -f

install:
	python setup.py install

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr dist .egg requests.egg-info
