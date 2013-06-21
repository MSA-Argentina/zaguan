from zaguan.controller import WebContainerController
from zaguan.examples.colors.actions import ColorsControllerActions


class ColorsController(WebContainerController):

    def __init__(self):
        WebContainerController.__init__(self)
        instancia = ColorsControllerActions(controller=self)
        self.add_processor("colors", instancia)

    def ready(self):
        self.enviar_comando("change_color", "yellow")

    def process_action(self, action, data):
        self.dispatch_action(action, data)
