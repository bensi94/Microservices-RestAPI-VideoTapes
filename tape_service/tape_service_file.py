from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from entity_classes.tape import Tape
from datetime import datetime

class Tape_service:

    def get_tapes(self):
        with ClusterRpcProxy(CONFIG) as rpc:
           return rpc.database_service.get_tapes()
    
    def get_tape(self, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_tape(tape_id=tape_id)
    
    def add_tape(self, tape):   
        try:
            tape['release_date'] = datetime.strptime(tape['release_date'], '%Y-%m-%d')
        except ValueError:
            return ('Invalid date', 400)

        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.add_tape(tape)
