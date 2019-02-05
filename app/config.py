''' States runtime environment configurations for the API '''

import os

class Config:
    ''' Defines common configurations '''

    SECRET = os.getenv('SECRET')

class TestingConfig(Config):
    ''' Defines configurations for testing environment'''

    TESTING = True

class DevelopmentConfig(Config):
    ''' Defines configurations for development environment'''

    DEBUG = True

class ProductionConfig(Config):
    ''' Defines configurations for production environment'''

    TESTING = False
    DEBUG = False

# create a dictionary to store instances of different configurations environments.
app_config = {
    'testing' : TestingConfig,
    'development' : DevelopmentConfig,
    'production' : ProductionConfig
}
