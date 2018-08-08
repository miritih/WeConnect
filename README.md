[![Build Status](https://travis-ci.org/miritih/WeConnect.svg?branch=master)](https://travis-ci.org/miritih/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/mwenda-eric/WeConnect/badge.svg?branch=master)](https://coveralls.io/github/mwenda-eric/WeConnect?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/5b51c1bf68870dbfa35f/maintainability)](https://codeclimate.com/github/miritih/WeConnect/maintainability)
# WeConnect
WeConnect provides a platform that brings businesses and individuals together by creating awareness for businesses and giving the users the ability to write reviews about the businesses they have interacted with. 


### Requirements
It is recommended that you have the following set up on your local environment before getting started
- python3.5 or later
- A working Virtual environment
- PostgreSQL. preferably 9.5 or later

### Installation
Clone the repository into your machine
`$ git clone https://github.com/mwenda-eric/WeConnect.git`

Change directory into WeConnect
`$ cd WeConnect`

Activate Your virtual environment
`source <env_folder>/bin/activate`

Install project dependencies
`pip install -r requirements.txt`

Set The following environment variables `SECRET_KEY`,`APP_SETTINGS`,`DATABASE_URI`,`FLASK_APP`

Variable| Description
---|---
`SECRET_KEY`| Sets the applications secret key
`APP_SETTINGS`| sets the environment, either `development` `testing` or `production` 
`DATABASE_URI`| sets the application database URL 
`FLASK_APP`| Exports flask app. set it to `run.py`


Finally, run `python app.py`

### Testing
Ensure you have the following environment variables set:
- `DATABASE_URI` variable should be set to your testing database URL
- `APP_SETTINGS` variable should be set to testing

Then Run the following  command
`nosetests --with-coverage --cover-package=app`

### Api Endpoints
1. Users Endpoints 
- `POST /api/v2/auth/register`  Creates a user account
- `POST /api/v2/auth/login` Logs in a user
- `POST /api/v2/auth/logout` Logout a user
- `PUT /api/v2/auth/reset-password` Resets user password
2. Businesses Endpoints
- `POST /api/v2/businesses` Register a new business
- `GET /api/v2/businesses` List all registered businesses
- `GET /api/v2/businesses/user` Gets all businesses for the current loggwd in user 
- `PUT /api/v2/businesses/<businessId>` Update business 
- `DELETE /api/v2/businesses/<businessId>` delets a business
3. Reviews Endpoints
- `POST /api/v2/businesses/<businessId>/reviews` create a new review 
- `GET /api/v2/businesses/<businessId>/reviews` Get reviews
- `PUT /api/v2/businesses/<businessId>/reviews/reviewId` Updates a review
- `DELETE /api/v2/businesses/<businessId>/reviews/reviewId` Deletes a review

##### Searching and pagination
For all GET endpoints, pagination can be applied by embedding `page` or `limit` params on the request URL
> e.g `GET /api/v2/businesses?page=2&limit=10` `page` sets the pagination page and `limit` will set the number of records per page
**If the params are not provided the default page will be 1 and limit will be 10**

For GET business Endpoint, search can be performed using `name`, `location` or `category`
> e.g `GET /api/v2/businesses?name=andela&category=technology&location=nairobi`
You can filter by either of the three params or with all of them at the same time

#### Documentation 
To view the WeConnect API documentation visit the following links:

WeConnect V1
https://app.swaggerhub.com/apis/miriti/WeConnect/1.0.0

WeConnect V2
https://app.swaggerhub.com/apis/miriti/WeConnect/2.0

### (Designs)HTML Pages included
The following are the included HTML pages
- Landing page/ Business catalog page. Lists all registered businesses
- User login page
- User sign up page
- Business profile/reviews page
- Business registration page
- Business edit page
