import urllib
from json import loads as from_json

from zaguan.controller import WebContainerController
from zaguan.examples.colors.settings import DEBUG


class ColorsController(WebContainerController):
    def __init__(self):
        WebContainerController.__init__(self)
        self.add_processor("colors", self.process_action)

    def ready(self):
        self.enviar_comando("change_color", "yellow")
        #self.push_command("change_color", "red")

    def process_action(self, action, data):
        print action, data
        if action == "document_ready":
            self.ready()
            print "ready"
        elif action == "select_color":
            self.enviar_comando("change_color", data)
            print "Color changed to " + data
        elif action == "log":
            if DEBUG:
                print "LOG >>>", data
        else:
            raise NotImplementedError("Action not implemented: %s" % action)


