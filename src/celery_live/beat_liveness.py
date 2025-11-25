import logging

from celery_live.config import BEAT_PID_FILE

logger = logging.getLogger(__name__)


def check_beat_liveness():
    if not BEAT_PID_FILE.is_file():
        logger.warning("Celery beat PID file NOT found.")
        return False
    logger.debug("Celery beat PID file found.")

    return True


def enable_beat_liveness_checks(app):
    pass
