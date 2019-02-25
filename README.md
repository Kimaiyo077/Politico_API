[![Build Status](https://travis-ci.org/Kimaiyo077/Politico_API.svg?branch=develop)](https://travis-ci.org/Kimaiyo077/Politico_API) [![Coverage Status](https://coveralls.io/repos/github/Kimaiyo077/Politico_API/badge.svg?branch=develop)](https://coveralls.io/github/Kimaiyo077/Politico_API?branch=develop)

# Project Overview

Politico_API is an application that enables users to communicate with servers to access certian information. It also allows admin users to create new information and to edit or delete existing information.

## Heroku application links

[Heroku app](https://isaac-politico-api-heroku.herokuapp.com/api/v2/offices)

## Pivotal Tracker Project Board

[Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2241889)

## API Documentation

[Documentation](https://politico8.docs.apiary.io/#)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2f5d240af4b87be28938)

# Required Features

1. Admin should be able to create political office.
2. Admin should be able to edit political offices.
3. Admin should be able to delete a specific office.
4. A user should be able to get all political offices.
5. A user should be able to get a specific political office.
6. Admin should be able to create a new political party.
7. Admin should be able to edit existing political parties.
8. Admin should be able to delete a specific political party.
9. A user should be able to get all political parties.
10. A user should be able to get a specific political party.
11. A user should be able to view all candidates running for office.
12. A user should be able to cast their vote for a candidate in a particula office.
13. A user should be able to view the results for a specific office.

# Installation and Setup

Clone or download this repository and install virtualenv using `pip install virtualenv`

## Create and activate a virtual environment

To create a virtual environment called venv use:
`python virtualenv venv`

activate your virtual environment with:
`source venv/scripts/activate`

## Install requirements

install requirements using `pip install -r requirements.txt`

## Running the application

After the configuration, you will run the app uing the following commands

`export FLASK_APP=run.py`
`flask run`

## API endpoints

| Method  | API Endpoint                  | Description                   |
| ------- | ----------------------------- | ----------------------------- |
| `GET`   | `/api/v2/offices`             | View all offices              |
| `POST`  | `/api/v2/offices`          | Add a new office to the list  |
| `PATCH` | `/api/v2/offices/<office_id>` | update the name of a specific office |
| `GET`   | `/api/v2/offices/<office_id>` | View a specific party from the list |
| `DELETE`| `/api/v2/offices/<office_id>`  | Deletes a specific office     |
| `GET`   | `/api/v2/parties`             | Views all parties in the list |
| `POST`  | `/api/v2/parties`            | Adds a new party to the list  |
| `PATCH` | `/api/v2/parties/<party_id>` | Edit name of a specific party |
| `GET`   | `/api/v2/parties/<party_id>`  | View a specific party         |
| `DELETE`| `/api/v2/parties/<party_id>`  | Deletes a specific party      |
| `POST`  | `/api/v2/auth/signup`         | Create a user account         |
| `POST`  | `/api/v2/auth/login`          | Allows users to log in        |
| `POST`  | `/api/v2/offices/<office_id>/register`  | Allows admin to register a candidate|
| `GET`   | `/api/v2/offices/<office_id>/candidates`| Allows users to view candidates|
| `POST`  | `/api/v2/votes`               | Allows users to cast votes   |
| `GET`   | `/api/v2/offices/<office_id>/results` | ALlows users to view the results of a particular office |

## API Payloads

### Creating a new office

`/api/v2/offices`

Payload

```
{
    'name': 'Presidential',
    'type': 'Federal'
}
```

Expected response

```
{
    'data': {'id': '1', name': 'Presidential', 'type': 'Federal'},
    'status': 200
}
```

### Updating an existing offices name

`/api/v2/offices/1`

Payload

```
{
    'name' : 'King'
}
```

Expected response

```
{
    'data' : {'id':'1', 'name':'King', 'type': 'Federal'}
}
```

### Add new party

`/api/v2/parties`

Payload

```
{
    'name': 'Jubilee Party',
    'hqAddress' : 'Jubilee House, Nairobi',
    'logoUrl' : 'https://images.pexels.com'
}
```

Expected response

```
{
    'Status' : 200,
    'Message' : 'New Party added',
    'Party' : 'Jubilee Party'
}
```

### Update an existing party

`/api/v2/parties/1`

Payload

```
{
    'name' : 'Nasa Party'
}
```

Expected response

```
{
    'data' : {'id':'1', 'name': 'Nasa Party', 'hqAddress' : 'Jubilee House, Nairobi', logoUrl' : 'https://images.pexels.com},
    'status' : 200
}
```

### Register a candidate

`/api/v2/offices/<office-id>/register`

Payload

```
{
    'user_id': 1,
    'party_id' : 1
}
```

### Cast a vote

`/api/v2/votes`

Payload

```
{
    'candidate' : 1,
    'user' : 2
}
```