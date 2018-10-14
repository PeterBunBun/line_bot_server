from flask import Flask
from flask_restplus import Api
from source.apis.line import line_apis

app = Flask(__name__)
api = Api(app,
          title='LINE bot',
          version='1.0',
          description='中文測試')

api.add_namespace(line_apis)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=12121)