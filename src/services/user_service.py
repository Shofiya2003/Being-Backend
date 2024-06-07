from src import db

User = db['users']

def check_unique_credentials(username,email):
    try:
        return User.find_one({'$or':[{'username':username},{'email':email}]})
    except Exception as e:
        return e
    
def find_user(query):
    try:
        return User.find_one(query)
    except Exception as e:
        return e