# -*- coding: utf-8 -*-
import urllib
import inspect

from json import dumps, loads

from zaguan.actions import BaseActionController
from zaguan.container import launch_browser


class WebContainerController(object):
    def __init__(self):
        self.processors = []

    """Clase base para los controladores de los contenedores web."""
    def on_navigation_requested(self, elem, view, frame, req, data=None):
        """Callback que se ejecuta cada vez que se carga una URI dentro del
        objeto webkit."""
        uri = req.get_uri()
        self.process_uri(uri)

    def process_uri(self, uri):
        """Procesa la URI y la separa en partes para llamar a process_action."""
        for processor in self.processors:
            processor(uri)

    def set_pantalla(self, pantalla, **kwargs):
        """Envia un comando de cambio de pantalla a la interfaz Web"""
        self.enviar_comando("cambiar_pantalla", [pantalla, kwargs])

    def enviar_comando(self, comando, data=None):
        """Genera el comando Javascript a enviar a la interfaz web y lo envia.
        """
        json_data = dumps(data).replace("\\\"", "\\\'")
        self.send_function("run_op('%s', '%s')" % (comando, json_data))

    def get_browser(self, uri, settings=[], debug=False):
        """Obtiene el objeto browser y lo prepara para poder ser usada en este
        contexto.

        Opcionalmente, se pueden pasar una lista de tuplas (key, value) de
        settings para hacer override de los defaults del browser.

        Devuelve el objeto browser y setea la funcion de envio para la clase.
        """
        browser, web_send = launch_browser(uri, echo=debug,
                                           user_settings=settings)
        self.send_function = web_send

        browser.connect("resource-request-starting",
                        self.on_navigation_requested)
        return browser

    def add_processor(self, url_word, instance):
        def _inner(uri):
            scheme, path = uri.split(':', 1)
            if scheme == "http":
                parts = path.split("/")[2:]
                if parts[0] == url_word:
                    remain = parts[1]
                elif parts[1]  == url_word:
                    remain = parts[2]
                else:
                    remain = None
                if remain is not None:
                    try:
                        action, data = remain.split("?")
                    except ValueError:
                        action = remain
                        data = "null"

                    data = loads(urllib.unquote(data))

                    # search the action at the 'action controller' instance
                    # argumetn. if we dont find the action, we try to get it
                    # from the controller itself.
                    method = getattr(instance, action, None)
                    if method is None:
                        method = getattr(self, action, None)
                    if not method:
                        raise NotImplementedError()
                    return method(data)

        self.processors.append(_inner)

    def bindaction(self, action):
        """Bind actions into the WebContainerController."""
        if BaseActionController not in inspect.getmro(action):
            raise TypeError("Only BaseActionController type is allowed.")

        self.actions = action(controller=self)

    def dispatch_action(self, action, data):
        """Execute 'action' with the given data or raise NotImplementedError."""
        method = getattr(self.actions, action, None)

        if method is None:
            msg = '%s is not implemented at %s' % (action, repr(self.actions))
            raise NotImplementedError(msg)

        return method(data)
