from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log

class Recomenndation_Nameko_api:

    name = 'recommendation_service'
    entrypoint_logger = EntrypointLogger()

    @rpc
    def on_hello(self):
        _log.info('Hello world log!')
        return('Hello World return!')
