from sqlalchemy import  select, func, Table, Column, String, MetaData, Integer, Date, ForeignKey, insert
from database_service.json_service import Json_service
from database_service.database_utils import Database_utils
from shared_utils.logger import _log

class Tables:
    def __init__(self, engine, connection):
        self.db = engine 
        self.meta = MetaData(self.db)
        self.users_table = None
        self.tapes_table = None
        self.borrow_table = None
        self.connection = connection
        self.utils = Database_utils(connection)
        
            
    def create_tables(self):
        _log.info('Creating tables')

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
        
        # Data base is only populated if it's empty before
        if (self.utils.count_rows(self.users_table) == 0 and 
            self.utils.count_rows(self.tapes_table) == 0 and 
            self.utils.count_rows(self.borrow_table) == 0):
        
            _log.info('Populating tables')
            json_service = Json_service()
            json_service.read_json()
            
            for user in json_service.get_users():
                insert_query = insert(self.users_table).values(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    phone=user.phone,
                    address=user.address
                )
                self.connection.execute(insert_query)
            
            for tape in json_service.get_tape_list():
                insert_query = insert(self.tapes_table).values(
                    id=tape.id,
                    title=tape.title,
                    director=tape.director,
                    type=tape.type,
                    release_date=tape.release_date,
                    eidr=tape.eidr
                )
                self.connection.execute(insert_query)

            for borrow in json_service.get_borrow_list():
                insert_query = insert(self.borrow_table).values(
                    id=borrow.id,
                    user_id=borrow.user_id,
                    tape_id=borrow.id,
                    borrow_date=borrow.borrow_date,
                    return_date=borrow.return_date
                )
                self.connection.execute(insert_query)

    def get_users_table(self):
        return self.users_table
    
    def get_tapes_table(self):
        return self.tapes_table

    def get_borrow_table(self):
        return self.borrow_table
        


  
