from pathlib import Path
import os, uuid, sys

class GlobalConfigs(object):
    """
    Get configs through environment variables
    """

    """Line services hosts"""
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'ed90a8b9b93f43cdd2ec683782e8a999')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'gR9mmJHcWDjpgCZ6m4VJZrJjHCJ2SIc8oieJJnG4W1hqlBlisWxVptHjM5jYhTRe0TSQdNHkM1jhWvgQFTrgd7jLKZ024syfk5tbzA51IZBoQvgIVtgylqhMzDjIgAknzDUBu1PfI3XkMVUqMQ9lvQdB04t89/1O/w1cDnyilFU=')
    LINE_DB_CONNECTION_STRING = os.getenv('LINE_DB_CONNECTION_STRING',
                                          'mongodb+srv://project1106_read_write:110616@cluster0-vof3h.mongodb.net/test?retryWrites=true')

    if not LINE_CHANNEL_SECRET:
        print('Specify LINE_CHANNEL_SECRET as environment variable.')
        sys.exit(1)
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)
    if not LINE_DB_CONNECTION_STRING:
        print('Specify LINE_DB_CONNECTION_STRING as environment variable.')
        sys.exit(1)

    """Deployment information"""
    DEPLOYMENT_VERSION = os.getenv('DEPLOYMENT_VERSION', 'No Info')
    VBENV = os.getenv('VBENV')
    VBLOC = os.getenv('VBLOC')
    MY_ENV = '{}_{}'.format(VBLOC, VBENV)

    HOST = '0.0.0.0'
    PORT = 3030
    BASE_URL = '/jobs'

    """Development Setup"""
    DEVELOPMENT_KEY = os.getenv('DEVELOPMENT_KEY', str(uuid.uuid4()))
    DEBUG_MODE = False if os.getenv('DEPLOYMENT_VERSION', None) else True

    PATH = Path(__file__)
    PROJECT_ROOT = str(PATH.parents[1])
    LOG_DIR = str(PROJECT_ROOT + '/Logs/')

    """Temp Setups"""
    VINBOM_API_HOSTS = dict(
        us_LOCAL='http://localhost:9090',
        us_DEV='http://vinbom-core-dev.corp.nio.io',
        cn_DEV='https://vinbom-core-dev.nevext.com',
        cn_STG='https://vinbom-core-stg.nevext.com',
        cn_PROD='https://vinbom-core.nevext.com'
    )

    VINBOM_API_PATHS = dict(
        SEARCH='/api/v1/search/logs',
        INGEST='/api/v1/ingest/sap56',
        BASIC='/api/v1/basic/vin',
        CONFIG='/api/v1/configurations',
        PARTS='/api/v1/parts/vin',
        ECU_PARTS='/api/v1/parts/ecu/vin',
        TRACE_PARTS='/api/v1/parts/trace/vin'
    )
