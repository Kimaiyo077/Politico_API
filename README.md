[![Build Status](https://travis-ci.org/Kimaiyo077/Politico_API.svg?branch=develop)](https://travis-ci.org/Kimaiyo077/Politico_API) [![Coverage Status](https://coveralls.io/repos/github/Kimaiyo077/Politico_API/badge.svg?branch=develop)](https://coveralls.io/github/Kimaiyo077/Politico_API?branch=develop)

# Project Overview

Politico_API is an application that enables users to communicate with servers to access certian information. It also allows admin users to create new information and to edit or delete existing information.

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
| `GET`   | `/api/v1/offices`             | View all offices              |
| `POST`  | `/api/v1/offices`          | Add a new office to the list  |
| `PATCH` | `/api/v1/offices/<office_id>` | update the name of a specific office |
| `GET`   | `/api/v1/offices/<office_id>` | View a specific party from the list |
| `DELETE`| `/api/v1/offices/<office_id>`  | Deletes a specific office     |
| `GET`   | `/api/v1/parties`             | Views all parties in the list |
| `POST`  | `/api/v1/parties`            | Adds a new party to the list  |
| `PATCH` | `/api/v1/parties/<party_id>/name` | Edit name of a specific party |
| `GET`   | `/api/v1/parties/<party_id>`  | View a specific party         |
| `DELETE`| `/api/v1/parties/<party_id>`  | Deletes a specific party      |

## API Payloads

### Creating a new office

`/api/v1/offices`

Payload

```
{
    'name': 'Presidential',
    'type': 'State Government'
}
```

Expected response

```
{
    'data': {'id': '1', name': 'Presidential', 'type': 'State Government'},
    'status': 200
}
```

### Updating an existing offices name

`/api/v1/offices/1`

Payload

```
{
    'name' : 'Presidents'
}
```

Expected response

```
{
    'data' : {'id':'1', 'name':'Presidents', 'type': 'State Government'}
}
```

### Add new party

`/api/v1/parties`

Payload

```
{
    'name': 'Jubilee Party',
    'hqAddress' : 'Jubilee House, Nairobi',
    'logoUrl' : 'https://images.pexels.com/photos/866351/pexels-photo-866351.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
}
```

Expected response

```
{
    'Status' : 'OK',
    'Message' : 'New Party added',
    'Party' : 'Jubilee Party'
}
```

### Update an existing party

`/api/v1/parties/1/name`

Payload

```
{
    'name' : 'Nasa Party'
}
```

Expected response

```
{
    'data' : {'id':'1', 'name': 'Nasa Party', 'hqAddress' : 'Jubilee House, Nairobi', logoUrl' : 'https://images.pexels.com/photos/866351/pexels-photo-866351.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'},
    'status' : 200
}
```

## Heroku application links

[Heroku app](https://isaac-politico-api-heroku.herokuapp.com/api/v1/offices)

## Pivotal Tracker Project Board

[Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2241889)