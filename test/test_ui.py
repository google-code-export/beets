# This file is part of beets.
# Copyright 2010, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Tests for the command-line interface.
"""

import unittest
import sys
import os
sys.path.append('..')
from beets import library
from beets import ui
from beets.ui import commands
import test_db

# Dummy printing so we can get the commands' output.
outbuffer = []
def buffer_append(*txt):
    outbuffer.extend(txt)
def get_output():
    return u' '.join(outbuffer)
def clear_buffer():
    outbuffer[:]

class ListTest(unittest.TestCase):
    def setUp(self):
        self.old_print = ui.print_
        ui.print_ = buffer_append
        commands.print_ = buffer_append

        clear_buffer()
        self.lib = library.Library(':memory:')
        i = test_db.item()
        self.lib.add(i)

    def tearDown(self):
        ui.print_ = self.old_print
        commands.print_ = self.old_print
        
    def test_list_outputs_item(self):
        commands.list_items(self.lib, '', False)
        out = get_output()
        self.assertTrue(u'the title' in out)
    
    def test_list_album_omits_title(self):
        commands.list_items(self.lib, '', True)
        out = get_output()
        self.assertTrue(u'the title' not in out)
    
class PrintTest(unittest.TestCase):
    def setUp(self):
        class Devnull(object):
            def write(self, d):
                pass
        self.stdout = sys.stdout
        sys.stdout = Devnull()

    def tearDown(self):
        sys.stdout = self.stdout
    
    def test_print_without_locale(self):
        lang = os.environ.get('LANG')
        if lang:
            del os.environ['LANG']

        try:
            ui.print_(u'something')
        except TypeError:
            self.fail('TypeError during print')
        finally:
            if lang:
                os.environ['LANG'] = lang

    def test_print_with_invalid_locale(self):
        old_lang = os.environ.get('LANG')
        os.environ['LANG'] = ''
        old_ctype = os.environ.get('LC_CTYPE')
        os.environ['LC_CTYPE'] = 'UTF-8'

        try:
            ui.print_(u'something')
        except ValueError:
            self.fail('ValueError during print')
        finally:
            if old_lang:
                os.environ['LANG'] = old_lang
            else:
                del os.environ['LANG']
            if old_ctype:
                os.environ['LC_CTYPE'] = old_ctype
            else:
                del os.environ['LC_CTYPE']

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
