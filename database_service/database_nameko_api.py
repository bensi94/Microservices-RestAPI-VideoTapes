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
    def get_users(self):
        return self.db_user_service.get_users()

    @rpc
    def get_user(self, user_id):
        return self.db_user_service.get_user(user_id)
    
    @rpc
    def add_user(self, user):
        return self.db_user_service.add_user(user)

    @rpc
    def delete_user(self, user_id):
        return self.db_user_service.delete_user(user_id)
    
    @rpc
    def update_user(self, user_id, user):
        return self.db_user_service.update_user(user_id, user)
    
    @rpc
    def get_tapes(self):
        return self.db_tape_service.get_tapes()
    
    @rpc
    def get_tape(self, tape_id):
        return self.db_tape_service.get_tape(tape_id)

    @rpc
    def add_tape(self, tape):
        return self.db_tape_service.add_tape(tape)

    @rpc 
    def delete_tape(self, tape_id):
        return self.db_tape_service.delete_tape(tape_id)

    @rpc 
    def update_tape(self, tape_id, tape):
        return self.db_tape_service.update_tape(tape_id, tape)

    #ONLY USED FOR TESTING, HANDLE WITH CARE
    @rpc
    def delete_and_populate(self):
        return self.database_service.delete_and_populate()
        
