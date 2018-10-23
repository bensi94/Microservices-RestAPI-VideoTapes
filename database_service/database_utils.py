from sqlalchemy import select, func

class Database_utils:

    def __init__(self, connection):
        self.connection = connection

    def count_rows(self, table):
        return int(self.connection.execute(select([func.count()]).select_from(table)).scalar())

    def get_max_id(self, table):
        return int(self.connection.execute(select([func.max(table.c.id)])).scalar()) + 1
    
    def check_if_exist(self, table, id):
        select_query = select([func.count(table.c.id)]).where(
            table.c.id == id)
        return int(self.connection.execute(select_query).scalar())
