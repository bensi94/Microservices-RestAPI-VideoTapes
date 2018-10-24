from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response, request
import json

class UserAPI(MethodView):

    # Returns list of users if user_id is none
    # But spesific user by id if user is not None
    def get(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            if user_id is None:
                users = rpc.user_service.get_users()
                return Response(json.dumps(users), mimetype='application/json')
            else:
                user = rpc.user_service.get_user(user_id = user_id)

                if user is not None:
                    return Response(json.dumps(user), mimetype='application/json')
        
        return('User not found!', 404)
        
    # Creates new user
    def post(self):
        user = {
            'name': request.args.get('name'),
            'email': request.args.get('email'),
            'phone': request.args.get('phone'),
            'address': request.args.get('address')
        }

        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.user_service.add_user(user)
            return(response['msg'], response['code'])
    #  Deletes user by ID
    def delete(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.user_service.delete_user(user_id)
            return(response['msg'], response['code'])

    # Updates user by ID
    def put(self, user_id):
        user = {
            'name':request.args.get('name'),
            'email':request.args.get('email'),
            'phone':request.args.get('phone'),
            'address':request.args.get('address')
        }

        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.user_service.update_user(user_id, user)
            return(response['msg'], response['code'])
        
