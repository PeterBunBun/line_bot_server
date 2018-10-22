from source.helper.line.line_db_client import get_line_user_col, get_line_group_col
from source.helper.logger import getProgramLogger
from linebot import LineBotApi
from linebot.models import TextSendMessage
from source.global_config import GlobalConfigs
from linebot.models import (
    MessageEvent,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    PostbackEvent,
    BeaconEvent,
    AccountLinkEvent,
)
import json

line_bot_api = LineBotApi(GlobalConfigs.LINE_CHANNEL_ACCESS_TOKEN)

logger = getProgramLogger(__name__)

def get_all_enabled_users():
    """

    :return:
    """
    user_col = get_line_user_col()
    qstring = {
        'enable': True
    }

    return list(user_col.find(qstring))

def get_all_enabled_groups():
    """

    :return:
    """
    group_col = get_line_group_col()
    qstring = {
        'enable': True
    }

    return list(group_col.find(qstring))

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
        'user_id': user_follow_event.source.user_id
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
    logger.info('enabling group')
    group_col = get_line_group_col()

    logger.info('creating qstring')
    qstring = {
        'group_id': group_join_event.source.group_id
    }

    logger.info('creating insert_doc')
    insert_doc = {
        '$set': {
            'join_time': group_join_event.timestamp,
            'enable': True
        }
    }

    logger.info('trying to write to db')
    try:
        logger.info('updating db')
        group_col.update_one(qstring, insert_doc, upsert=True)
        logger.info('done updating')
    except Exception as e:
        error_msg = 'Error while enabling group: {} to the database. Error: {}'.format(group_join_event, e)
        logger.error(error_msg)
        raise e

    return None

def disable_user(user_unfollow_event):
    user_col = get_line_user_col()
    qstring = {
        'user_id': user_unfollow_event.source.user_id
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
        'group_id': group_leave_event.source.group_id
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

def push_message_to_many(list_of_ids, text_body):
    """

    :param list_of_ids:
    :param text_body:
    :return:
    """

    logger.info("Pushing: {}".format(text_body))

    for id in list_of_ids:
        line_bot_api.push_message(id, TextSendMessage(text=text_body))

class WebhookParserPeter(object):
    """Webhook Parser."""

    def __init__(self):
        """__init__ method.

        :param str channel_secret: Channel secret (as text)
        """
        pass

    def parse(self, body):
        """Parse webhook request body as text.

        :param str body: Webhook request body (as text)
        :param str signature: X-Line-Signature value (as text)
        :rtype: list[T <= :py:class:`linebot.models.events.Event`]
        :return:
        """
        pass

        body_json = json.loads(body)
        events = []
        for event in body_json['events']:
            event_type = event['type']
            if event_type == 'message':
                events.append(MessageEvent.new_from_json_dict(event))
            elif event_type == 'follow':
                events.append(FollowEvent.new_from_json_dict(event))
            elif event_type == 'unfollow':
                events.append(UnfollowEvent.new_from_json_dict(event))
            elif event_type == 'join':
                events.append(JoinEvent.new_from_json_dict(event))
            elif event_type == 'leave':
                events.append(LeaveEvent.new_from_json_dict(event))
            elif event_type == 'postback':
                events.append(PostbackEvent.new_from_json_dict(event))
            elif event_type == 'beacon':
                events.append(BeaconEvent.new_from_json_dict(event))
            elif event_type == 'accountLink':
                events.append(AccountLinkEvent.new_from_json_dict(event))
            else:
                logger.warn('Unknown event type. type=' + event_type)

        return events

if __name__ == "__main__":
    pass


