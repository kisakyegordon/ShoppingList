[![Build Status](https://travis-ci.org/kisakyegordon/ShoppingList.svg?branch=master)](https://travis-ci.org/kisakyegordon/ShoppingList)

[![Coverage Status](https://coveralls.io/repos/github/kisakyegordon/ShoppingList/badge.svg?branch=master)](https://coveralls.io/github/kisakyegordon/ShoppingList?branch=master)

# SHOPPINGLIST API
A simple Shopping List Flask API, For Tracking a Users Planned Shopping Lists and their corresponding items.

### API Documentation
ShoppingList API Documentation
```
- http://docs.shoppinglist11.apiary.io/#reference/0/shoppinglist-manipulation/delete-a-shopping-list
```


### Features:
* Users can create accounts
* Users can login
* Users can create, edit, view and delete a Shopping List
* Users can create, edit, view and delete Shopping List Items



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



### Installing
Clone the Repository to your local machine using
- git clone https://github.com/kisakyegordon/ShoppingList

### Installing Requirred Plugins
To Install Requirred Plugins
```
- Setup a virtual environemnt and activate it
- pip install -r requirements.txt
```

### Running The API
To run the Application

```
- python run.py 
```

### Running The Tests With Coverage
To run all API tests
```
- nosetests --with-coverage --cover-package=app
```

