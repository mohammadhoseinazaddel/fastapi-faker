from system.base.service import ServiceBase


class CreditService(ServiceBase):
    def __init__(self):
        from .interfaces.calculator import credit_calculator_agent
        from .interfaces.user_credit import credit_user_agent
        from .interfaces.score import score_agent
        self.score = score_agent
        self.calculator = credit_calculator_agent
        self.user = credit_user_agent
