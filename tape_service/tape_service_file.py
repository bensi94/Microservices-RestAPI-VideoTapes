from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG

class Tape_service:

    def get_tapes(self):
        with ClusterRpcProxy(CONFIG) as rpc:
           return rpc.database_service.get_tapes()
    
    def get_tape(self, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_tape(tape_id=tape_id)