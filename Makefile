update-trans:
	pybabel extract --mapping babel.cfg --output messages.pot .
	pybabel update --input-file messages.pot --output-dir translations/ --locale ja --domain messages

compile-trans:
	pybabel compile --directory translations/ --domain messages