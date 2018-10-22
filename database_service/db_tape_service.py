from sqlalchemy import select
from shared_utils.logger import _log
from entity_classes.tape import Tape
import json

class Database_tape_service:
    
    def __init__(self, connection, tables):
        self.connection = connection
        self.tables = tables

    def get_tapes(self):
        select_query = select([self.tables.get_tapes_table()])
        result = self.connection.execute(select_query)

        tapes = []
        for res in result:
            tape = Tape(input_tuple=res)
            tapes.append(tape.return_as_dict())

        return tapes

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




