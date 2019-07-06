import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@electivoespecialidadi.cm0fytbjzmgm.us-east-1.rds.amazonaws.com:5432/{}'.format(
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME'))
