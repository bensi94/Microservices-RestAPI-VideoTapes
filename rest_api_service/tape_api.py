from flask.views import MethodView


class TapeAPI(MethodView):

    # Returns list of tapes if tape_id is none
    # But spesific tape by id if tape is not None
    def get(self, tape_id):
        if tape_id is None:
            # TO DO: return list of tapes
            pass
        else:
            pass
            # TO DO: return single tape

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
