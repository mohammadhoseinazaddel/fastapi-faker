import asyncio

from sqlalchemy.orm import sessionmaker, scoped_session

from notification.notification_service import NotificationService
from system.celery import app
from system.dbs.postgre import engine

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)  # to open a session and reuse it for this periodic task
db = Session()

notification_sr = NotificationService()


@app.task
def send_sms():
    try:
        # use async to handle requests parallel
        asyncio.run(
            notification_sr.sms.job_send_sms_and_update_status_from_ready_to_sending_async_version(db=db)
        )
        db.close()
    except Exception as e:
        raise e


@app.task
def inquiry_sms():
    try:
        notification_sr.sms.job_inquiry(db=db)
    except Exception as e:
        raise e


@app.task
def retry_sms():
    try:
        notification_sr.sms.job_retry(db=db)
    except Exception as e:
        raise e


@app.task
def send_push_notification():
    try:
        notification_sr.push_notification.job_send_push_notification_and_update_status_from_ready_to_sending(db=db)
    except Exception as e:
        raise e


@app.task
def retry_push_notification():
    try:
        notification_sr.push_notification.job_retry(db=db)
    except Exception as e:
        raise e
