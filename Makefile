TARGET ?= ./main.py

run:
	poetry run python3 $(TARGET)
aboba:
	poetry run python3 ./gui/main.py	
	