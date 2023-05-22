from ext_services.finnotech.check_bargashti.interfaces.token import finnotech_token_agent
from system.base.service import ServiceBase


class FinnotechService(ServiceBase):
    def __init__(self):
        from ext_services.finnotech.check_bargashti.interfaces.cheque_bargashti import finnotech_cheque_bargashti_agent

        self.cheque_bargashti = finnotech_cheque_bargashti_agent
        self.token = finnotech_token_agent
