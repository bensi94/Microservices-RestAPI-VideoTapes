from flask import Flask
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.logger import EntrypointLogger, _log
from user_api import UserAPI

app = Flask(__name__)


user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET', ])
app.add_url_rule('/users/', view_func=user_view, methods=['POST', ])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

@app.route("/")
def index():
    return ('Hello wrorld!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

