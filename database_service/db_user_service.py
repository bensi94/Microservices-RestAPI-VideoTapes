from sqlalchemy import select, insert, func, and_, update, or_
from shared_utils.logger import _log
from entity_classes.user import User
from entity_classes.tape import Tape
from database_service.database_utils import Database_utils
from datetime import datetime, date
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
            self.delete_reviews(user_id)
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

    # Delete users from borrws, if user_id is set
    # it only deletes as single review, otherwise all
    def delete_borrow(self, user_id, tape_id=None):
        borrow_table = self.tables.get_borrow_table()
        
        # Delete all borrows of user
        if tape_id is None:
            self.connection.execute(borrow_table.delete().where(
                borrow_table.c.user_id == user_id))
        # Delete borrow of user by single tape
        else:
             self.connection.execute(borrow_table.delete().where(and_(
                 borrow_table.c.user_id == user_id, borrow_table.c.tape_id == tape_id)))

    # Delete users from reveiws, if tape_id is set
    # it only deletes as single review, otherwise all
    def delete_reviews(self, user_id, tape_id=None):
        review_table = self.tables.get_review_table()

        # Delete all reviews of tape
        if tape_id is None:
            self.connection.execute(review_table.delete().where(
                review_table.c.user_id == user_id))
        # Delete review of tape by single user
        else:
             self.connection.execute(review_table.delete().where(and_(
                 review_table.c.user_id == user_id, review_table.c.tape_id == tape_id)))

    def get_user_reviews(self, user_id):
        users_table = self.tables.get_users_table()
        tapes_table = self.tables.get_tapes_table()
        review_table = self.tables.get_review_table()

        user_query = select(['*']).select_from(users_table).where(
            users_table.c.id == user_id
        )

        user_res = self.connection.execute(user_query)

        user_res = user_res.fetchone()

        if user_res is None:
            return None
        
        user = User(input_tuple=user_res)

        result_dict = user.return_as_dict()
        
        get_query = select(['*']).select_from(
            tapes_table.join(review_table)).where(review_table.c.user_id == user_id)

        result = self.connection.execute(get_query)

        results = []
        for res in result:
            tape = Tape(input_tuple=res)
            review_dict = tape.return_as_dict()
            review_dict['rating'] = res[-1]
            results.append(review_dict)
            _log.info(review_dict)

        result_dict['Reviews'] = results

        if len(results) == 0:
            result_dict['Reviews'] = 'No review for this user'

        return result_dict


    def on_loan_at(self, loan_date):
        borrow_table = self.tables.get_borrow_table()
        user_table = self.tables.get_users_table()

        select_query = select(['*']).select_from(user_table.join(borrow_table)).where(
            and_(borrow_table.c.borrow_date <= loan_date, or_(borrow_table.c.return_date > loan_date, borrow_table.c.return_date == None)))
        
        loan_res = self.connection.execute(select_query)

        users = []
        for res in loan_res:
            user = User(input_tuple=res)
            users.append(user.return_as_dict())

        return users
    
    def on_loan_for(self, loan_duration):
        today = datetime.today().strftime('%Y-%m-%d')
        dur_res = self.connection.execute('SELECT * FROM users JOIN borrows ON users.id = borrows.user_id WHERE borrows.return_date IS NULL AND (borrows.borrow_date + \' '+ str(loan_duration) + ' day\'::interval) < \'' + str(today) +'\'')

        users = []
        for res in dur_res:
            user = User(input_tuple=res)
            users.append(user.return_as_dict())

        return users
    
    def on_loan_for_and_at(self, loan_date, loan_duration):
        query = 'SELECT * FROM users JOIN borrows ON users.id = borrows.user_id WHERE (borrows.borrow_date + \''+ str(loan_duration) + 'day\'::interval) < \''+ str(loan_date)+'\'AND (borrows.return_date > \''+str(loan_date)+'\' OR borrows.return_date IS NULL)'
        _log.info(query)
        loan_res = self.connection.execute(query)

        users = []
        for res in loan_res:
            user = User(input_tuple=res)
            users.append(user.return_as_dict())

        return users

    def add_review(self, review):
        review_table = self.tables.get_review_table()

        validation = self.validate_review(review)

        if validation != 'valid':
            return validation


        if self.check_reveiew_exist(review) is not None:
            response = {
                'msg': 'Review already exist for this tape',
                'code': 400
            }
            return response

        review_id = self.connection.execute(review_table.insert(), review).inserted_primary_key[0]

        review['id'] = review_id

        response = {
            'msg': json.dumps(review),
            'code': 200
        }

        return response

    def update_review(self, review):
        tape_id = review['tape_id']
        user_id = review['user_id']
        review_table = self.tables.get_review_table()

        validation = self.validate_review(review)
        if validation != 'valid':
            return validation

        if self.check_reveiew_exist(review) is None:
            response = {
                'msg': 'Review does not exist for this tape',
                'code': 400
            }
            return response
        
        self.connection.execute(
            review_table.update().where(and_(review_table.c.tape_id == tape_id, 
            review_table.c.user_id == user_id )), review)

        review_id_query = select([review_table.c.id]).where(and_(
            review_table.c.tape_id == tape_id, review_table.c.user_id == user_id
        ))
        review_id = self.connection.execute(review_id_query).scalar()        

        review['id'] = review_id

        response = {
            'msg': json.dumps(review),
            'code': 200
        }

        return response

    def delete_review(self, user_id, tape_id):
        review_taple = self.tables.get_review_table()
        
        # Just used for the check that takes in review
        review = {
            'user_id': user_id,
            'tape_id': tape_id
        }

        validation = self.validate_review(review)
        if validation != 'valid':
            return validation

        if self.check_reveiew_exist(review) is None:
            response = {
                'msg': 'Review does not exist for this tape',
                'code': 400
            }
            return response

        self.connection.execute(
            review_taple.delete().where(and_(
                review_taple.c.user_id == user_id, 
                review_taple.c.tape_id == tape_id)))

        response = {
            'code': 200,
            'msg': 'Review with user ID:' + str(user_id) + ' and tape ID:' + str(tape_id) + ' deleted'
        }

        return response
        
        

    def check_reveiew_exist(self, review):
        tape_id = review['tape_id']
        user_id = review['user_id']
        review_table = self.tables.get_review_table()

        # Checks that reveiw exists in table
        review_query = select(['*']).select_from(review_table).where(and_(
            review_table.c.tape_id == tape_id, review_table.c.user_id == user_id
        ))
        review_res = self.connection.execute(review_query)
        return review_res.fetchone()

    def validate_review(self, review):
        tape_id = review['tape_id']
        user_id = review['user_id']
        users_table = self.tables.get_users_table()
        tapes_table = self.tables.get_tapes_table()

        # Checks that user_id exists
        user_query = select(['*']).select_from(users_table).where(
            users_table.c.id == user_id
        )
        user_res = self.connection.execute(user_query)
        user_res = user_res.fetchone()
        if user_res is None:
            response = {
                'msg': 'User ID does not exist!',
                'code': 404
            }
            return response

        # Checks that tape_id exists
        tape_query = select(['*']).select_from(tapes_table).where(
            tapes_table.c.id == tape_id
        )
        tape_res = self.connection.execute(tape_query)
        tape_res = tape_res.fetchone()
        if tape_res is None:
            response = {
                'msg': 'Tape ID does not exist!',
                'code': 404
            }
            return response
        
        return 'valid'
