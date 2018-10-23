from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
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