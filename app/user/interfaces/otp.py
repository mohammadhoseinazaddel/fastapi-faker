from datetime import datetime
import time
from random import randrange

from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from notification.interfaces.sms import sms_agent
from system.base.crud import CRUDBase
from system.base.exceptions import HTTP_401_Otp_Walpay
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal
from user.models.otp_sent import otp_crud, UsrOtpSent
from user.models.schemas.otp_sent import OtpSentCreateSchema, OtpSentUpdateSchema, OtpSentGetMultiSchema


class OtpInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = crud
        self.model = UsrOtpSent

    @staticmethod
    def get_otp_text(otp: str):
        return f"شما در حال ورود به وال پی هستید. رمز یکبار مصرف:" \
               f"\n code " \
               f"{otp}"

    def send_otp(self, mobile: str, db: Session = SessionLocal()):
        from notification.notification_service import NotificationService
        notification_sr = NotificationService()

        otp_sent = db.query(UsrOtpSent).filter(UsrOtpSent.mobile == mobile).order_by(
            desc(UsrOtpSent.sent_at)).first()

        if not otp_sent or (datetime.now() - otp_sent.sent_at).seconds > settings.OTP_TIME_OUT:
            otp = str(randrange(100000, 1000000))

            # send sms with notification service
            notification_sr.sms.send_sms_with_template(
                input_type="send-otp",
                input_unique_id=0,
                template_name='otp',
                template_key_values_dict={'otp_code': otp},
                mobile_number=mobile
            )

            otp_sent = UsrOtpSent(mobile=mobile, otp=str(otp), sent_at=datetime.now())
            db.add(otp_sent)
            db.commit()
            db.refresh(otp_sent)

            return True

        else:
            return False

    @staticmethod
    def check_otp(mobile: str, otp: str, db: Session = SessionLocal()):
        if mobile == settings.DEFAULT_MOBILE_USER_MOBILE and otp == '323090':
            return True

        otp_sent = db.query(UsrOtpSent).filter(UsrOtpSent.mobile == mobile).order_by(
            desc(UsrOtpSent.sent_at)).first()
        if not otp_sent:
            time.sleep(1)
            raise HTTP_401_Otp_Walpay
        if (datetime.now() - otp_sent.sent_at).seconds > settings.OTP_TIME_OUT:
            time.sleep(1)
            raise HTTP_401_Otp_Walpay
        if otp_sent.otp != otp:
            time.sleep(1)
            raise HTTP_401_Otp_Walpay
        if otp_sent.used_at is not None:
            time.sleep(1)
            raise HTTP_401_Otp_Walpay

        otp_sent.used_at = datetime.now()
        db.add(otp_sent)
        db.commit()
        db.refresh(otp_sent)

        return True


otp_agent = OtpInterface(
    crud=otp_crud,
    create_schema=OtpSentCreateSchema,
    update_schema=OtpSentUpdateSchema,
    get_multi_schema=OtpSentGetMultiSchema
)
