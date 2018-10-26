from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response
import json

class RecommendationAPI(MethodView):

    # Returns a recommendation for user
    def get(self, user_id):
         with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.recommendation_service.get_recommendation(user_id)
            if not isinstance(response, dict): 
                return Response(json.dumps(response),  mimetype='application/json')
            else:
                return(response['msg'], response['code'])
