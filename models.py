
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
        self.businesses = {
            "1": {
                "bio": "Epic",
                "category": "Tech",
                "id": "1",
                "location": "Nairobi,Kenya",
                "name": "Andela",
                "user_id": "mwenda-eric"
            }
        }

    def add_businesses(self, name, location, category, bio, user_id):
        """Adds a new business to businesses dictionary"""
        id = str(len(self.businesses) + 1)
        new_business = {
            'id': id,
            'name': name,
            'location': location,
            'category': category,
            "bio": bio,
            'user_id': user_id
        }
        self.businesses[id] = new_business
        return self.businesses


class Reviews(object):
    """Reviews model class will store all revies data for businesses"""

    def __init__(self):
        self.reviews = {}

    def add_review(self, body, user_id, business_id):
        """ Creates a new review for businesses"""
        id = str(uuid.uuid4())
        new_review = {
            'id': id,
            'body': body,
            'user_id': user_id,
            'business_id': business_id
        }
        self.reviews[id] = new_review
