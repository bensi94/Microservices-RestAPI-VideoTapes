from flask.views import MethodView

class UserTapeAPI(MethodView):

    # Gets information about the tapes a given user has on loan
    def get(self, user_id):
        # TO DO: return loan information
        pass

    # Registers tape on loan
    def post(self, user_id, tape_id):
        # TO DO: register tape
        pass

    #  Returns tape that was on loan
    def delete(self, user_id, tape_id):
        # TO DO: return the tape
        pass

    # Updates borrowing information
    def put(self, user_id, tape_id):
        # TO DO: update the tape information
        pass
