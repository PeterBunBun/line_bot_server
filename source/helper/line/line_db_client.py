from pymongo import MongoClient
from source.global_config import GlobalConfigs
from source.helper.logger import getProgramLogger

import ssl

logger = getProgramLogger(__name__)

def get_line_user_col():
    logger.info('Connecting to DB: line, collection: user')
    client = MongoClient(GlobalConfigs.LINE_DB_CONNECTION_STRING,
                         ssl_cert_reqs=ssl.CERT_NONE)
    return client.line.user

def get_line_group_col():
    logger.info('Connecting to DB: line, collection: group')
    client = MongoClient(GlobalConfigs.LINE_DB_CONNECTION_STRING,
                         ssl_cert_reqs=ssl.CERT_NONE)
    return client.line.group
