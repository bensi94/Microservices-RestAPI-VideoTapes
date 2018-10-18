from sqlalchemy import  select, func, Table, Column, String, MetaData, Integer, Date, ForeignKey, create_engine
from data_base.json_service import Json_service

class Tables:
    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        self.meta = MetaData(self.db)
        self.users_table = ()
        self.tapes_table = ()
        self.borrow_table = ()
            
    def create_tables(self):
                ## USERS table schema
        users_table = Table('users', self.meta,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, nullable=False),
                            Column('email', String),
                            Column('phone', String),
                            Column('address', String))
        users_table.create(self.db, checkfirst=True)
        self.users_table = users_table

        ## TAPES table schema
        tapes_table = Table('tapes', self.meta,
                            Column('id', Integer, primary_key=True),
                            Column('title', String, nullable=False),
                            Column('director', String),
                            Column('type', String),
                            Column('release_date', Date),
                            Column('eidr', String))
        tapes_table.create(self.db, checkfirst=True)
        self.tapes_table = tapes_table

        ## BORROW table schema
        borrow_table = Table('borrows', self.meta,
                             Column('id', Integer, primary_key=True),
                             Column('user_id', Integer, ForeignKey(
                                 'users.id'), nullable=False),
                             Column('tape_id', Integer, ForeignKey(
                                 'tapes.id'), nullable=False),
                             Column('borrow_date', Date),
                             Column('return_date', Date))
        borrow_table.create(self.db, checkfirst=True)
        self.borrow_table = borrow_table

    def populate_tables(self):
        print("Here")
        json_service = Json_service()
        json_service.read_json()
        
        # We only want to populate the tables if they are empty
        if (select([func.count()]).select_from(self.users_table) == 0 and
            select([func.count()]).select_from(self.tapes_table) == 0 and
            select([func.count()]).select_from(self.borrow_table) == 0):
            json_service = Json_service()
            json_service.read_json()
            
