from flask_restplus import Namespace, Resource
from flask import request, abort, jsonify
from source.helper.logger import getProgramLogger

iot_apis = Namespace('iot', description='Call back endpoint for line server')

logger = getProgramLogger(__name__)

@iot_apis.route('/button_click')
class ButtonClick(Resource):

    def get(self):
        """

        :return:
        """
