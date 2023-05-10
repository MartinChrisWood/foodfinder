# foodfinder

Developing an app to make it easier for people to find foodbanks in and around Sheffield.


## Install

```shell
python3 -m venv env
source env/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

By default, flask will look for a file called `app.py`, you can also name a specific python program to run.

```shell
flask --debug run
```

## Test

Preferred unittesting framework is PyTest:

```shell
pytest
```

## Auto-assigning coordinates to postcodes and foodbanks

```shell
python src/make_data.py
```