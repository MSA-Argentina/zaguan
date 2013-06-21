try:
    from webkit import WebView, WebSettings
except ImportError:
    print "webkit not found"


class WebKitMethods(object):
    @staticmethod
    def create_browser():
        settings = WebSettings()
        #settings.set_property('enable-xss-auditor', False)
        # todas las settings en http://webkitgtk.org/reference/webkitgtk/stable/WebKitWebSettings.html
        settings.set_property('enable-default-context-menu', False)
        settings.set_property('enable-accelerated-compositing', True)
        settings.set_property('enable-file-access-from-file-uris', True)
        webview = WebView()
        webview.set_settings(settings)
        return webview

    @staticmethod
    def inject_javascript(browser, script):
        browser.execute_script(script)

    @staticmethod
    def open_uri(browser, uri):
        browser.open(uri)
