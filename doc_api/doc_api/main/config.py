import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("DOCAPI_SECRET_KEY", "secret_key")
    HASH_FUNCTIONS = {"sha256", "sha1", "md5"}
    ALLOWED_EXTENSION = {"docx", "pdf"}


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@intelligent_lovelace/dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@intelligent_lovelace/test"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DOCAPI_DATABASE_URI", "postgres://postgres:password@intelligent_lovelace/postgres"
    )


CONFIG_BY_NAME = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
KEY = Config.SECRET_KEY
