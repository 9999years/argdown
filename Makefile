clean:
	rm -rf dist/* &1>/dev/null
	rm -rf build/* &1>/dev/null
upload: clean
	python setup.py bdist_wheel
	twine upload --config-file ~/.pypirc dist/*
test:
	pytest
