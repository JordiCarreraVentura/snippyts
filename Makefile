test:
	source env/snippyts/bin/activate ;
	pytest tests ;
	python -m src.snippyts.__init__ ;
	python -m src.snippyts.preprocessing ;

all: test