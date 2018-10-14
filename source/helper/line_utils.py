from source.helper.db_client import get_line_user_col, get_line_group_col
from source.helper.logger import getProgramLogger
from linebot import LineBotApi
from linebot.models import TextSendMessage
from source.global_config import GlobalConfigs
from datetime import datetime

logger = getProgramLogger(__name__)

def find_user(user_id, **kwargs):
    user_col = get_line_user_col()
    qstring = {
        'user_id': user_id,
        **kwargs
    }

    result = list(user_col.find(qstring))

    if len(result) > 1:
        error_msg = 'More than 1 entries are found with user_id: {}'.format(user_id)
        logger.error(error_msg)
        raise Exception(error_msg)
    elif len(result) == 1:
        return result[0]
    else:
        return None

def find_group(group_id, **kwargs):
    group_col = get_line_group_col()
    qstring = {
        'group_id': group_id,
        **kwargs
    }

    result = list(group_col.find(qstring))

    if len(result) > 1:
        error_msg = 'More than 1 entries are found with group_id: {}'.format(group_id)
        logger.error(error_msg)
        raise Exception(error_msg)
    elif len(result) == 1:
        return result[0]
    else:
        return None

def enable_user(user_follow_event):
    user_col = get_line_user_col()
    qstring = {
        'user_id': user_follow_event.source.userId
    }
    insert_doc = {
        '$set': {
            'join_time': user_follow_event.timestamp,
            'enable': True
        }
    }
    try:
        user_col.update_one(qstring, insert_doc, upsert=True)
    except Exception as e:
        error_msg = 'Error while enabling user: {} to the database. Error: {}'.format(user_follow_event, e)
        logger.error(error_msg)
        raise e

    return None

def enable_group(group_join_event):
    logger.debug('enabling group')
    group_col = get_line_group_col()

    logger.debug('creating qstring')
    qstring = {
        'group_id': group_join_event.source.groupId
    }

    logger.debug('creating insert_doc')
    insert_doc = {
        '$set': {
            'join_time': group_join_event.timestamp,
            'enable': True
        }
    }

    logger.debug('trying to write to db')
    try:
        logger.debug('updating db')
        group_col.update_one(qstring, insert_doc, upsert=True)
        logger.debug('done updating')
    except Exception as e:
        error_msg = 'Error while enabling group: {} to the database. Error: {}'.format(group_join_event, e)
        logger.error(error_msg)
        raise e

    return None

def disable_user(user_unfollow_event):
    user_col = get_line_user_col()
    qstring = {
        'user_id': user_unfollow_event.source.userId
    }
    insert_doc = {
        '$set': {
            'enable': False
        }
    }
    try:
        user_col.update_one(qstring, insert_doc, upsert=True)
    except Exception as e:
        error_msg = 'Error while disabling user: {} to the database. Error: {}'.format(user_unfollow_event, e)
        logger.error(error_msg)
        raise e

    return None

def disable_group(group_leave_event):
    group_col = get_line_group_col()
    qstring = {
        'group_id': group_leave_event.source.groupId
    }
    insert_doc = {
        '$set': {
            'enable': False
        }
    }
    try:
        group_col.update_one(qstring, insert_doc, upsert=True)
    except Exception as e:
        error_msg = 'Error while disabling group: {} to the database. Error: {}'.format(group_leave_event, e)
        logger.error(error_msg)
        raise e

    return None

def reply_message(reply_token, message_str):
    try:
        line_bot_api = LineBotApi(GlobalConfigs.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=message_str)
        )
    except Exception as e:
        error_msg = 'Error while replying message to {}. Error: {}'.format(reply_token, e)
        logger.error(error_msg)
        raise e

if __name__ == "__main__":
    pass


