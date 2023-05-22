from system.celery import app

from system_object import SystemObjectsService

sys_obj_sr = SystemObjectsService()


@app.task
def update_coin_prices():
    try:
        sys_obj_sr.coin.update_coin_price()
    except Exception as e:
        raise e
