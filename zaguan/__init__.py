from gi.repository import GLib, Gtk as gtk, Gdk as gdk
timeout_add = GLib.timeout_add
WINDOW_TOPLEVEL = gtk.WindowType.TOPLEVEL
WIN_POS_CENTER_ALWAYS = gtk.WindowPosition.CENTER_ALWAYS


from time import sleep

from zaguan.controller import WebContainerController


class Zaguan(object):
    def __init__(self, uri, controller=None):
        if controller is None:
            controller = WebContainerController()
        self.controller = controller
        self.uri = uri
        self.on_close = None

    def run(self, settings=None, window=None, debug=False, on_close=None,
            cef=False):
        self.on_close = on_close
        self.run_gtk(settings, window, debug)

    def OnExit(self, widget, data=None):
        self.exiting = True
        gtk.main_quit()

    def run_gtk(self, settings=None, window=None, debug=False):
        gdk.threads_init()

        if window is None:
            self.window = gtk.Window(WINDOW_TOPLEVEL)
            self.window.set_position(WIN_POS_CENTER_ALWAYS)
        else:
            self.window = window

        browser = self.controller.get_browser(self.uri, debug=debug,
                                              settings=settings)
        self.window.connect("delete-event", self.quit)
        self.window.set_border_width(0)
        self.window.add(browser)

        sleep(1)
        self.window.show_all()
        self.window.show()
        gtk.main()

    def quit(self, widget, event):
        if self.on_close is not None:
            self.on_close(widget, event)
