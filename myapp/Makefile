## The Makefile includes instructions on environment setup and lint tests
# Create and activate a virtual environment
# Install dependencies in requirements.txt
# Dockerfile should pass hadolint
# app.py should pass pylint
# (Optional) Build a simple integration test

setup:
	# Create python virtualenv & source it
	# source ~/.wegapp/bin/activate
	python3 -m venv ~/.wegapp
	# windows
	 C:\Users\lnguo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\virtualenv venvironment
     venvironment\Scripts\activate
install:
	# This should be run from inside a virtualenv
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	# Additional, optional, tests could go here
	#python -m pytest -vv --cov=myrepolib tests/*.py
	#python -m pytest --nbval notebook.ipynb

lint:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# This is linter for Dockerfiles
	wget -O ./hadolint https://github.com/hadolint/hadolint/releases/download/v2.6.0/hadolint-Linux-x86_64 &&\
    chmod +x ./hadolint
	hadolint Dockerfile
	# This is a linter for Python source code linter: https://www.pylint.org/
	# This should be run from inside a virtualenv
	pylint --disable=R,C,W1203,W0703 src/app.py

all: install lint test

run:
	python manage.py runserver

migrate:
    python manage.py makemigrations
	python manage.py migrate

createsuperuser:
    python manage.py createsuperuser

createnewapp:
	python manage.py startapp polls