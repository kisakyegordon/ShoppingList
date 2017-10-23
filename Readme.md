[![Build Status](https://travis-ci.org/kisakyegordon/ShoppingList.svg?branch=master)](https://travis-ci.org/kisakyegordon/ShoppingList)


[![Coverage Status](https://coveralls.io/repos/github/kisakyegordon/ShoppingList/badge.svg?branch=master)](https://coveralls.io/github/kisakyegordon/ShoppingList?branch=master)

# SHOPPINGLIST API
A simple Shopping List Flask API, For Tracking a Users Planned Shopping Lists and their corresponding items.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See the deployment section for notes on how to deploy the project on a live system.

### Prerequisites
    * Python 3 Installed on your local machine
    ```
    git clone https://github.com/kisakyegordon/ShoppingList
    ```

    * Ensure Virtualenv is Installed on your local machine using
    ```
    pip install virtualenv
    ```

    * Clone the Repository to your local machine using
    ```
    git clone https://github.com/kisakyegordon/ShoppingList
    ```

    * Setup the virtual environment and activate it using 
    ```
    virtualenv -p python3 myenv
    ```

    * To Install Requirred Plugins - while inside the activated virtual environment
    ```
    pip install -r requirements.txt
    ```

### Database Migrations
* This step asssumes you have the postgres database setup on your local machine , if not go [here] (https://www.postgresql.org/download/)


    * On your psql console, create your main application database:
    ```
    CREATE DATABASE shoppinglist_db;
    ```

    * Also create your testing database
        ```
    CREATE DATABASE shoppinglist_test;
    ```

    * Run database migrations 
    ```
    (myenv)$ python manage.py db init

    (myenv)$ python manage.py db migrate
    ```

    * And finally, migrate your migrations to persist on the DB
    ```
    (myenv)$ python manage.py db upgrade

## Running The API
To run the Application - simply enter the following command in your terminal.
When Successfully run, the API should now be accessible at http://127.0.0.1:5000

```
python run.py 
```

## Running the tests
To run Application tests simply run the following keyword to let nosetests run all tests
```
nosetests
```

### Running the tests with coverage

To get an understanding of what percentage of this project has been tested - simply run

```
nosetests --with-coverage --cover-package=app
```

## Deployment

Using Heroku as a free development server
* Go to settings on Heroku - Variables pick the provided App variables for postgres and pass that very same variable in your configurations
* Push all changes to your github account
* Deploy the github branch with the running API to your Heroku account.


### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /auth/register | True | Create an account
POST | /auth/login | True | Login a user
POST | /auth/reset-password | True | Reset a user password



#### Endpoints to create, update, view and delete a shopping list
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /shoppinglists/ | False | Create a bucket list
GET | /shoppinglists/ | False | View all shopping lists
GET | /shoppinglists/id | False | View details of a shopping list
PUT | /shoppinglists/id | False | Updates a shopping list with a given id
DELETE | /shoppinglists/id | False | Deletes a shoppinglist with a given id



#### Endpoints to create, update, view and delete a shopping list item
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
GET | /shoppinglists/id/items | False | View Items of a given list id
GET | /shoppinglists/id/items/<item_id> | False | View details of a particular item on a given list id
POST | /shoppinglists/id/items/ | False | Add an Item to a shopping list
PUT | /shoppinglists/id/items/<item_id> | False | Update a shopping list item on a given list
DELETE | /shoppinglists/id/items/<item_id> | False | Delete a shopping list item from a given list
