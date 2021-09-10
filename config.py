import os 

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'Capstone please work...'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False