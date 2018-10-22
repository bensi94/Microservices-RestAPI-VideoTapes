from sqlalchemy import create_engine
import json

from database_service.tables import Tables
from shared_utils.logger import _log

class Database_service:

    tables = None

    # Creates connections to the database
    def __init__(self):
        _log.info('Connecting to database')

        # Get the config for the database
        with open('database_service/db-config.json', 'r') as file:
            config = json.load(file)

        user = config['POSTGRES_USER']
        db = config['POSTGRES_DB']
        password = config['POSTGRES_PASSWORD']
        host = config['POSTGRES_HOST']
        connection_string = 'postgresql+psycopg2://' + \
            user + ':' + password + '@' + host + '/' + db

        self.db = create_engine(connection_string)
        self.conn = self.db.connect()

    # Initializes tables and data in the database
    def init_database(self):
        _log.info('Initializing to database')

        self.tables = Tables(self.db, self.conn)

        # Tables created here if they don't exist
        self.tables.create_tables()

        # Tables populated only if they are empty
        self.tables.populate_tables()

    def get_connection(self):
        return self.conn
    
    def get_tables(self):
        return self.tables



