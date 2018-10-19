from database_service.db_service import Database_service
from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log



class Database_Nameko_api:
    """
        Database Microservice:
        This microservice handles the communications with the database through the nemko_api
    """

    name = 'database_service'

    entrypoint_logger = EntrypointLogger()

    database_service = Database_service()
    database_service.init_database()

    @rpc
    def on_hello(self):
        _log.info('MY LOGGING')
        return("ZUP")
