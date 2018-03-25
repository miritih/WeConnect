from instance.validations import (validate_username,
                                  validate_email,
                                  username_taken
                                  )
"""
This files stores all validation schema for all POST and PUT json data
It's what will be used  to validate user data
"""
# register user schema. will validate new user data
reg_user_schema = {
    'username': {
        'type': 'string',
        'required': True,
        'validator': validate_username
    },
    'email': {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': validate_email
    },
    'password': {
        'type': 'string',
        'regex': '\A[0-9a-zA-Z!@#$%&*]{6,20}\Z',
        'required': True,
        'empty': False,
    },
    'first_name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'last_name': {
        'type': 'string',
        'required': True,
        'empty': False,
    }
}
# login data schema. will validate login data
login_schema = {
    "username": {
        'type': 'string',
        'required': True,
        'validator': username_taken
    },
    "password": {
        'type': 'string',
        'required': True
    }
}
