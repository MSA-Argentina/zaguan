import pygtk
pygtk.require('2.0')
import gtk
import thread
import os
import urllib

from time import sleep

from zaguan.examples.colors.controller import ColorsController


gtk.gdk.threads_init()

def load_window():
    controller = ColorsController()
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_position(gtk.WIN_POS_CENTER_ALWAYS)

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_ = os.path.join(cur_dir, 'html/index.html')
    uri = 'file://' + urllib.pathname2url(file_)
    browser = controller.get_browser(uri, debug=True)
    window.set_border_width(0)
    window.add(browser)
    sleep(1)
    window.show_all()
    window.show()
    gtk.main()

if __name__ == "__main__":
    load_window()
