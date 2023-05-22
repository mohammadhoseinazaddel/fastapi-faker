from system.base.service import ServiceBase


class OrderService(ServiceBase):
    def __init__(self):
        from .interfaces.pay import pay_agent
        from .interfaces.fund import fund_agent
        from .interfaces.commission import commission_agent

        self.pay = pay_agent
        self.fund = fund_agent
        self.commission = commission_agent


order_SR = OrderService()
