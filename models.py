
import uuid


class User(object):
    """The class data models. storea application data in data structures"""

    def __init__(self):
        self.users = {}
        self.user_token = {}

    def add_user(self, username, password, first_name, last_name, admin=False):
        """Creates a new user an append to the list of users"""
        data = {'id': uuid.uuid4(), 'username': username, 'password': password,
                'first_name': first_name, "last_name": last_name, "admin": admin}
        self.users[username] = data
        return self.users


class Business(object):
    """Business model. store all business data"""

    def __init__(self):
        self.businesses = {}

    def add_businesses(self, name, location, category, bio, user_id):
        """Adds a new business to businesses dictionary"""
        new_business = {'id': uuid.uuid4(), 'name': name, 'location': location,
                        'category': category, "bio": bio, 'user_id': user_id}
        self.businesses[name] = new_business
        return self.businesses

    def update_business(self):
        """ """
        pass

    def delete_business(self):
        """ """
        pass
