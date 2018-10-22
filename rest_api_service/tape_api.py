from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response, request
import json

class TapeAPI(MethodView):

    # Returns list of tapes if tape_id is none
    # But spesific tape by id if tape is not None
    def get(self, tape_id):
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
        title = request.args.get('title')

        if title is None:
            return ('Title is required!', 400)

        tape = {
            "title": request.args.get('title'),
            "director": request.args.get('director'),
            "type": request.args.get('type'),
            "release_date": request.args.get('release_date'),
            "eidr": request.args.get('eidr')
        }

        
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.tape_service.add_tape(tape)

        return(response)

    #  Deletes tape by ID
    def delete(self, tape_id):
        # TO DO: delete a single tape
        pass

    # Updates tape by ID
    def put(self, tape_id):
        # TO DO: update a single tape
        pass
