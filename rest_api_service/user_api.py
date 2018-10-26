from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response, request
import json

class UserAPI(MethodView):

    # Returns list of users if user_id is none
    # But spesific user by id if user is not None
    def get(self, user_id):
        
        loan_date = request.args.get('loan_date')
        loan_duration = request.args.get('loan_duration')
        if loan_date is not None and loan_duration is not None:
            with ClusterRpcProxy(CONFIG) as rpc:
                on_loan = rpc.user_service.on_loan_for_and_at(loan_date, loan_duration)
                if isinstance(on_loan, list):
                    if on_loan == []:
                        return ('No user had tapes on loan that date', 200)
                    return Response(json.dumps(on_loan), mimetype='application/json')
                return(on_loan['msg'], on_loan['code'])
        
        if loan_date is not None:
            with ClusterRpcProxy(CONFIG) as rpc:
                on_loan = rpc.user_service.on_loan_at(loan_date)
                if isinstance(on_loan, list):
                    if on_loan == []:
                        return ('No user had tapes on loan that date', 200)
                    return Response(json.dumps(on_loan), mimetype='application/json')
                return(on_loan['msg'], on_loan['code'])
        
        if loan_duration is not None:
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.user_service.on_loan_for(loan_duration)
                if isinstance(response, list):
                    if response == []:
                        return ('No users have had a tape on loan for that duration', 200)
                    return Response(json.dumps(response), mimetype='application/json')
                return(response['msg'], response['code'])
    

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
        
