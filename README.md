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