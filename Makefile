VERSION := $(shell awk '/version/ {print substr($$3, 2, length($$3) - 2)}' pyproject.toml)

test:
	source env/snippyts/bin/activate ;
	pytest tests ;
	python -m src.snippyts.__init__ ;
	python -m src.snippyts.preprocessing ;

build:
	source env/snippyts/bin/activate ;
	python -m build ;
	version_number=`sh get_version_number.sh` ;
	python -m twine upload --repository pypi dist/*$(VERSION)*  ;

all: test