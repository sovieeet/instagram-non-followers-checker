.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: Run
run: 			## Run the script
	python ig_non_followers_checker/main.py