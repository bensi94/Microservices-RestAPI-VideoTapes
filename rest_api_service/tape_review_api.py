from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response, request
import json

class TapeReviewAPI(MethodView):

    # Returns reviews of tape if user_id is None
    # But reviews of tape by spesific user if user_id is not None
    def get(self, tape_id, user_id):
         with ClusterRpcProxy(CONFIG) as rpc:
            if tape_id is None:
                all_reviews = rpc.review_service.get_all_reviews()
                return Response(json.dumps(all_reviews), mimetype='application/json')
            else:
                if user_id is None:
                    tape_reviews=rpc.review_service.get_tape_reviews(tape_id)
                    return Response(json.dumps(tape_reviews), mimetype='application/json')
                else:
                    review=rpc.review_service.get_review(tape_id, user_id)
                    if review is None:
                        return('User id not found')
                    return Response(json.dumps(review), mimetype='application/json')

    #  Deletes review by user and tape ID
    def delete(self, tape_id, user_id):
        # TO DO: delete review
        pass

    # Updates reveiw by user and tape ID
    def put(self, tape_id, user_id):
        # TO DO: update review
        pass
