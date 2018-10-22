from sqlalchemy import select, insert, func
from shared_utils.logger import _log
from entity_classes.tape import Tape
from database_service.database_utils import Database_utils
import json

class Database_tape_service:
    
    def __init__(self, connection, tables):
        self.connection = connection
        self.tables = tables
        self.utils = Database_utils(connection)

    # Makes a select * from tables query and returns tapes
    def get_tapes(self):
        select_query = select([self.tables.get_tapes_table()])
        result = self.connection.execute(select_query)

        tapes = []
        for res in result:
            tape = Tape(input_tuple=res)
            tapes.append(tape.return_as_dict())

        return tapes

    # Makes a select * from tables where id == x, query and returns tape
    def get_tape(self, tape_id):
        tape_table = self.tables.get_tapes_table()
        select_query = select([tape_table]).where(tape_table.c.id == tape_id)
        result = self.connection.execute(select_query)
        result = result.fetchone()

        if result is None:
            return None
        else:
            tape = Tape(input_tuple=result)
            return tape.return_as_dict()
    
    # Makes Insert query for tape
    def add_tape(self, tape):
        tape_table = self.tables.get_tapes_table()
        new_id = self.utils.get_max_id(tape_table)

        # Checking if eidr exists in database
        if int(self.connection.execute(select(
            [func.count(tape_table.c.eidr)]).where(tape_table.c.eidr 
            == tape['eidr'])).scalar()) > 0:
            response = {
                'code': 400,
                'msg': 'Edir already exists'
            }

        else: 
            insert_query = insert(tape_table).values(
                id=new_id,
                title=tape['title'],
                director=tape['director'],
                type=tape['type'],
                release_date=tape['release_date'],
                eidr=tape['eidr']
            )

            self.connection.execute(insert_query)

            response = {
                'code': 200,
                'msg': 'Tape added: title=' + tape['title'] + ' id=' + str(new_id)
            }
        return response




