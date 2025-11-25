from celery.signals import worker_ready, worker_shutdown

from celery_live.config import WORKER_READINESS_FILE


def on_worker_ready(*_, **__):
    WORKER_READINESS_FILE.touch()


def on_worker_shutdown(*_, **__):
    WORKER_READINESS_FILE.unlink(missing_ok=True)


def check_worker_readiness():
    return WORKER_READINESS_FILE.exists()


def enable_worker_readiness_checks(app):
    worker_ready.connect(on_worker_ready)
    worker_shutdown.connect(on_worker_shutdown)
