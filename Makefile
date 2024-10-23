install:
	.env/bin/pip install -r requirements.txt

clean:
	find . -name '__pycache__' -exec rm -rf {} +

create_env:
	python3 -m venv .env

# init database
init-db:
	.env/bin/python create_db.py

# run server
run:
	.env/bin/uvicorn app.main:app --reload

# run env & server
start:
	bash start.sh

remove-db:
	rm -f ./tasks.db

setup: create_env install init-db run
