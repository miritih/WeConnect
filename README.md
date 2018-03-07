[![Build Status](https://travis-ci.org/mwenda-eric/WeConnect.svg?branch=master)](https://travis-ci.org/mwenda-eric/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/mwenda-eric/WeConnect/badge.svg?branch=master)](https://coveralls.io/github/mwenda-eric/WeConnect?branch=master)
# WeConnect
WeConnect provides a platform that brings businesses and individuals together by creating awareness for businesses and giving the users the ability to write reviews about the businesses they have interacted with. 


### Requirements
It is recommended that you have the following set up on your local environment before getting started
- python3.5 or later
- A working Virtual environment

### Installation
Clone the repository into your machine
`$ git clone https://github.com/mwenda-eric/WeConnect.git`

Change directory into WeConnect
`$ cd WeConnect`

Activate Your virtual environment
`source <env_folder>/binactivate`

Install project dependencies
`pip install -r requirements.txt`

Finally run `python app.py`

### Testing
Run command 
`nosetests tests --with-coverage`

### Api Endpoints
1. Users 
- `POST /api/v1/auth/register` Creates a user account
- `POST /api/v1/auth/login` Logs in a user
- `POST /api/v1/auth/logout` Logout a user
- `PUT /api/v1/auth/reset-password` Resets user password
2. Businesses
- `POST /api/v1/businesses` Register a new business
- `GET /api/v1/businesses` List all registered businesses
- `PUT /api/v1/businesses/<businessId>` Update business 
- `DELETE /api/v1/businesses/<businessId>` delets a business
3. Reviews
- `POST /api/v1/businesses/<businessId>/reviews` create a new review 
- `GET /api/v1/businesses/<businessId>/reviews` Get reviews


### (Designs)HTML Pages included
The following are the included HTML pages
- Landing page/ Business catalog page. Lists all registered businesses
- User login page
- User sign up page
- Business profile/reviews page
- Business registration page
- Business edit page

###credits
- eric mwenda