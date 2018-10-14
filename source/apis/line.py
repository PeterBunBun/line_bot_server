from flask_restplus import Namespace, Resource
from flask import request, abort, jsonify
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, JoinEvent, FollowEvent, LeaveEvent, UnfollowEvent
from source.global_config import GlobalConfigs
from source.helper.line_utils import enable_group, reply_message, enable_user, disable_group, disable_user
from source.helper.logger import getProgramLogger

import json

line_apis = Namespace('line', description='Call back endpoint for line server')
line_bot_api = LineBotApi(GlobalConfigs.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(GlobalConfigs.LINE_CHANNEL_SECRET)
handler = WebhookHandler(GlobalConfigs.LINE_CHANNEL_SECRET)

logger = getProgramLogger(__name__)

@line_apis.route('/callback')
class Callback(Resource):

    def post(self):
        logger.info('A LINE callback request is received')
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        logger.info("Header: {}".format(dict(request.headers)))
        logger.info("Request body: " + body)

        #parse webhook body
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError as e:
            logger.error(e)
            abort(400, '{}'.format(e))

        errors = list()

        # Process event in events list one by one
        for event in events:
            if isinstance(event, JoinEvent):
                logger.info('Processing a JoinEvent')
                if event.source.type == 'group':
                    logger.info('JoinEvent: Joining a group')
                    enable_group(event)
                    reply_message(event.reply_token, 'Thank you for adding me to the group, I wiil notify the group when an emergency happened')
                elif event.source.type == 'room':
                    logger.info('JoinEvent: Joining a room')
                    logger.info('Got a join room event but did not process')
                    pass

            elif isinstance(event, LeaveEvent):
                logger.info('Processing a LeaveEvent')
                if event.source.type == 'group':
                    logger.info('LeaveEvent: Leaving a group')
                    disable_group(event)
                elif event.source.type == 'room':
                    logger.info('LeaveEvent: Leaving a room')
                    logger.info('Got a leave room event but did not process')
                    pass

            elif isinstance(event, FollowEvent):
                logger.info('Processing a FollowEvent')
                enable_user(event)
                reply_message(event.reply_token, 'Thank you for following me, I wiil notify you when an emergency happened')

            elif isinstance(event, UnfollowEvent):
                logger.info('Processing a UnfollowEvent')
                disable_user(event)

            else:
                error_msg = 'Unknown event type detected, type: {}, event content: {}'.format(type(event), event)
                logger.erorr(error_msg)
                errors.append(error_msg)

        return 'OK' if not errors else jsonify(errors)

@line_apis.route('/push_text')
class PushText(Resource):

    def post(self):
        body = request.get_data(as_text=True)
        logger.info("Request body: " + body)

        source_ip = request.remote_addr
        pushing_msg = 'Calling from: {}\nPushing body: {}'.format(source_ip, body)
        logger.info("Pushing: {}".format(pushing_msg))
        user_id_peter_lee = 'C1f77fa55580cec85ec3bb97d018d9a39'
        line_bot_api.push_message(user_id_peter_lee, TextSendMessage(text=pushing_msg))

        return 'OK'