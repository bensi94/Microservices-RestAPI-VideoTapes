from sqlalchemy import select
from shared_utils.logger import _log
from entity_classes.user import User
import json

class Database_user_service:
    
    def __init__(self, connection, users):
        self.connection = connection
        self.users = users

    def get_users(self):
        select_query = select([self.users.get_users_table()])
        result = self.connection.execute(select_query)

        users = []
        for res in result:
            user = User(input_tuple=res)
            users.append(user.return_as_dict())

        return users



