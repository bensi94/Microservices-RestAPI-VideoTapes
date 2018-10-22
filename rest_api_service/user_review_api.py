from flask.views import MethodView


class UserReviewAPI(MethodView):

    # Returns reviews by user if tape_id is None
    # But reviews by user of spesific tape if tape is not None
    def get(self, user_id, tape_id):
        if tape_id is None:
            # TO DO: return list of reviews
            pass
        else:
            pass
            # TO DO: return user reveiws for given tape

    # Creates new review of a tape
    def post(self, user_id, tape_id):
        # TO DO: Create review
        pass

    #  Deletes review by user and tape ID
    def delete(self, user_id, tape_id):
        # TO DO: delete review
        pass

    # Updates reveiw by user and tape ID
    def put(self, user_id, tape_id):
        # TO DO: update review
        pass
