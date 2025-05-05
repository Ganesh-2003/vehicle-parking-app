import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_USER = os.path.join(BASE_DIR, 'database', 'users.db')
DATABASE_PARKINGLOT = os.path.join(BASE_DIR, 'database', 'parkinglot.db')