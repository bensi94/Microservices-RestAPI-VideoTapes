from sqlalchemy import select, insert, func, and_, update
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
                title=tape['title'],
                director=tape['director'],
                type=tape['type'],
                release_date=tape['release_date'],
                eidr=tape['eidr']
            )

            current_id = self.connection.execute(insert_query).inserted_primary_key[0]
            tape['id'] = current_id

            
            response = {
                'code': 200,
                'msg': json.dumps(tape)
            }
        return response

    # Deletes user by id
    def delete_tape(self, tape_id):
        tape_table = self.tables.get_tapes_table()

        if self.utils.check_if_exist(tape_table, tape_id) > 0:
            self.delete_borrow(tape_id)
            self.delete_review(tape_id)
            self.connection.execute(tape_table.delete().where(tape_table.c.id == tape_id))
            response = {
                'code': 200,
                'msg': 'Tape with ID:' + str(tape_id) + ' deleted'
            }
        else:
            response = {
                'code': 400,
                'msg': 'Tape ID does not exist'
            }
        return response
    
    # Updates tape at a spesific id
    def update_tape(self, tape_id, tape):
        tape_table = self.tables.get_tapes_table()

        if self.utils.check_if_exist(tape_table, tape_id) > 0:
            if int(self.connection.execute(select(
                [func.count(tape_table.c.eidr)]).where(
                    tape_table.c.eidr == tape['eidr'])).scalar()) > 0:
                response = {
                    'code': 400,
                    'msg': 'Edir already exists'
                }
                return response

            update_query = update(tape_table).values(
                title=tape['title'],
                director=tape['director'],
                type=tape['type'],
                release_date=tape['release_date'],
                eidr=tape['eidr']
            ).where(tape_table.c.id == tape_id)
            self.connection.execute(update_query)
            
            tape['id'] = tape_id

            response = {
                'code': 200,
                'msg': json.dumps(tape)
            }
            return response
        else:
            response = {
                'code': 400,
                'msg': 'Tape ID does not exist'
            }
            return response



    # Delete tapes from borrows, if user_id is set 
    # it only deletes as single tape, otherwise all
    def delete_borrow(self, tape_id, user_id=None):
        borrow_table = self.tables.get_borrow_table()
        
        # Delete all borrows of tape
        if user_id is None:
            self.connection.execute(borrow_table.delete().where(
                borrow_table.c.tape_id == tape_id))
        # Delete borrow of tape by single user
        else:
             self.connection.execute(borrow_table.delete().where(and_(
                 borrow_table.c.tape_id == tape_id, borrow_table.c.user_id == user_id)))

    # Delete tapes from reveiws, if user_id is set
    # it only deletes as single review, otherwise all
    def delete_review(self, tape_id, user_id=None):
        review_table = self.tables.get_review_table()

        # Delete all reviews of tape
        if user_id is None:
            self.connection.execute(review_table.delete().where(
                review_table.c.tape_id == tape_id))
        # Delete review of tape by single user
        else:
             self.connection.execute(review_table.delete().where(and_(
                 review_table.c.tape_id == tape_id, review_table.c.user_id == user_id)))

    
    def register_tape(self, borrow):
        tape_table = self.tables.get_tapes_table()
        user_table = self.tables.get_tapes_table()
        borrow_table = self.tables.get_borrow_table()
        new_id = self.utils.get_max_id(borrow_table)

        # Checking if user_id and tape_id both exist
        if self.utils.check_if_borrow_exists(borrow_table, borrow['user_id'], borrow['tape_id']):
            response = {
                'code': 400,
                'msg': 'This user already has this tape or loan or has rented it before.'
            }
            return response
        if not self.utils.check_if_exist(tape_table, borrow['tape_id']):
            response = {
                'code': 400,
                'msg': 'No tape with that ID exists'
            }
            return response
        elif not self.utils.check_if_exist(user_table, borrow['user_id']):
            response = {
                'code': 400,
                'msg': 'No user with that ID exists'
            }
            return response

        else: 
            insert_query = insert(borrow_table).values(
                id=new_id,
                tape_id=borrow['tape_id'],
                user_id=borrow['user_id'],
                borrow_date = borrow['borrow_date'],
                return_date = None
            )

            self.connection.execute(insert_query)

            borrow['id'] = new_id
            
            response = {
                'code': 200,
                'msg': json.dumps(borrow)
            }
            return response

    def return_tape(self, return_date, user_id, tape_id):
        borrow_table = self.tables.get_borrow_table()

        if  not self.utils.check_if_borrow_exists(borrow_table, user_id, tape_id):
            response = {
                'code': 400,
                'msg': 'The user with this ID does not have tape on loan with this ID.'
            }
            return response
        else:
            if not self.utils.return_date_is_none(borrow_table, user_id, tape_id):
                response = {
                    'code': 400,
                    'msg': 'Tape has already been returned.'
                }
                return response
            response = {
                'code': 200,
                'msg': 'Tape has been returned'
            }
            update_query = update(borrow_table).values(
                return_date = return_date
            ).where(and_(borrow_table.c.tape_id == tape_id, 
                borrow_table.c.user_id == user_id))
            self.connection.execute(update_query)

            return response
    def update_registration(self, borrow):
        borrow_table = self.tables.get_borrow_table()
        if self.utils.check_if_borrow_exists(borrow_table, borrow['user_id'], borrow['tape_id']):
            update_query = update(borrow_table).values(
                    borrow_date = borrow['borrow_date'],
                    return_date = borrow['return_date']
                ).where(and_(borrow_table.c.tape_id == borrow['tape_id'], borrow_table.c.user_id == borrow['user_id']))
            self.connection.execute(update_query)
            response = {
                'code': 200,
                'msg': 'Registration has been updated.'
            }
            return response
        else:
            response = {
                'code': 400,
                'msg': 'This registration does not exist.'
            }
            return response

    def get_tapes_of_user(self, user_id):
        borrow_table = self.tables.get_borrow_table()
        tape_table = self.tables.get_tapes_table()
        user_table = self.tables.get_users_table()

        select_user = select([user_table]).where(user_table.c.id == user_id)
        user_result = self.connection.execute(select_user)
        user_result = user_result.fetchone()
        if user_result == None:
            response = {
                'code': 400,
                'msg': 'There is no user with this ID.'
            }
            return response
        select_query = select(['*']).select_from(tape_table.join(borrow_table)).where(and_(borrow_table.c.return_date == None, borrow_table.c.user_id == user_id))

        result = self.connection.execute(select_query)
        tapes = []
        for res in result:
            tape = Tape(input_tuple=res)
            tapes.append(tape.return_as_dict())

        return tapes