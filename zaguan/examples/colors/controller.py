from __future__ import absolute_import

from zaguan.controller import WebContainerController
from actions import ColorsControllerActions


class ColorsController(WebContainerController):

    def __init__(self):
        WebContainerController.__init__(self)
        instancia = ColorsControllerActions(controller=self)
        self.add_processor("colors", instancia)

    def ready(self):
        self.send_command("change_color", "yellow")

