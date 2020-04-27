import os

basedir = os.path.abspath(os.path.dirname(__file__))


# creating a configuration class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-can-be-guest'\

    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://favor:KYlOqGN60gQ6bDI4@cluster0-aet1e.mongodb.net/test?retryWrites=true&w=majority'


    
