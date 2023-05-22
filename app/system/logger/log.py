import logging
import logging.config
# import graypy

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# logging.config.dictConfig(LOG_CONFIG)

# graylog_handler = graypy.GELFUDPHandler('localhost', 12201)

requests_logger = logging.getLogger("request")
user_logger = logging.getLogger("user")
blockchain_logger = logging.getLogger("blockchain")
wallet_logger = logging.getLogger("wallet")
ext_service_logger = logging.getLogger("wallet")


# requests_logger.addHandler(graylog_handler)
# user_logger.addHandler(graylog_handler)
# blockchain_logger.addHandler(graylog_handler)
# wallet_logger.addHandler(graylog_handler)
# ext_service_logger.addHandler(graylog_handler)
