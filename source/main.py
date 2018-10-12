from flask import Flask
from flask_restplus import Api
from source.apis.users_api import users_api

app = Flask(__name__)
api = Api(app,
    title= 'Demo test APIs',
    version='v1.0',
    description='Descriptions',
)

api.add_namespace(users_api)

if __name__ == '__main__':
    app.run()