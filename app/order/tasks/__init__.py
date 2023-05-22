from system.celery import app
from order import OrderService


order_sr = OrderService()

@app.task
def update_order_expired():
    try:
        order_sr.pay.finish_expired_orders()
    except Exception as e:
        raise e
