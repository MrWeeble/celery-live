import logging
import time

from celery import bootsteps

from celery_live.config import WORKER_LIVENESS_FILE, WORKER_LIVENESS_TIMEOUT

logger = logging.getLogger(__name__)


class LivenessProbe(bootsteps.StartStopStep):
    requires = {"celery.worker.components:Timer"}

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.requests = []
        self.tref = None

    def start(self, worker):
        self.tref = worker.timer.call_repeatedly(
            1.0,
            self.update_heartbeat_file,
            (worker,),
            priority=10,
        )

    def stop(self, worker):
        WORKER_LIVENESS_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):
        WORKER_LIVENESS_FILE.touch()


def enable_worker_liveness_checks(app):
    app.steps["worker"].add(LivenessProbe)


def check_worker_liveness():
    if not WORKER_LIVENESS_FILE.is_file():
        logger.warning(f"Liveness file {WORKER_LIVENESS_FILE} NOT found.")
        return False
    stats = WORKER_LIVENESS_FILE.stat()
    heartbeat_timestamp = stats.st_mtime
    current_timestamp = time.time()
    time_diff = current_timestamp - heartbeat_timestamp
    if time_diff > WORKER_LIVENESS_TIMEOUT:
        logger.warning(
            f"Liveness file not been touched for {time_diff} seconds which is more "
            f"than the configured timeout of {WORKER_LIVENESS_TIMEOUT} seconds."
        )
        return False
    logger.debug(
        f"Celery Worker last touched {time_diff} seconds ago, which is within the "
        f"configured timeout of {WORKER_LIVENESS_TIMEOUT} seconds."
    )
    return True
