import click

from celery_live.beat_liveness import check_beat_liveness
from celery_live.beat_readiness import check_beat_readiness
from celery_live.worker_liveness import check_worker_liveness
from celery_live.worker_readiness import check_worker_readiness

checks = {
    "worker": {
        "live": check_worker_liveness,
        "ready": check_worker_readiness,
    },
    "beat": {
        "live": check_beat_liveness,
        "ready": check_beat_readiness,
    },
}


@click.command()
@click.argument("service")
@click.argument("check_type")
def check(service, check_type):
    try:
        service_checks = checks[service]
    except KeyError:
        raise click.UsageError(
            f"Invalid service. Must be one of {sorted(checks.keys())}"
        )

    try:
        check = service_checks[check_type]
    except KeyError:
        raise click.UsageError(
            f"Invalid check type. Must be one of {sorted(service_checks.keys())}"
        )

    status = check()
    if status:
        click.echo("OK")
        exit(0)
    else:
        click.echo("NOT OK")
        exit(1)


if __name__ == "__main__":
    check()
