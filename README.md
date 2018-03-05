# API-Monitor
[![CircleCI](https://circleci.com/gh/Ashaba/API-Monitor/tree/develop.svg?style=svg)](https://circleci.com/gh/Ashaba/API-Monitor/tree/develop)
[![Coverage Status](https://coveralls.io/repos/github/Ashaba/API-Monitor/badge.svg?branch=develop)](https://coveralls.io/github/Ashaba/API-Monitor?branch=develop)
 
 An application that performs health checks of an api
 
 # Dependencies
 - `Python 3.6.2`
 - `PostgreSQL`
 - `JQuery-3.3.1`
 - `Flask 0.12.2`
 
 # Installation
 - Clone the repository  
 ```$ git clone https://github.com/Ashaba/API-Monitor.git```
 
 - Copy contents of  `env.sample` into `.env`   
 ```$ cp env.sample .env```
 
 - Configure the database by modifying the `SQLALCHEMY_DATABASE_URI` variable in the .env file

 - Install virtualenv using `pip`
 ```& sudo pip3 install virtualenv```

 - Create a virtual environment  
 ```$ virtualenv -p python3 envname```
 
 - Activate the virtual environment  
 ```$ source envname/bin/activate```
 
 - Install requirements  
 ```$ pip install -r requirements.txt```
 
 - Add environment variables to the `PYTHONPATH`  
 ```$ export $(cat .env)```
 
 # Database Migrations
 - Run migrations  
 
 ```$ python manage.py db upgrade```
 
 
 # Running the application
 `$ flask run`
 Access it on the url `http://127.0.0.1:5000`
 
 
 # Running tests
 -  `$ pytest`
