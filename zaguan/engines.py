import gi
gi.require_version('WebKit2', '4.0')

from gi.repository.WebKit2 import WebView, Settings

class WebKitMethods(object):
    @staticmethod
    def create_browser(debug=False):
        settings = Settings()
        # TODO: Ver que onda esto
        # https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/Settings.html#WebKit2.Settings.props.enable_page_cache
        settings.set_allow_file_access_from_file_urls(True)
        if debug:
            settings.set_enable_developer_extras(True)
        webview = WebView()

        if not debug:
            # https://people.gnome.org/~gcampagna/docs/WebKit2-3.0/WebKit2.WebView-context-menu.html
            def _menu(webview, context_menu, event, hit_test_result):
                context_menu.remove_all()
            webview.connect('context-menu', _menu)

        webview.set_settings(settings)
        return webview

    @staticmethod
    def inject_javascript(browser, script):
        browser.run_javascript(script)

    @staticmethod
    def open_uri(browser, uri):
        browser.load_uri(uri)

    @staticmethod
    def set_settings(browser, user_settings):
        browser_settings = browser.get_settings()
        if user_settings is not None:
            for setting, value in user_settings:
                browser_settings.set_property(setting, value)
