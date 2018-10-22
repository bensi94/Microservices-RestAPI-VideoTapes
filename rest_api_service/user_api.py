from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG

class UserAPI(MethodView):

    # Returns list of users if user_id is none
    # But spesific user by id if user is not None
    def get(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            user_service_result = rpc.user_service.on_hello()
            return (user_service_result)
        
        # if user_id is None:
        #     # TO DO: return list of users
        #     pass
        # else:
        #     pass
        #     # TO DO: return single user

    # Creates new user
    def post(self):
        # TO DO: Create user
        pass

    #  Deletes user by ID
    def delete(self, user_id):
        # TO DO: delete a single user
        pass

    # Updates user by ID
    def put(self, user_id):
        # TO DO: update a single user
        pass
        
