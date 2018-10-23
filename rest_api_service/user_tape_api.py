from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG
from flask import Response

class UserTapeAPI(MethodView):

    # Gets information about the tapes a given user has on loan
    def get(self, user_id):
        pass

    # Registers tape on loan
    def post(self, user_id, tape_id):
        borrow = {
            'user_id': user_id,
            'tape_id': tape_id,
            'borrow_date': None,
            'return date': None
        }

        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.tape_service.register_tape(borrow)
            return(response['msg'], response['code'])
    #  Returns tape that was on loan
    def delete(self, user_id, tape_id):
        # TO DO: return the tape
        pass

    # Updates borrowing information
    def put(self, user_id, tape_id):
        # TO DO: update the tape information
        pass
