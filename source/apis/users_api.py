from flask_restplus import Namespace, Resource, fields

users_api = Namespace('users_api', description='Get all endpoint insight')

apis_usage = users_api.model('mfg api rq', {
    'count': fields.String(required=True, description='Total usage count of a specific API'),
    'last_used': fields.String(required=True, description='Last used timestamp'),
})

@users_api.route('/addfriend')
class AddFriend(Resource):

    def get(self):
        '''List all current APIs'''

        return 'This is only for test (GET) new'