from finance.interfaces.bank_profile import bank_profile_agent
from system.base.service import ServiceBase


class FinanceService(ServiceBase):
    def __init__(self):
        from .interfaces.settle import settle_agent
        from .interfaces.bank import bank_agent
        from .interfaces.debt_user import debt_user_agent
        from .interfaces.refund import refund_agent
        from .interfaces.transfer import transfer_agent
        from .interfaces.settle_pgw import settle_pgw_agent
        from .interfaces.settle_credit import settle_credit_agent
        from .interfaces.dashboard import merchant_dashboard_agent

        self.settle = settle_agent
        self.settle_pgw = settle_pgw_agent
        self.settle_credit = settle_credit_agent
        self.bank = bank_agent
        self.refund = refund_agent
        self.transfer = transfer_agent
        self.bank_profile = bank_profile_agent
        self.merchant_dashboard = merchant_dashboard_agent
        self.debt_user = debt_user_agent


finance_SR = FinanceService()
