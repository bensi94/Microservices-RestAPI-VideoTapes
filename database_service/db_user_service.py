from sqlalchemy import select, insert
from shared_utils.logger import _log
from entity_classes.user import User
from database_service.database_utils import Database_utils
import json

class Database_user_service:
    
    def __init__(self, connection, tables):
        self.connection = connection
        self.tables = tables
        self.utils = Database_utils(connection)

    def get_users(self):
        select_query = select([self.tables.get_users_table()])
        result = self.connection.execute(select_query)

        users = []
        for res in result:
            user = User(input_tuple=res)
            users.append(user.return_as_dict())

        return users

    def get_user(self, user_id):
        user_table = self.tables.get_users_table()
        select_query = select([user_table]).where(user_table.c.id == user_id)
        result = self.connection.execute(select_query)
        result = result.fetchone()

        if result is None:
            return None
        else:
            user = User(input_tuple=result)
            return user.return_as_dict()

    def add_user(self, user):
        user_table = self.tables.get_users_table()
        new_id = self.utils.get_max_id(user_table)

        insert_query = insert(user_table).values(
            id = new_id,
            name = user['name'],
            email = user['email'],
            phone = user['phone'],
            address = user['address']
        )
        self.connection.execute(insert_query)
        response = {
            'code': 200,
            'msg': 'User added: name='+ user['name'] + ' id = ' + str(new_id)
        }
        return response