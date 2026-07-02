"""
Configuration file for Fake News Detector API
Modify these settings based on your deployment environment
"""

import os

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Server Settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    
    # Model Settings
    MODEL_PATH = os.environ.get('MODEL_PATH', 'finalized_model.pkl')
    VECTORIZER_PATH = os.environ.get('VECTORIZER_PATH', 'tfidf_vectorizer.pkl')
    TRAINING_DATA_PATH = os.environ.get('TRAINING_DATA_PATH', 'news.csv')
    
    # API Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    JSON_SORT_KEYS = False
    
    # CORS Settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')  # Change to specific domain in production
    
    # Rate Limiting (requests per hour per IP)
    RATE_LIMIT_ENABLED = False  # Set to True in production
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_PERIOD = 3600  # 1 hour in seconds
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CORS_ORIGINS = '*'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Override CORS_ORIGINS with your frontend domain
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://yourfrontend.com')
    RATE_LIMIT_ENABLED = True
    
    # Production logging
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])


# Example usage in app.py:
# from config import get_config
# app.config.from_object(get_config())