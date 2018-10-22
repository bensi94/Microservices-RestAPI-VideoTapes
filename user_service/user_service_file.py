from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG

class User_service:

    def get_users(self):
        with ClusterRpcProxy(CONFIG) as rpc:
           return rpc.database_service.get_users()