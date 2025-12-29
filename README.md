# COMPSCI 235 - CS235 Pod Library
This is a repository for the podcasts webapp project of CompSci 235 in Semester 2, 2024. Assignment done by Neil Huang, Anthony Liang and Ziyang Zhou.
## Description

This repository contains the completed assignment (everything detailed from phase 1 to 3). The Installation for any dependencies will be the same as the starter repository given. The explanation on how to setup the virtual environment will also be the same.
## Installation


**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
If pip is available for update, then do so following the instructions on the terminal after the last command.

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *project directory*, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python –m pytest –v tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Configuration

The *project directory/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
* `SQLALCHEMY_DATABASE_URI`: A connection string that tells SQLAlchemy what database to connect to.
* `SQLALCHEMY_ECHO`:  Controls whether SQLAlchemy logs all the SQL statements it executes.
* `REPOSITORY`: Select between the database or memory repository,
## Data sources

The data files are modified excerpts downloaded from:

https://www.kaggle.com/code/switkowski/building-a-podcast-recommendation-engine/input




