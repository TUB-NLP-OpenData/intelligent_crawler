.PHONY: build clean

VENV=.env/bin/activate

build: clean
	python3 -m venv .env
	.env/bin/pip3 install -r requirements.txt

run:
	. $(VENV); python generate_testbed_definition.py

clean:
	rm -rf .env/
	rm -rf .ve*/
