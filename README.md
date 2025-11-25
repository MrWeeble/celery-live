Celery Live
===========

Celery Live is a library for monitoring the health of Celery workers and beat.
Designed to be easy to use with kubernetes, it is heavily based on 
[this blog post](https://medium.com/ambient-innovation/health-checks-for-celery-in-kubernetes-cf3274a3e106)
but packaged for easy deployment.

Usage
=====

In your celery app, add the following code:

```python
from celery import Celery
from celery_live import (
    enable_beat_liveness_checks,
    enable_beat_readiness_checks,
    enable_worker_liveness_checks,
    enable_worker_readiness_checks,
)

app = Celery("ptk_connect")

enable_beat_readiness_checks(app)
enable_worker_readiness_checks(app)
enable_beat_liveness_checks(app)
enable_worker_liveness_checks(app)
```

You can then run these commands to determine liveness or readiness state of beat or worker
 * celery-live beat live
 * celery-live beat ready
 * celery-live worker live
 * celery-live worker ready

this would be configured in kubernetes like
```yaml
    livenessProbe:
      exec:
        command:
        - celery-live
        - worker
        - live
      initialDelaySeconds: 5
      periodSeconds: 5
```