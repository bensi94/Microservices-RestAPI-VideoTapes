from sqlalchemy import create_engine
import json

from data_base.tables import Tables

class Database_service:
    def __init__(self):
        with open('data_base/db-config.json', 'r') as file:
            config = json.load(file)

        user = config['POSTGRES_USER']
        db = config['POSTGRES_DB']
        password = config['POSTGRES_PASSWORD']
        host = config['POSTGRES_HOST']
        connection_string = 'postgresql+psycopg2://' + \
            user + ':' + password + '@' + host + '/' + db

        self.db = create_engine(connection_string)
        self.conn = self.db.connect()


    def init_data_base(self):
        tables = Tables(self.db, self.conn)

        # Tables created here if they don't exist
        tables.create_tables()

        # Tables populated only if they are empty
        tables.populate_tables()






