from flask_restplus import Namespace, Resource, fields

callback_apis = Namespace('callback', description='Call back endpoint for line server')

@callback_apis.route('/')
class Callback(Resource):

    def get(self):
        """

        :return:
        """

        return 'This is the callback response'