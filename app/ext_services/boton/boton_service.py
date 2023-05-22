from system.base.service import ServiceBase
from .interfaces.consumer_thread import ConsumerThread


class BotonService(ServiceBase):
    def __init__(self):
        from .interfaces.deposit import deposit_agent

        self.deposit = deposit_agent

    @staticmethod
    def run_worker():
        threads = [
            ConsumerThread(consume_type='withdraw', withdraw_type="ACK", network="BITCOIN"),
            ConsumerThread(consume_type='withdraw', withdraw_type="ACK", network="TRC20"),
            ConsumerThread(consume_type='withdraw', withdraw_type="ACK", network="ERC20"),
            ConsumerThread(consume_type='withdraw', withdraw_type="VERIFY", network="BITCOIN"),
            ConsumerThread(consume_type='withdraw', withdraw_type="VERIFY", network="TRC20"),
            ConsumerThread(consume_type='withdraw', withdraw_type="VERIFY", network="ERC20"),
            ConsumerThread(consume_type='deposit')
        ]
        for thread in threads:
            thread.start()
