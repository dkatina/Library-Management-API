
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    DEBUG = True


class TestingConfig:
    pass

class ProductionConfig:
    pass