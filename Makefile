VERSION := $(shell awk '/version/ {print substr($$3, 2, length($$3) - 2)}' pyproject.toml)
PYINT := env/snippyts/bin/python

test:
	$(PYINT) -m pytest tests/* ;
	$(PYINT) -m src.snippyts.__init__ ;
	$(PYINT) -m src.snippyts.preprocessing ;

build:
	$(PYINT) -m build

push:
	$(PYINT) -m twine upload --repository pypi dist/*$(VERSION)*  ;

release: build push
