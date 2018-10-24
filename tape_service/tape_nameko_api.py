from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log
from tape_service.tape_service_file import Tape_service

class Tape_Nameko_api:

    name = 'tape_service'
    entrypoint_logger = EntrypointLogger()
    tape_service = Tape_service()

    @rpc
    def get_tapes(self):
        return self.tape_service.get_tapes()

    @rpc
    def get_tape(self, tape_id):
        return self.tape_service.get_tape(tape_id)

    @rpc
    def add_tape(self, tape):
        return self.tape_service.add_tape(tape)

    @rpc
    def delete_tape(self, tape_id):
        return self.tape_service.delete_tape(tape_id)

    @rpc
    def update_tape(self, tape_id, tape):
        return self.tape_service.update_tape(tape_id, tape)
    
    @rpc
    def register_tape(self, borrow):
        return self.tape_service.register_tape(borrow)
    
    @rpc
    def return_tape(self, user_id, tape_id):
        return self.tape_service.return_tape(user_id, tape_id)

    @rpc
    def update_registration(self, borrow):
        return self.tape_service.update_registration(borrow)