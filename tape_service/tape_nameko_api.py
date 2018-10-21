from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log

class Tape_Nameko_api:

    name = 'tape_service'
    entrypoint_logger = EntrypointLogger()

    @rpc
    def on_hello(self):
        _log.info('Hello world log!')
        return('Hello World return!')
