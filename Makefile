install:
	pip install -r requirements.txt

clean:
	find . -name '__pycache__' -exec rm -rf {} +

create_env:
	python3 -m venv .env

# init database
init-db:
	python create_db.py

# run server
run:
	uvicorn app.main:app --reload

# run env & server
start:
	bash start.sh

# Команда для очищення бази даних (можливо вам знадобиться для тестування)
remove-db:
	rm -f ./tasks.db

# Команда для створення та запуску всього проекту з нуля
setup: install init-db run
