from sqlalchemy import create_engine, MetaData
import json
import os
import time

from database_service.tables import Tables
from shared_utils.logger import _log
from sqlalchemy_utils import drop_database, create_database

class Database_service:

    tables = None

    # Creates connections to the database
    def __init__(self):
        _log.info('Connecting to database')

        # Get the config for the database
        with open(os.environ['DB_CONFIG'], 'r') as file:
            config = json.load(file)

        # Gets the connection varibles from the config file
        user = config['POSTGRES_USER']
        db = config['POSTGRES_DB']
        password = config['POSTGRES_PASSWORD']
        host = config['POSTGRES_HOST']
        connection_string = 'postgresql+psycopg2://' + \
            user + ':' + password + '@' + host + '/' + db

        _log.info(connection_string)

        self.db = create_engine(connection_string)
        self.conn = self.db.connect()
        self.meta = MetaData(self.db)

        self.connection_string = connection_string

    # Initializes tables and data in the database
    def init_database(self):
        _log.info('Initializing to database')

        self.tables = Tables(self.db, self.conn, self.meta)

        # Tables created here if they don't exist
        self.tables.create_tables()

        # Tables populated only if they are empty
        self.tables.populate_tables()

    def get_connection(self):
        return self.conn
    
    def get_tables(self):
        return self.tables

    # ONLY USED FOR TESTING, HANDLE WITH CARE
    def delete_and_populate(self):
        trans = self.conn.begin()

        # Deletes from all tables
        for table in reversed(self.meta.sorted_tables):
            delete_string = table.delete()
            _log.info(delete_string)
            self.conn.execute(delete_string)
        
        # Resets the counting sequence
        self.conn.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1')
        self.conn.execute('ALTER SEQUENCE tapes_id_seq RESTART WITH 1')
        self.conn.execute('ALTER SEQUENCE borrows_id_seq RESTART WITH 1')
        self.conn.execute('ALTER SEQUENCE reviews_id_seq RESTART WITH 1')

        trans.commit()

        self.tables.populate_tables()
        return ('Tables Deleted and repopulated!')