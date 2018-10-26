from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from entity_classes.tape import Tape
from datetime import datetime
import re

class Tape_service:

    def get_tapes(self):
        with ClusterRpcProxy(CONFIG) as rpc:
           return rpc.database_service.get_tapes()
    
    def get_tape(self, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_tape(tape_id=tape_id)
    
    def add_tape(self, tape):
        validation, msg = self.validate_tape(tape)
        if validation:
            tape['release_date'] = datetime.strptime(
                tape['release_date'], '%Y-%m-%d')
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.database_service.add_tape(tape)
        else:
            response = {
                'code': 400,
                'msg': msg
            }

        return response

    def delete_tape(self, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.delete_tape(tape_id=tape_id)

    def update_tape(self, tape_id, tape):
        validation, msg = self.validate_tape(tape)

        if validation:
            tape['release_date'] = datetime.strptime(tape['release_date'], '%Y-%m-%d')
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.database_service.update_tape(tape_id, tape)
        else:
            response = {
                'code': 400,
                'msg': msg
            }
        return response


    def validate_tape(self, tape):
        if tape['title'] is None:
            return False, 'Title is required'
        
        if tape['release_date'] is not None:
            pattern = re.compile('^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$')

            if not pattern.match(tape['release_date']):
                return False, 'Invalid date'

        pattern = re.compile('^10.5240/(([A-Z]|[0-9]){4}-){5}[A-Z]$')

        if not pattern.match(tape['eidr']):
            return False, 'Invalid eidr'

        return True, ''
    
    def register_tape(self, borrow):
        borrow['borrow_date'] = datetime.today().strftime('%Y-%m-%d')
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.register_tape(borrow)
            return response
    
    def return_tape(self, user_id, tape_id):
        return_date = datetime.today().strftime('%Y-%m-%d')
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.return_tape(return_date, user_id, tape_id)
            return response
            
    def update_registration(self, borrow):
        pattern = re.compile('^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$')
        if borrow['return_date'] is not None:
            if not pattern.match(borrow['return_date']):
                response = {
                    'code': 400,
                    'msg': 'Invalid date format for return_date'
                }
                return response
            borrow['return_date'] = datetime.strptime(borrow['return_date'], '%Y-%m-%d')
        if not pattern.match(borrow['borrow_date']):
            response = {
                'code': 400,
                'msg': 'Invalid date format for borrow_date'
            }
            return response
        with ClusterRpcProxy(CONFIG) as rpc:
            borrow['borrow_date'] = datetime.strptime(borrow['borrow_date'], '%Y-%m-%d')
            response = rpc.database_service.update_registration(borrow)
            return response
    
    def get_tapes_of_user(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.get_tapes_of_user(user_id)
            return response
        

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
            response = rpc.database_service.on_loan_at_tapes(loan_date)
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
            response = rpc.database_service.on_loan_for_tapes(loan_duration)
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
            response = rpc.database_service.on_loan_for_and_at_tapes(loan_date, loan_duration)
            return response