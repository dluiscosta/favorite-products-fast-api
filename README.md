## Introduction

This is a side project intended to serve as my first contact with Python's 
[FastAPI](https://fastapi.tiangolo.com/), as well as a technical assessment. 
No productive usage is envisioned.

# Favorite Products FastAPI

The Favorite Products allows Customers to be created and Favorite Products to be appended to them. These are interconnected with [this](https://gist.github.com/Bgouveia/9e043a3eba439489a35e70d1b5ea08ec) Luiza Lab's API, including cross validation and data fetching.

# Running the project

In order to run this project, Python 3.8 and [pipenv](https://pipenv.pypa.io/en/latest/) will be required. From the root folder, starting with

```
pipenv install --dev
```

will create a virtual environment with all the required dependencies installed. Then,

```
pipenv run python main.py
```

will start up the application and expose it [here](http://localhost:8000), also making a [Swagger](http://127.0.0.1:8000/docs) and a [ReDoc](http://127.0.0.1:8000/redoc) interactive documentations available.

Additionally, unit tests can be run with

```
pipenv run pytest
```
