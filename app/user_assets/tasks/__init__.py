from system.celery import app
from system_object import SystemObjectsService
from user_assets import UserAssetsService
from ext_services import BotonService
from user.interfaces.user import user_agent

system_object_sr = SystemObjectsService()
user_assets_sr = UserAssetsService()
boton_sr = BotonService()

@app.task
def manage_income_deposit():
    try:
        user_assets_sr.wallet.manage_income_deposit(
            sys_obj_sr=system_object_sr,
            boton_sr=boton_sr,
            user_agent=user_agent,
        )
    except Exception as e:
        raise e
