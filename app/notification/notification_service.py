from notification.interfaces.notification_center import notification_center_agent
from system.base.service import ServiceBase
from system.dbs.postgre import SessionLocal


class NotificationService(ServiceBase):

    def __init__(self):
        from .interfaces.providers import provider_agent
        from .interfaces.sms import sms_agent
        from .interfaces.template import template_agent
        from .interfaces.push_notification import push_notification_agent

        self.provider = provider_agent
        self.sms = sms_agent
        self.template = template_agent
        self.push_notification = push_notification_agent
        self.notification_center = notification_center_agent

    def init_providers(self):
        db = SessionLocal()
        if not self.provider.find_item_multi(
                db=db,
                name='kavenegar',
                line_number='100006555',
                raise_not_found_exception=False
        ):
            self.provider.add_item(db=db, name='kavenegar', line_number='100006555', position_number=1)
            db.commit()
        db.close()

    def init_templates(self):
        db = SessionLocal()

        # init "otp" template
        if not self.template.find_item_multi(
                db=db,
                name='otp',
                raise_not_found_exception=False
        ):
            # OTP
            self.template.add_item(
                db=db,
                name='otp',
                text="""
                    code: @@otp_code@@
                    کد ورود شما به وال پی
                    """,
                title='otp code'
            )
            db.commit()

        # init "get_card_number_to_refund" template
        if not self.template.find_item_multi(
                db=db,
                name='get_card_number_to_refund',
                raise_not_found_exception=False
        ):
            # Get card number to refund
            self.template.add_item(
                db=db,
                name='get_card_number_to_refund',
                text="@@name@@" + " عزیز لطفا جهت استرداد مبلغ سفارش خود از " +
                     "@@merchant_name@@" + " وارد لینک زیر شده و شماره کارت خود را وارد نمایید. " +
                     "\n" +
                     "@@link@@",
                title='register card number for refund'
            )
            db.commit()

        # init "refunded_user_notified" template
        if not self.template.find_item_multi(
                db=db,
                name='refunded_user_notified',
                raise_not_found_exception=False
        ):
            # Get card number to refund
            self.template.add_item(
                db=db,
                name='refunded_user_notified',
                text=
                "@@name@@" + " عزیز سفارش شما با شناسه " +
                " @@order_uuid@@ " + " برگشت داده شد. " + "\n" +
                "مبلغ " + "@@tmn_amount@@" + " تومان " + "به شماره شبا" +
                " @@iban_number@@ " +"واریز شد." + " همجنین مبلغ " +
                "@@credit_amount@@ " + "تومان به اعتبار شما در وال پی اضافه شد.",
                title='sms to user after refund'
            )
            db.commit()
        db.close()
