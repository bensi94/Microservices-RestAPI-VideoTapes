from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response
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
        # TO DO: Create tape
        pass

    #  Deletes tape by ID
    def delete(self, tape_id):
        # TO DO: delete a single tape
        pass

    # Updates tape by ID
    def put(self, tape_id):
        # TO DO: update a single tape
        pass