from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response, request
import json

class UserReviewAPI(MethodView):

    # Returns reviews by user if tape_id is None
    # But reviews by user of spesific tape if tape is not None
    def get(self, user_id, tape_id):
         with ClusterRpcProxy(CONFIG) as rpc:
            if tape_id is None:
                user_reviews = rpc.review_service.get_user_reviews(user_id)
                return Response(json.dumps(user_reviews), mimetype='application/json')
            else:
                review = rpc.review_service.get_review(tape_id, user_id)
                return Response(json.dumps(review), mimetype='application/json')

    # Creates new review of a tape
    def post(self, user_id, tape_id):
        review = {
            "rating": request.args.get('rating'),
            "user_id": user_id,
            "tape_id": tape_id
        }
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.review_service.add_review(review)
            return(response['msg'], response['code'])

    #  Deletes review by user and tape ID
    def delete(self, user_id, tape_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.review_service.delete_review(user_id, tape_id)
            return(response['msg'], response['code'])

    # Updates reveiw by user and tape ID
    def put(self, user_id, tape_id):
        review = {
            "rating": request.args.get('rating'),
            "user_id": user_id,
            "tape_id": tape_id
        }
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.review_service.update_review(review)
            return(response['msg'], response['code'])
        
