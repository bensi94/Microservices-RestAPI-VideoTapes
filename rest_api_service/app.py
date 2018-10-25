from flask import Flask
from nameko.standalone.rpc import ClusterRpcProxy
from shared_utils.logger import EntrypointLogger, _log
from user_api import UserAPI
from tape_api import TapeAPI
from user_tape_api import UserTapeAPI

app = Flask(__name__)

### UserAPI ###
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET', ])
app.add_url_rule('/users', view_func=user_view, methods=['POST', ])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

### TapeAPI ###
tape_view = TapeAPI.as_view('tape_api')
user_tape_view = UserTapeAPI.as_view('user_tape_api')

app.add_url_rule('/tapes/', defaults={'tape_id': None},
                 view_func=tape_view, methods=['GET', ])
app.add_url_rule('/tapes',  view_func=tape_view, methods=['POST', ])
app.add_url_rule('/tapes/<int:tape_id>', view_func=tape_view,
                 methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/users/<int:user_id>/tapes',
                view_func = user_tape_view, methods=['GET', ])
app.add_url_rule('/users/<int:user_id>/tapes/<int:tape_id>', view_func=user_tape_view, 
                methods=['POST', ])
app.add_url_rule('/users/<int:user_id>/tapes/<int:tape_id>', view_func=user_tape_view, 
                methods=['PUT', 'DELETE'])


@app.route("/")
def index():
    return ('Hello world!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

