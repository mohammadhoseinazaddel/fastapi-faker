from .setup import router
from .worker import app


app.conf.beat_schedule = router.schedules()
