#! /usr/bin/env python
from flask.app import Flask
from flask.globals import request

from zaguan.examples.colors.controller import ColorsController

_msg_queue = []
def queue_send(msg):
    _msg_queue.append(msg)


if __name__ == '__main__':
    controller = ColorsController()

    app = Flask(__name__, static_folder="html")
    app.add_url_rule('/<path:filename>', endpoint='static',
                     view_func=app.send_static_file)
    app.debug = True

    @app.route("/")
    def index(module=None):
        html = open("html/index.html").read()
        return html + '<script src="js/debug.js" type="text/javascript"></script>'

    @app.route("/colors/<action>")
    def actions(action):
        controller.process_uri(request.url)
        return ""

    @app.route("/debug/messages")
    def debug_send():
        global _msg_queue
        messages = "\n".join(_msg_queue)
        _msg_queue = []
        return messages
    app.run()
