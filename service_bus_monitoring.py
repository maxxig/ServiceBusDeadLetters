import config, func, time, logging
from datetime import datetime
cnfg = config.get_config()

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler('log.log')
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

from azure.servicebus.management import ServiceBusAdministrationClient
from azure.servicebus import ServiceBusClient, TransportType

CONNECTION_STR = cnfg['service_bus_connection_string']

dt = datetime.now()
logger.info(f'{dt}: Start processing.')
# is for test
#result_dict = {'es-bulk': {'Subscription': 'product.complete', 'dead_letters_count': 221}, 'products-prices-publishing': {'Subscription': 'exec', 'dead_letters_count': 14}, 'products-publishing': {'Subscription': 'oneday', 'dead_letters_count': 35}, 'products-update': {'Subscription': 'stock-management', 'dead_letters_count': 11833}, 'sm-stock-update': {'Subscription': 'elasticsearch', 'dead_letters_count': 1943}, 'variation-groups-cache-update': {'Subscription': 'change-variation-groups-events-to-markethub', 'dead_letters_count': 158}}
result_dict = {}
with ServiceBusAdministrationClient.from_connection_string(CONNECTION_STR) as servicebus_mgmt_client:
    result_dict = func.get_deadletters_cnt(servicebus_mgmt_client)

#with ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=False, transport_type = TransportType.AmqpOverWebsocket) as servicebus_client:
logger.info(f'{datetime.now()}: Deadletters info: {str(result_dict)}')
is_new_value = func.check_previous_version(result_dict)
logger.info(f'{datetime.now()}: Is new value: {is_new_value}')
if len(result_dict) > 0 and is_new_value:
    func.sendEmail(func.generate_html_table(result_dict), cnfg['email_login'], cnfg['email_password'], cnfg['emails_to'], '1')
    logger.info(f'{datetime.now()}: Email sended')
logger.info(f'{datetime.now()}: Stop processing.')
