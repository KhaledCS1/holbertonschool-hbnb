"""Configuration settings for the HBnB application"""
import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
