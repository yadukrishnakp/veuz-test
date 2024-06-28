# veuz_core New Site 

This App used for User registration and login, the user can create new employees and its settings.

# Project Requirements
```
Python >= 3.10.10
Django >= 4.1.7
```

## Installation

Follow these commands step by step


```python

# create virtual env
python -m venv venv

# activate virtual env
   #linux
     source/bin/activate
   #windows 
     venv/Scripts/activate


# install and upgrade pip
python -m pip install --upgrade pip

# install project requirements
pip install -r requirements.txt


For permission seeder

```sh
python manage.py loaddata initial-data.json
```


# copy '.env.example' and rename '.env.example' to '.env'
# create postgresql database
# set database credentials in '.env' file

# run local server
python manage.py runserver

