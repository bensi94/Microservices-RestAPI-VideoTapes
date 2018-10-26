from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response, request
import json

class TapeAPI(MethodView):

    # Returns list of tapes if tape_id is none
    # But spesific tape by id if tape is not None
    def get(self, tape_id):
        
        
        loan_date = request.args.get('loan_date')
        loan_duration = request.args.get('loan_duration')
        if loan_date is not None and loan_duration is not None:
            with ClusterRpcProxy(CONFIG) as rpc:
                on_loan = rpc.tape_service.on_loan_for_and_at(loan_date, loan_duration)
                if isinstance(on_loan, list):
                    if on_loan == []:
                        return ('No tapes were on loan that date', 200)
                    return Response(json.dumps(on_loan), mimetype='application/json')
                return(on_loan['msg'], on_loan['code'])
        
        if loan_date is not None:
            with ClusterRpcProxy(CONFIG) as rpc:
                on_loan = rpc.tape_service.on_loan_at(loan_date)
                if isinstance(on_loan, list):
                    if on_loan == []:
                        return ('No tapes were on loan that date', 200)
                    return Response(json.dumps(on_loan), mimetype='application/json')
                return(on_loan['msg'], on_loan['code'])
        
        if loan_duration is not None:
            with ClusterRpcProxy(CONFIG) as rpc:
                response = rpc.tape_service.on_loan_for(loan_duration)
                if isinstance(response, list):
                    if response == []:
                        return ('No tapes have been on loan for that duration', 200)
                    return Response(json.dumps(response), mimetype='application/json')
                return(response['msg'], response['code'])


        
        with ClusterRpcProxy(CONFIG) as rpc:
            if tape_id is None:
                tapes = rpc.tape_service.get_tapes()
                if tapes is not None:
                    return Response(json.dumps(tapes),  mimetype='application/json') 
            else:
                tape = rpc.tape_service.get_tape(tape_id=tape_id)

                if tape is not None:
                    return  Response(json.dumps(tape),  mimetype='application/json') 

        return ('Tape not found!', 404)
            
    # Creates new tape
    def post(self):
        tape = {
            "title": request.args.get('title'),
            "director": request.args.get('director'),
            "type": request.args.get('type'),
            "release_date": request.args.get('release_date'),
            "eidr": request.args.get('eidr')
        }
        
        with ClusterRpcProxy(CONFIG) as rpc:
             response = rpc.tape_service.add_tape(tape)
             return(response['msg'], response['code'])
             
    #  Deletes tape by ID
    def delete(self, tape_id):
       with ClusterRpcProxy(CONFIG) as rpc:
           response = rpc.tape_service.delete_tape(tape_id)
           return(response['msg'], response['code'])

    # Updates tape by ID
    def put(self, tape_id):
        tape = {
            "title": request.args.get('title'),
            "director": request.args.get('director'),
            "type": request.args.get('type'),
            "release_date": request.args.get('release_date'),
            "eidr": request.args.get('eidr')
        }

        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.tape_service.update_tape(tape_id, tape)
            return(response['msg'], response['code'])
        
