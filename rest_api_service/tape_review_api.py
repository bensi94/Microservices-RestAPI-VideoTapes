from flask.views import MethodView


class TapeReviewAPI(MethodView):

    # Returns reviews of tape if user_id is None
    # But reviews of tape by spesific user if user_id is not None
    def get(self, tape_id, user_id):
        if tape_id is None:
            # TO DO: return list of reviews 
            pass
        else:
            pass
            # TO DO: return reveiws for given user

    #  Deletes review by user and tape ID
    def delete(self, tape_id, user_id):
        # TO DO: delete review
        pass

    # Updates reveiw by user and tape ID
    def put(self, tape_id, user_id):
        # TO DO: update review
        pass
