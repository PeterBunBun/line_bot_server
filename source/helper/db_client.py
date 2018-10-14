from pymongo import MongoClient
from source.global_config import GlobalConfigs
import ssl

def get_line_user_col():
    client = MongoClient(GlobalConfigs.LINE_DB_CONNECTION_STRING,
                         ssl_cert_reqs=ssl.CERT_NONE)
    return client.line.user

def get_line_group_col():
    client = MongoClient(GlobalConfigs.LINE_DB_CONNECTION_STRING,
                         ssl_cert_reqs=ssl.CERT_NONE)
    return client.line.group
