from json import dumps, loads
from urllib.parse import unquote

from zaguan.container import launch_browser

class WebContainerController(object):
    """Base class for the web containers of the controllers."""
    def __init__(self):
        self.processors = []

    def on_navigation_requested(self, webview, resource, request):
        """This is the Callback executed each time  URI inside the webkit
        object is loaded"""
        uri = request.get_uri()

        self.process_uri(uri)

    def process_uri(self, uri):
        """Procces the url on each processor."""
        for processor in self.processors:
            processor(uri)

    def set_screen(self, screen, **kwargs):
        """Sends the change sreen command to the web interface."""
        self.send_command("change_screen", [screen, kwargs])

    def send_command(self, command, data=None):
        """Inyects the JS in the browser for the givven command."""
        json_data = dumps(data).replace("\\\"", "\\\'")
        self.send_function("run_op('%s', '%s')" % (command, json_data))

    def get_browser(self, uri, settings=None, debug=False):
        """Gets the browser objects and prpare it to bo able to be used in it's
        context.
        """
        if settings is None:
            settings = []

        browser, web_send = launch_browser(uri, debug=debug,
                                           user_settings=settings)
        self.send_function = web_send
        browser.connect("resource-load-started",
                        self.on_navigation_requested)
        return browser

    def add_processor(self, url_word, instance=None):
        def _inner(uri):
            scheme, path = uri.split(':', 1)
            if scheme == "http":
                parts = path.split("/")[2:]
                if parts[0] == url_word:
                    remain = parts[1]
                elif parts[1] == url_word:
                    remain = parts[2]
                else:
                    remain = None
                if remain is not None:
                    try:
                        action, data = remain.split("?")
                    except ValueError:
                        action = remain
                        data = "null"

                    data = loads(unquote(data))
                    # search the action at the 'action controller' instance
                    # argument. if we dont find the action, we try to get it
                    # from the controller itself.
                    method = getattr(instance, action, None)
                    if method is None:
                        method = getattr(self, action, None)

                    if not method:
                        raise NotImplementedError(action)
                    return method(data)

        self.processors.append(_inner)
