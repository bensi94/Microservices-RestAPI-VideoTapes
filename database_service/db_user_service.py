from sqlalchemy import select, insert, func, and_, update
from shared_utils.logger import _log
from entity_classes.user import User
from database_service.database_utils import Database_utils
from database_service.db_tape_service import Database_tape_service
import json

class Database_user_service:
    
    def __init__(self, connection, tables):
        self.connection = connection
        self.tables = tables
        self.utils = Database_utils(connection)
        #self.tape_service = Database_tape_service(connection, tables)

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

        insert_query = insert(user_table).values(
            name = user['name'],
            email = user['email'],
            phone = user['phone'],
            address = user['address']
        )
        current_id = self.connection.execute(insert_query).inserted_primary_key[0]
        user['id'] = current_id

        response = {
            'code': 200,
            'msg': json.dumps(user)
        }
        return response

    def delete_user(self, user_id):
        user_table = self.tables.get_users_table()
        if self.utils.check_if_exist(user_table, user_id) > 0:
            self.delete_borrow(user_id)
            self.connection.execute(user_table.delete().where(user_table.c.id == user_id))
            response = {
                'code': 200,
                'msg': 'User with ID:' + str(user_id) + ' deleted'
            }
        else:
            response = {
                'code': 400,
                'msg': 'User ID does not exist'
            }
        return response
    
    def update_user(self, user_id, user):
        user_table = self.tables.get_users_table()

        if self.utils.check_if_exist(user_table, user_id) > 0:

            update_query = update(user_table).values(
                name=user['name'],
                email=user['email'],
                phone=user['phone'],
                address=user['address'],
            ).where(user_table.c.id == user_id)
            self.connection.execute(update_query)
            
            user['id'] = user_id

            response = {
                'code': 200,
                'msg': json.dumps(user)
            }
        else:
            response = {
                'code': 400,
                'msg': 'User ID does not exist'
            }
        return response
    def delete_borrow(self, user_id, tape_id=None):
        borrow_table = self.tables.get_borrow_table()
        
        # Delete all borrows of user
        if user_id is None:
            self.connection.execute(borrow_table.delete().where(
                borrow_table.c.user_id == user_id))
        # Delete borrow of user by single tape
        else:
             self.connection.execute(borrow_table.delete().where(and_(
                 borrow_table.c.user_id == user_id, borrow_table.c.tape_id == tape_id)))
