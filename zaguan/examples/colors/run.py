import pygtk
pygtk.require('2.0')
import os
import urllib

from zaguan import Zaguan
from zaguan.examples.colors.controller import ColorsController


def load_window():
    controller = ColorsController()
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_ = os.path.join(cur_dir, 'html/index.html')
    uri = 'file://' + urllib.pathname2url(file_)
    zaguan = Zaguan(uri, controller)
    zaguan.run()

def load_browser():
    zaguan = Zaguan("http://www.google.com")
    zaguan.run(qt=True)

if __name__ == "__main__":
    #load_browser()
    load_window()
