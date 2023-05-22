from system.base.mixins import InterfaceLifeCycle


class BankInterface(InterfaceLifeCycle):
    def __init__(self):
        from .bank_pay import bank_pay_agent
        from .bank_pay_gw import payment_gateway_agent
        from .bank_profile import bank_profile_agent
        from .bank_transactions import bank_transactions_agent

        self.payment = bank_pay_agent
        self.gateway = payment_gateway_agent
        self.profile = bank_profile_agent
        self.transactions = bank_transactions_agent


bank_agent = BankInterface()
