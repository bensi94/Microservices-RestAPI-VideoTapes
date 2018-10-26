from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from datetime import datetime
import re

class User_service:

    def get_users(self):
        with ClusterRpcProxy(CONFIG) as rpc:
           return rpc.database_service.get_users()

    def get_user(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_user(user_id=user_id)
            
    def add_user(self, user):
        validation, msg = self.validate_user(user)

        if validation:
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.database_service.add_user(user)
        else:
            response = {
                'code': 400,
                'msg': msg
            }
        return response
    
    def delete_user(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.delete_user(user_id=user_id)
    
    def update_user(self, user_id, user):
        validation, msg = self.validate_user(user)

        if validation:
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.database_service.update_user(user_id, user)
        else:
            response = {
                'code': 400,
                'msg': msg
            }
        return response
        
    def validate_user(self, user):
        if user['name'] is None:
            return False, 'Name is required'
        if user['email'] is not None:
            pattern = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')

            if not pattern.match(user['email']):
                return False, 'Invalid email format.'
        
        pattern = re.compile('^[0-9]*$')

        if not pattern.match(user['phone']):
            return False, 'Invalid phone number format'
        
        return True, ''
    
    def on_loan_at(self, loan_date):
        pattern = re.compile('^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$')

        if not pattern.match(loan_date):
            response = {
                'code': 400,
                'msg': 'Invalid date format.'
            }
            return response
        loan_date = datetime.strptime(loan_date, '%Y-%m-%d')
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.on_loan_at(loan_date)
            return response
    
    def on_loan_for(self, loan_duration):
        if not loan_duration.isdigit():
            response = {
                'code': 400,
                'msg': 'The duration must be an integer'
            }
            return response
        with ClusterRpcProxy(CONFIG) as rpc:
            loan_duration = int(loan_duration)
            response = rpc.database_service.on_loan_for(loan_duration)
            return response

    def on_loan_for_and_at(self, loan_date, loan_duration):
        if not loan_duration.isdigit():
            response = {
                'code': 400,
                'msg': 'The duration must be an integer'
            }
            return response
        
        pattern = re.compile('^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$')

        if not pattern.match(loan_date):
            response = {
                'code': 400,
                'msg': 'Invalid date format.'
            }
            return response
        loan_date = datetime.strptime(loan_date, '%Y-%m-%d')
        
        with ClusterRpcProxy(CONFIG) as rpc:
            loan_duration = int(loan_duration)
            response = rpc.database_service.on_loan_for_and_at(loan_date, loan_duration)
            return response