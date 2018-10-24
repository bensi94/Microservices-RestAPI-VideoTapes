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
            pattern = re.compile('^[0-9]{4}-(((01|03|05|07|08|10|12)-([1-2][0-9]|3[0-1]))|((04|06|09|11)-([1-2][0-9]|30))|02-[1-2][0-9])$')

            if not pattern.match(tape['release_date']):
                return False, 'Invalid date'

        pattern = re.compile('^10.5240/(([A-Z]|[0-9]){4}-){5}[A-Z]$')

        if not pattern.match(tape['eidr']):
            return False, 'Invalid eidr'

        return True, ''
    
    def register_tape(self, borrow):
        borrow['borrow_date'] = datetime.datetime.today().strftime('%Y-%m-%d')
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.register_tape(borrow)
