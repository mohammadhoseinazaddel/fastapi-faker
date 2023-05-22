from system.base.service import ServiceBase


class WallexService(ServiceBase):
    def __init__(self):
        from ext_services.wallex.interfaces.login import wallex_login_agent
        from ext_services.wallex.interfaces.pay import wallex_pay_agent
        from ext_services.wallex.interfaces.price import WallexPriceInterface

        self.login = wallex_login_agent
        self.pay = wallex_pay_agent
        self.price = WallexPriceInterface()
