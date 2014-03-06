import os

SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'database.db'))


SAMPLE_CSV_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'sample_car_database.csv'))