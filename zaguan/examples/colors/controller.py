import urllib
from json import loads as from_json

from zaguan.controller import WebContainerController
from zaguan.examples.colors.settings import DEBUG


class ColorsController(WebContainerController):
    def __init__(self):
        WebContainerController.__init__(self)
        self.processors.append(self.process_colors_url)

    def process_colors_url(self, uri):
        scheme, path = uri.split(':', 1)
        print scheme, path, uri
        if scheme == "http":
            parts = path.split("/")[2:]
            if parts[0] == "colors":
                remain = parts[1]
            elif parts[1]  == "colors":
                remain = parts[2]
            else:
                remain = None
            if remain is not None:
                try:
                    action, data = remain.split("?")
                except ValueError:
                    action = remain
                    data = "null"

                data = from_json(urllib.unquote(data))
                print "ACTIONNNNNNN", action, data
                self.process_action(action, data)

    def ready(self):
        self.enviar_comando("change_color", "red")

    def process_action(self, action, data):
        """Dispatcher principal de acciones de voto_web."""
        print action, data
        if action == "document_ready":
            self.ready()
            print "ready"
        elif action == "log":
            if DEBUG:
                print "LOG >>>", data
        else:
            raise NotImplementedError("Action not implemented: %s" % action)


