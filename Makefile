.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: Test
run: 			## Run tests
	python -m unittest discover tests

.PHONY: Run
run: 			## Run the script
	python ig_non_followers_checker/main.py