
import uuid


class Model(object):
    """The class data models. storea application data in data structures"""

    def __init__(self):
        self.users = {}

    def add_user(self, username, password, first_name, last_name):
        """Creates a new user an append to the list of users"""
        data = {'id': uuid.uuid4(), 'username': username, 'password': password,
                'first_name': first_name, "last_name": last_name}
        self.users[username] = data
        return self.users

    def get_all_users(self):
        """returns a list of all registerd users"""
        return self.users

    def clear_data(self):
        """ clear application data"""
        self.users.clear()
