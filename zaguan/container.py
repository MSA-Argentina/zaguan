from zaguan.engines import WebKitMethods, GtkMozEmbedMethods
from zaguan.constants import WEBKIT
from zaguan.functions import asynchronous_gtk_message, get_implementation

implementation_name = get_implementation()


def launch_browser(uri, echo=False, user_settings=[]):
    if implementation_name == WEBKIT:
        implementation = WebKitMethods
    else:
        raise NotImplementedError("No web engine available")

    browser = implementation.create_browser()
    browser_settings = browser.get_settings()
    for setting, value in user_settings:
        browser_settings.set_property(setting, value)

    implementation.open_uri(browser, uri)

    def web_send(msg):
        if echo: print '<<<', msg
        asynchronous_gtk_message(implementation.inject_javascript)(browser,
                                                                   msg)

    return browser, web_send
