from instance.validations import (validate_username,
                                  validate_email,
                                  username_taken,
                                  validate_password,
                                  validate_bsname
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
        'validator': validate_password,
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
#update user schema
update_user_schema = {
    'username': {
        'type': 'string',
        'required': True,
    },
    'email': {
        'type': 'string',
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
    },
    'image': {
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
# reset-password data schema

reset_pass = {
    "password": {
        'type': 'string',
        'validator': validate_password,
        'required': True
    },
    "old_password": {
        'type': 'string',
        'required': True
    }
}

new_business = {
    "name": {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': validate_bsname
    },
    "location": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "category": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "bio": {
        'type': 'string',
        'required': True,
        'empty': False
    }
}
review_schema = {
    "review": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "title": {
        'type': 'string',
        'required': True,
        'empty': False
    }
}
