# Login System

A Login system made entirely with Python using Flask login, Flask Dance and Flask Mail. In this project the user is able to **Sign up**, **Sign in with email**, **Reset password** and **Sign in with Github, Google, Facebook or Twitter**.

## Installing

**Install environment**: 

     python3 -m pip install --user --upgrade pip
     python3 -m pip install --user virtualenv
     python3 -m venv env

**Enable virtual environment**: `source env/bin/activate `

**Install packages**: `pip install -r requirements.txt`

**Create db**: 

     python3
     from project import db, create_app
     db.create_all(app=create_app())
     exit()

### Run the application: 

- Terminal: `flask run`
