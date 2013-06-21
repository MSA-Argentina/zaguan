import gtk

from time import sleep

from zaguan.controller import WebContainerController


gtk.gdk.threads_init()


class Zaguan(object):
    def __init__(self, controller, uri):
        self.controller = controller
        self.uri = uri

    def run(self, settings=None, window=None, debug=False):
        if window is None:
            self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        else:
            self.window = window
        browser = self.controller.get_browser(self.uri, debug=debug,
                                              settings=settings)
        self.window.set_border_width(0)
        self.window.add(browser)
        sleep(1)
        self.window.show_all()
        self.window.show()
        gtk.main()
