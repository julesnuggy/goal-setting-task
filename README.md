# Goal Setting Task

## Installation Instructions

### Requires Python >=3.8


### create a virtualenv

```
python3 -m venv venv
```

### install requirements

```
pip3 install -r requirements.txt
```

### activate virtualenv

```
source venv/bin/activate
```

### recommended - set flask to development mode

(so it refreshes the web server if you make any changes to your code)

```
export FLASK_ENV=development
```

### run flask server

```
flask run
```

### you can also use the shell to do any debugging/code testing

### included is a module to run this in ipython

```
flask shell
```

### run tests

```
venv/bin/python -m pytest tests/
```
