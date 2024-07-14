.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: Run
run: 			## Run the script
	python ig_followers/main.py