from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.config import CONFIG


class Recomenndation_Nameko_api:
    "Very simple api that sends query to the database"

    name = 'recommendation_service'
    entrypoint_logger = EntrypointLogger()

    @rpc
    def get_recommendation(self, user_id):
        with ClusterRpcProxy(CONFIG) as rpc:
            response = rpc.database_service.get_recommendation(user_id)
            return response
