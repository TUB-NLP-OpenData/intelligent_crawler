.PHONY: build clean

VENV=.venv/bin/activate

build: clean
	virtualenv .venv
	.venv/bin/pip install -r requirements.txt

run:
	. $(VENV); python generate_testbed_definition.py

clean:
	rm -rf .env/
