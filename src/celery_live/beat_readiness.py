from celery.signals import beat_init

from celery_live.config import BEAT_READINESS_FILE


def on_beat_ready(*_, **__):
    BEAT_READINESS_FILE.touch()


def check_beat_readiness():
    return BEAT_READINESS_FILE.exists()


def enable_beat_readiness_checks(app):
    beat_init.connect(on_beat_ready)
