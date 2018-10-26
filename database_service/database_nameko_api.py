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

    @rpc
    def register_tape(self, borrow):
        return self.db_tape_service.register_tape(borrow)
    
    @rpc
    def return_tape(self, return_date, user_id, tape_id):
        return self.db_tape_service.return_tape(return_date, user_id, tape_id)
    
    @rpc
    def update_registration(self, borrow):
        return self.db_tape_service.update_registration(borrow)

    @rpc
    def get_tapes_of_user(self, user_id):
        return self.db_tape_service.get_tapes_of_user(user_id)

    @rpc
    def get_all_reviews(self):
        return self.db_tape_service.get_all_reviews()

    @rpc
    def get_tape_reviews(self, tape_id):
        return self.db_tape_service.get_tape_reviews(tape_id)

    @rpc
    def get_user_reviews(self, user_id):
        return self.db_user_service.get_user_reviews(user_id)

    @rpc
    def get_review(self, tape_id, user_id):
        return self.db_tape_service.get_review(tape_id, user_id)
 
    @rpc
    def on_loan_at(self, loan_date):
        return self.db_user_service.on_loan_at(loan_date)

    @rpc
    def on_loan_for(self, loan_duration):
        return self.db_user_service.on_loan_for(loan_duration)
    
    @rpc
    def add_review(self, review):
        return self.db_user_service.add_review(review)
    
    @rpc
    def update_review(self, review):
        return self.db_user_service.update_review(review)
    
    @rpc
    def delete_review(self, user_id, tape_id):
        return self.db_user_service.delete_review(user_id, tape_id)
    @rpc
    def on_loan_for_and_at(self, loan_date, loan_duration):
        return self.db_user_service.on_loan_for_and_at(loan_date, loan_duration)
    @rpc
    def get_recommendation(self, user_id):
        return self.db_user_service.get_recommendation(user_id)
    
    #ONLY USED FOR TESTING, HANDLE WITH CARE
    @rpc
    def delete_and_populate(self):
        return self.database_service.delete_and_populate()
        
