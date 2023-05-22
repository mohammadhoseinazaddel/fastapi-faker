from system.base.service import ServiceBase


class JibitService(ServiceBase):
    def __init__(self):
        from ext_services.jibit.interfaces.payment_gateway import jibit_payment_gw_agent
        from ext_services.jibit.interfaces.identity_validate import jibit_identity_agent
        from ext_services.jibit.interfaces.transfer import jibit_transferor_agent

        self.payment_gateway = jibit_payment_gw_agent
        self.identity_validate = jibit_identity_agent
        self.transferor = jibit_transferor_agent
