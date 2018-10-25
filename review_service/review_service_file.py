from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from shared_utils.logger import EntrypointLogger, _log

class ReviewService:

    def get_all_reviews(self):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_all_reviews()

    
    def get_tape_reviews(self, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_tape_reviews(tape_id)

    
    def get_user_reviews(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_user_reviews(user_id)

    
    def get_review(self, tape_id, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            return rpc.database_service.get_review(tape_id, user_id)
