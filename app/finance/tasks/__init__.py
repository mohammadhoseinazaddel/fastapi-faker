from system.celery import app
from finance.finance_service import FinanceService


@app.task
def merchants_settlement():
    try:
        finance_sr = FinanceService()
        finance_sr.merchant_settlement.all_merchants_settle()
    except Exception as e:
        raise e
