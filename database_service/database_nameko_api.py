from database_service.db_service import Database_service
from database_service.db_tape_service import Database_tape_service
from database_service.db_user_service import Database_user_service
from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log



class Database_Nameko_api:
    """
        Database Microservice:
        This microservice handles the communications with the database through the nemko_api
    """

    name = 'database_service'

    entrypoint_logger = EntrypointLogger()

    ## Init database
    database_service = Database_service()
    database_service.init_database()

    # Connections and tables used in all db services
    connection = database_service.get_connection()
    tables = database_service.get_tables()

    db_tape_service = Database_tape_service(connection, tables)
    db_user_service = Database_user_service(connection, tables)

    @rpc
    def get_tapes(self):
        return self.db_tape_service.get_tapes()
    
    @rpc
    def get_users(self):
        return self.db_user_service.get_users()

