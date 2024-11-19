DB_NAME = 'Polls'
DB_USER = 'qDlayyy'
DB_PASSWORD = 'SlavaBatman'
DB_HOST = 'localhost'
DB_PORT = '50000'

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False