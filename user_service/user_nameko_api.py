from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log
from user_service.user_service_file import User_service

class User_Nameko_api:

    name = 'user_service'
    entrypoint_logger = EntrypointLogger()
    user_service = User_service()

    @rpc
    def get_users(self):
        return self.user_service.get_users()
    @rpc
    def get_user(self, user_id):
        return self.user_service.get_user(user_id)

    @rpc
    def add_user(self, user):
        return self.user_service.add_user(user)

    @rpc
    def delete_user(self, user_id):
        return self.user_service.delete_user(user_id)
    
    @rpc
    def update_user(self, user_id, user):
        return self.user_service.update_user(user_id, user)

    @rpc
    def on_loan_at(self, loan_date):
        return self.user_service.on_loan_at(loan_date)
    
    @rpc
    def on_loan_for(self, loan_duration):
        return self.user_service.on_loan_for(loan_duration)
    
    @rpc
    def on_loan_for_and_at(self, loan_date, loan_duration):
        return self.user_service.on_loan_for_and_at(loan_date, loan_duration)