from sqlalchemy import select, func, Table, Column, String, MetaData, Integer, Date, ForeignKey, insert, create_engine
from database_service.json_service import Json_service
from database_service.database_utils import Database_utils
import json
import os

def connection_string():
    # Get the config for the database
    with open(os.environ['DB_CONFIG'], 'r') as file:
        config = json.load(file)

    user = config['POSTGRES_USER']
    db = config['POSTGRES_DB']
    password = config['POSTGRES_PASSWORD']
    host = config['POSTGRES_HOST']
    connection_string = 'postgresql+psycopg2://' + \
        user + ':' + password + '@' + host + '/' + db

    return connection_string


def init_database():
    db = create_engine(connection_string())
    connection = db.connect()

    utils = Database_utils(connection)

    meta = MetaData(db)

    print('Creating tables')

    ## USERS table schema
    users_table = Table('users', meta,
                        Column('id', Integer, primary_key=True),
                        Column('name', String, nullable=False),
                        Column('email', String),
                        Column('phone', String),
                        Column('address', String))
    users_table.create(db, checkfirst=True)

    ## TAPES table schema
    tapes_table = Table('tapes', meta,
                        Column('id', Integer, primary_key=True),
                        Column('title', String, nullable=False),
                        Column('director', String),
                        Column('type', String),
                        Column('release_date', Date),
                        Column('eidr', String))
    tapes_table.create(db, checkfirst=True)

    ## BORROW table schema
    borrow_table = Table('borrows', meta,
                            Column('id', Integer, primary_key=True),
                            Column('user_id', Integer, ForeignKey(
                                'users.id'), nullable=False),
                            Column('tape_id', Integer, ForeignKey(
                                'tapes.id'), nullable=False),
                            Column('borrow_date', Date),
                            Column('return_date', Date))
    borrow_table.create(db, checkfirst=True)


        # Data base is only populated if it's empty before
    if (utils.count_rows(users_table) == 0 and
        utils.count_rows(tapes_table) == 0 and 
        utils.count_rows(borrow_table) == 0):
    
        print('Populating tables')
        json_service = Json_service()
        json_service.read_json()
        
        for user in json_service.get_users():
            insert_query = insert(users_table).values(
                id=user.id,
                name=user.name,
                email=user.email,
                phone=user.phone,
                address=user.address
            )
            connection.execute(insert_query)
        
        for tape in json_service.get_tape_list():
            insert_query = insert(tapes_table).values(
                id=tape.id,
                title=tape.title,
                director=tape.director,
                type=tape.type,
                release_date=tape.release_date,
                eidr=tape.eidr
            )
            connection.execute(insert_query)

        for borrow in json_service.get_borrow_list():
            insert_query = insert(borrow_table).values(
                id=borrow.id,
                user_id=borrow.user_id,
                tape_id=borrow.id,
                borrow_date=borrow.borrow_date,
                return_date=borrow.return_date
            )
            connection.execute(insert_query)



def delete_all_db():
        db = create_engine(connection_string())
        metadata = MetaData(bind=db)
        metadata.reflect()

        for tbl in reversed(metadata.sorted_tables):
             db.execute(tbl.delete())
    
