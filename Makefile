update-trans:
	pybabel extract --mapping babel.cfg --output messages.pot .
	pybabel update --input-file messages.pot --output-dir translations/ --locale ja --domain messages

compile-trans:
	pybabel compile --directory translations/ --domain messages

appengine-deploy:
	# Note: If you are on OS X, and you are using homebrew python,
	# you are going to get a weird error.
	pip install -r requirements.txt -t lib