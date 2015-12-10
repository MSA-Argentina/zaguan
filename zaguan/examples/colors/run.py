#!/usr/bin/env python
from __future__ import absolute_import
import os

try:
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    pass

from zaguan import Zaguan
from controller import ColorsController


def load_window():
    controller = ColorsController()
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_ = os.path.join(cur_dir, 'html/index.html')
    uri = 'file://' + pathname2url(file_)
    zaguan = Zaguan(uri, controller)
    zaguan.run(debug=True)


def load_browser():
    zaguan = Zaguan("http://www.google.com")
    zaguan.run(qt=True)


if __name__ == "__main__":
    #load_browser()
    load_window()
