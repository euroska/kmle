import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("DOCAPI_SECRET_KEY", "secret_key")
    HASH_FUNCTIONS = {"sha256", "sha1", "md5"}
    ALLOWED_EXTENSION = {"docx", "pdf"}
    TIKA_SERVER = os.getenv("DOCAPI_TIKA_URL", "http://docapi-tika")


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DOCAPI_DEV_DB", "postgres://postgres:password@docapi-postgres/dev"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DOCAPI_TEST_DB", "postgres://postgres:password@docapi-postgres/test"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DOCAPI_PROD_DB", "postgres://postgres:password@docapi-postgres/postgres"
    )


CONFIG_BY_NAME = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
KEY = Config.SECRET_KEY
