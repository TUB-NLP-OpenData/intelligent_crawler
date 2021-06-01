.PHONY: build clean

VENV=.env/bin/activate
VENV_SCRAPER=.envscraper/bin/activate

build: clean
	python3 -m venv .envscraper
	.envscraper/bin/pip3 install --upgrade pip setuptools wheel
	.envscraper/bin/pip3 install -r code/data_acquisition/scraper/requirements.txt

run-crawler:
	. $(VENV_SCRAPER); cd code/data_acquisition/scraper; scrapy crawl news-crawler

clean:
	rm -rf .env*/
	rm -rf .ve*/
