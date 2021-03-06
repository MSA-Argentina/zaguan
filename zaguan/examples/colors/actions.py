from __future__ import absolute_import
from __future__ import print_function

from zaguan.actions import BaseActionController
from settings import DEBUG


class ColorsControllerActions(BaseActionController):
    """Thsi are the actions for the colors controller."""

    def document_ready(self):
        """Action excecuted when the document is ready."""
        self.controller.ready()
        print("ready")

    def select_color(self, data):
        """Action excecuted when 'select_color' is called."""
        self.controller.send_command("change_color", data)
        print("Color changed to " + data)

    def log(self, data):
        """Action excecuted when 'log' is called and debug is True."""
        if DEBUG:
            print("LOG >>>", data)
