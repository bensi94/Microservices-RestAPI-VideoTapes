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
    
    def add_review(self, review):

        if self.validate_review(review):
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.database_service.add_review(review)
        else:
            response = {
                'msg': 'Invalid review!, rating has to be an integer between 1 and 10!',
                'code': 400
            }
        return response

    def update_review(self, review):
        if self.validate_review(review):
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.database_service.update_review(review)
        else:
            response = {
                'msg': 'Invalid review!, rating has to be an integer between 1 and 10!',
                'code': 400
            }
        return response
    

    # Checks that review is int between 1 and 10
    def validate_review(self, review):
        rating = review['rating']
        if rating.isdigit():
            rating = int(rating)
            if  rating > 0 and rating <= 10:
                return True
                
        return False

    def delete_review(self, user_id, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.delete_review(user_id, tape_id)
            _log.info("RESPONSE: " )
            _log.info(response)
            return response
