from zaguan.engines import WebKitMethods
from zaguan.functions import asynchronous_gtk_message


def launch_browser(uri, debug=False, user_settings=None, window=None):
    """Creates and initialize a browser object"""
    implementation = WebKitMethods

    browser = implementation.create_browser(debug)
    implementation.set_settings(browser, user_settings)

    implementation.open_uri(browser, uri)

    def web_send(msg):
        if debug:
            print('<<<', msg)
        func = asynchronous_gtk_message(implementation.inject_javascript)
        func(browser, msg)

    return browser, web_send
