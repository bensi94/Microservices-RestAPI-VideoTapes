from database_service.db_service import Database_service
from database_service.db_tape_service import Database_tape_service
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

    @rpc
    def get_tapes(self):
        return self.db_tape_service.get_tapes()
    
    @rpc
    def get_tape(self, tape_id):
        return self.db_tape_service.get_tape(tape_id)

    @rpc
    def add_tape(self, tape):
        return self.db_tape_service.add_tape(tape)

