import gi


def get_wk_implementation(webkit_version):
    """Returns the Zaguan webkit wrapper.

    Arguments:
        webkit_version -- a number representing the version.
    """
    implementation = WebKit2Methods
    if webkit_version == 1:
        implementation = WebKitMethods

    return implementation


class WebKitMethods(object):
    """Methods for WebKit1."""
    @staticmethod
    def create_browser(debug=False):
        """Creates a WebView instance, properly configured.

        Arguments:
            debug -- boolean to indicate if it should output debug and add
                context menu and inspector.
        """
        gi.require_version('WebKit', '3.0')
        from gi.repository.WebKit import WebView, WebSettings, set_cache_model

        # http://lazka.github.io/pgi-docs/WebKit-3.0/functions.html#WebKit.set_cache_model
        cache_model = WebView.CacheModel.WEBKIT_CACHE_MODEL_DOCUMENT_BROWSER
        set_cache_model(cache_model)

        if debug:
            WebKitMethods.print_version()

        settings = WebSettings()
        # Settings for webkitgtk http://webkitgtk.org/reference/webkitgtk/stable/WebKitWebSettings.html
        # Setting for WebKit via git http://lazka.github.io/pgi-docs/#WebKit-3.0/classes/WebSettings.html
        settings.set_property('enable-default-context-menu', False)
        settings.set_property('enable-accelerated-compositing', True)
        settings.set_property('enable-file-access-from-file-uris', True)

        if debug:
            settings.set_property('enable-default-context-menu', False)

        webview = WebView()
        webview.set_settings(settings)
        return webview

    @staticmethod
    def inject_javascript(browser, script):
        """Injects JS on a WebView object.

        Arguments:
            browser -- the WebView target.
            script -- the code to run.
        """
        browser.execute_script(script)

    @staticmethod
    def open_uri(browser, uri):
        """Opens a uri in the browser.

        Arguments:
            browser -- the WebView target.
            uri -- the uri to open.
        """
        browser.open(uri)

    @staticmethod
    def set_settings(browser, user_settings):
        """Adds the settings to the browser settings.

        Arguments:
            browser -- a WebView instance.
            user_settings -- the settings to add to the browser.
        """
        browser_settings = browser.get_settings()
        if user_settings is not None:
            for setting, value in user_settings:
                browser_settings.set_property(setting, value)

    @staticmethod
    def get_inspector(browser):
        """Gets the inspector instance.

        Arguments:
            browser -- a WebView instance.
        """
        from zaguan_inspector import Inspector

        inspector = browser.get_inspector()

        return Inspector(inspector)

    @staticmethod
    def connect(browser, callback):
        """Connects the navigation event to the browser.


        Arguments:
            browser -- a WebView instance.
            callback -- the callback function.
        """
        browser.connect("resource-request-starting", callback)

    @staticmethod
    def print_version():
        """Prints the WebKit version."""
        from gi.repository.WebKit import (major_version, minor_version,
                                          micro_version)
        version = "{}.{}.{}".format(major_version(), minor_version(),
                                    micro_version())
        print("Cargando WebKit: {}".format(version))


class WebKit2Methods(object):
    @staticmethod
    def create_browser(debug=False):
        """Creates a WebView instance, properly configured.

        Arguments:
            debug -- boolean to indicate if it should output debug and add
                context menu and inspector.
        """
        gi.require_version('WebKit2', '4.0')
        from gi.repository.WebKit2 import (WebView, Settings, CacheModel,
                                           ProcessModel)

        if debug:
            WebKit2Methods.print_version()

        settings = Settings()
        settings.set_allow_file_access_from_file_urls(True)
        if debug:
            settings.set_enable_developer_extras(True)
        webview = WebView()

        # http://lazka.github.io/pgi-docs/WebKit2-4.0/classes/WebContext.html#WebKit2.WebContext.set_cache_model
        context = webview.get_context()
        context.set_cache_model(CacheModel.DOCUMENT_BROWSER)

        # https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/Settings.html#WebKit2.Settings.props.enable_page_cache
        context.set_process_model(ProcessModel.SHARED_SECONDARY_PROCESS)

        if not debug:
            # https://people.gnome.org/~gcampagna/docs/WebKit2-3.0/WebKit2.WebView-context-menu.html
            def menu_contextual(webview, context_menu, event, hit_test_result):
                context_menu.remove_all()

            webview.connect('context-menu', menu_contextual)

        webview.set_settings(settings)
        return webview

    @staticmethod
    def inject_javascript(browser, script):
        """Injects JS on a WebView object.

        Arguments:
            browser -- the WebView target.
            script -- the code to run.
        """
        browser.run_javascript(script)

    @staticmethod
    def open_uri(browser, uri):
        """Opens a uri in the browser.

        Arguments:
            browser -- the WebView target.
            uri -- the uri to open.
        """
        browser.load_uri(uri)

    @staticmethod
    def set_settings(browser, user_settings):
        """Adds the settings to the browser settings.

        Arguments:
            browser -- a WebView instance.
            user_settings -- the settings to add to the browser.
        """
        browser_settings = browser.get_settings()
        if user_settings is not None:
            for setting, value in user_settings:
                browser_settings.set_property(setting, value)

    @staticmethod
    def connect(browser, callback):
        """Connects the navigation event to the browser.


        Arguments:
            browser -- a WebView instance.
            callback -- the callback function.
        """
        browser.connect("resource-load-started", callback)

    @staticmethod
    def print_version():
        """Prints the WebKit version."""
        from gi.repository.WebKit2 import (get_major_version,
                                           get_minor_version,
                                           get_micro_version)

        version = "{}.{}.{}".format(get_major_version(), get_minor_version(),
                                    get_micro_version())
        print("Cargando WebKit: {}".format(version))
