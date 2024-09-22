import os

class Config:
    URL = "localhost:9000"
    KEY = "KEY"
    SECRET = "SECRET"

    @classmethod
    def init_app(cls,app):
        pass

class DevConfig(Config):
    URL = "localhost:9000"
    KEY = "gjUHI2lScQ6JhwnbBkas"
    SECRET = os.getenv("SECRET")

config = {
    'dev': DevConfig,
}