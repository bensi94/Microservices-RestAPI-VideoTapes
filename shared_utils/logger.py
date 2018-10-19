from nameko.extensions import DependencyProvider
import logging
import weakref
import time

_log = logging.getLogger(__name__)

class EntrypointLogger(DependencyProvider):

    def setup(self):
        self.entrypoint_starts = weakref.WeakKeyDictionary()

    def worker_setup(self, worker_ctx):
        _log.info('Starting execution of {}'.format(worker_ctx.entrypoint))
        self.entrypoint_starts[worker_ctx] = time.perf_counter()

    def worker_result(self, worker_ctx, result=None, exc_info=None):
        _log.info('Completed execution of {}'.format(worker_ctx.entrypoint))

