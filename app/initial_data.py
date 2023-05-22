from sqlalchemy.orm import Session

from notification.notification_service import NotificationService
from system.dbs.postgre import SessionLocal

from system_object import SystemObjectsService

from user import UserService


if __name__ == "__main__":

    print('start initial info')

    user_sr = UserService()
    user_sr.initiate_scopes()
    user_sr.initiate_default_groups()
    user_sr.init_merchant_data()
    user_sr.initiate_full_admin_user()
    print('finish initial user info')

    system_object_sr = SystemObjectsService()
    system_object_sr.init_fake_data()
    system_object_sr.init_coin_data()
    print('finish initial coin data')

    notification_sr = NotificationService()
    notification_sr.init_providers()
    notification_sr.init_templates()

    print('finish initial info')