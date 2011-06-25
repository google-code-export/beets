# This file is part of beets.
# Copyright 2011, Adrian Sampson.
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

"""Test file manipulation functionality of Item.
"""

import unittest
import shutil
import os
import stat
from os.path import join

import _common
from _common import item, touch
import beets.library
from beets import util

class MoveTest(unittest.TestCase):
    def setUp(self):
        # make a temporary file
        self.path = join(_common.RSRC, 'temp.mp3')
        shutil.copy(join(_common.RSRC, 'full.mp3'), self.path)
        
        # add it to a temporary library
        self.lib = beets.library.Library(':memory:')
        self.i = beets.library.Item.from_path(self.path)
        self.lib.add(self.i)
        
        # set up the destination
        self.libdir = join(_common.RSRC, 'testlibdir')
        self.lib.directory = self.libdir
        self.lib.path_formats = {'default': join('$artist', '$album', '$title')}
        self.i.artist = 'one'
        self.i.album = 'two'
        self.i.title = 'three'
        self.dest = join(self.libdir, 'one', 'two', 'three.mp3')
        
    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.libdir):
            shutil.rmtree(self.libdir)
    
    def test_move_arrives(self):
        self.i.move(self.lib)
        self.assertTrue(os.path.exists(self.dest))
    
    def test_move_departs(self):
        self.i.move(self.lib)
        self.assertTrue(not os.path.exists(self.path))
    
    def test_copy_arrives(self):
        self.i.move(self.lib, copy=True)
        self.assertTrue(os.path.exists(self.dest))
    
    def test_copy_does_not_depart(self):
        self.i.move(self.lib, copy=True)
        self.assertTrue(os.path.exists(self.path))
    
    def test_move_changes_path(self):
        self.i.move(self.lib)
        self.assertEqual(self.i.path, util.normpath(self.dest))

    def test_copy_already_at_destination(self):
        self.i.move(self.lib)
        old_path = self.i.path
        self.i.move(self.lib, copy=True)
        self.assertEqual(self.i.path, old_path)

    def test_move_already_at_destination(self):
        self.i.move(self.lib)
        old_path = self.i.path
        self.i.move(self.lib, copy=False)
        self.assertEqual(self.i.path, old_path)

    def test_read_only_file_copied_writable(self):
        # Make the source file read-only.
        os.chmod(self.path, 0444)

        try:
            self.i.move(self.lib, copy=True)
            self.assertTrue(os.access(self.i.path, os.W_OK))
        finally:
            # Make everything writable so it can be cleaned up.
            os.chmod(self.path, 0777)
            os.chmod(self.i.path, 0777)
    
class HelperTest(unittest.TestCase):
    def test_ancestry_works_on_file(self):
        p = '/a/b/c'
        a =  ['/','/a','/a/b']
        self.assertEqual(util.ancestry(p), a)
    def test_ancestry_works_on_dir(self):
        p = '/a/b/c/'
        a = ['/', '/a', '/a/b', '/a/b/c']
        self.assertEqual(util.ancestry(p), a)
    def test_ancestry_works_on_relative(self):
        p = 'a/b/c'
        a = ['a', 'a/b']
        self.assertEqual(util.ancestry(p), a)
    
    def test_components_works_on_file(self):
        p = '/a/b/c'
        a =  ['/', 'a', 'b', 'c']
        self.assertEqual(util.components(p), a)
    def test_components_works_on_dir(self):
        p = '/a/b/c/'
        a =  ['/', 'a', 'b', 'c']
        self.assertEqual(util.components(p), a)
    def test_components_works_on_relative(self):
        p = 'a/b/c'
        a =  ['a', 'b', 'c']
        self.assertEqual(util.components(p), a)

class AlbumFileTest(unittest.TestCase):
    def setUp(self):
        # Make library and item.
        self.lib = beets.library.Library(':memory:')
        self.lib.path_formats = \
            {'default': join('$albumartist', '$album', '$title')}
        self.libdir = os.path.join(_common.RSRC, 'testlibdir')
        self.lib.directory = self.libdir
        self.i = item()
        # Make a file for the item.
        self.i.path = self.lib.destination(self.i)
        util.mkdirall(self.i.path)
        touch(self.i.path)
        # Make an album.
        self.ai = self.lib.add_album((self.i,))
    def tearDown(self):
        if os.path.exists(self.libdir):
            shutil.rmtree(self.libdir)

    def test_albuminfo_move_changes_paths(self):
        self.ai.album = 'newAlbumName'
        self.ai.move()
        self.lib.load(self.i)

        self.assert_('newAlbumName' in self.i.path)

    def test_albuminfo_move_moves_file(self):
        oldpath = self.i.path
        self.ai.album = 'newAlbumName'
        self.ai.move()
        self.lib.load(self.i)

        self.assertFalse(os.path.exists(oldpath))
        self.assertTrue(os.path.exists(self.i.path))

    def test_albuminfo_move_copies_file(self):
        oldpath = self.i.path
        self.ai.album = 'newAlbumName'
        self.ai.move(True)
        self.lib.load(self.i)

        self.assertTrue(os.path.exists(oldpath))
        self.assertTrue(os.path.exists(self.i.path))

class ArtFileTest(unittest.TestCase):
    def setUp(self):
        # Make library and item.
        self.lib = beets.library.Library(':memory:')
        self.libdir = os.path.abspath(os.path.join(_common.RSRC, 'testlibdir'))
        self.lib.directory = self.libdir
        self.i = item()
        self.i.path = self.lib.destination(self.i)
        # Make a music file.
        util.mkdirall(self.i.path)
        touch(self.i.path)
        # Make an album.
        self.ai = self.lib.add_album((self.i,))
        # Make an art file too.
        self.art = self.lib.get_album(self.i).art_destination('something.jpg')
        touch(self.art)
        self.ai.artpath = self.art
    def tearDown(self):
        if os.path.exists(self.libdir):
            shutil.rmtree(self.libdir)

    def test_art_deleted_when_items_deleted(self):
        self.assertTrue(os.path.exists(self.art))
        self.ai.remove(True)
        self.assertFalse(os.path.exists(self.art))

    def test_art_moves_with_album(self):
        self.assertTrue(os.path.exists(self.art))
        oldpath = self.i.path
        self.ai.album = 'newAlbum'
        self.ai.move()
        self.lib.load(self.i)

        self.assertNotEqual(self.i.path, oldpath)
        self.assertFalse(os.path.exists(self.art))
        newart = self.lib.get_album(self.i).art_destination(self.art)
        self.assertTrue(os.path.exists(newart))

    def test_setart_copies_image(self):
        newart = os.path.join(self.libdir, 'newart.jpg')
        touch(newart)
        i2 = item()
        i2.path = self.i.path
        i2.artist = 'someArtist'
        ai = self.lib.add_album((i2,))
        i2.move(self.lib, True)
        
        self.assertEqual(ai.artpath, None)
        ai.set_art(newart)
        self.assertTrue(os.path.exists(ai.artpath))
    
    def test_setart_sets_permissions(self):
        newart = os.path.join(self.libdir, 'newart.jpg')
        touch(newart)
        os.chmod(newart, 0400) # read-only
        
        try:
            i2 = item()
            i2.path = self.i.path
            i2.artist = 'someArtist'
            ai = self.lib.add_album((i2,))
            i2.move(self.lib, True)
            ai.set_art(newart)
            
            mode = stat.S_IMODE(os.stat(ai.artpath).st_mode)
            self.assertTrue(mode & stat.S_IRGRP)
            self.assertTrue(os.access(ai.artpath, os.W_OK))
            
        finally:
            # Make everything writable so it can be cleaned up.
            os.chmod(newart, 0777)
            os.chmod(ai.artpath, 0777)

class RemoveTest(unittest.TestCase):
    def setUp(self):
        # Make library and item.
        self.lib = beets.library.Library(':memory:')
        self.libdir = os.path.abspath(os.path.join(_common.RSRC, 'testlibdir'))
        self.lib.directory = self.libdir
        self.i = item()
        self.i.path = self.lib.destination(self.i)
        # Make a music file.
        util.mkdirall(self.i.path)
        touch(self.i.path)
        # Make an album with the item.
        self.ai = self.lib.add_album((self.i,))
    def tearDown(self):
        if os.path.exists(self.libdir):
            shutil.rmtree(self.libdir)

    def test_removing_last_item_removes_empty_dir(self):
        parent = os.path.dirname(self.i.path)
        self.assertTrue(os.path.exists(parent))
        self.lib.remove(self.i, True)
        self.assertFalse(os.path.exists(parent))

    def test_removing_last_item_preserves_nonempty_dir(self):
        parent = os.path.dirname(self.i.path)
        touch(os.path.join(parent, 'dummy.txt'))
        self.lib.remove(self.i, True)
        self.assertTrue(os.path.exists(parent))

    def test_removing_without_delete_leaves_file(self):
        path = self.i.path
        self.lib.remove(self.i)
        self.assertTrue(os.path.exists(path))

    def test_removing_last_item_preserves_library_dir(self):
        self.lib.remove(self.i, True)
        self.assertTrue(os.path.exists(self.libdir))

    def test_removing_item_outside_of_library_deletes_nothing(self):
        self.lib.directory = os.path.abspath(os.path.join(_common.RSRC, 'xxx'))
        parent = os.path.dirname(self.i.path)
        self.lib.remove(self.i, True)
        self.assertTrue(os.path.exists(parent))

# Tests that we can "delete" nonexistent files.
class SoftRemoveTest(unittest.TestCase, _common.ExtraAsserts):
    def setUp(self):
        self.path = os.path.join(_common.RSRC, 'testfile')
        touch(self.path)
    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_soft_remove_deletes_file(self):
        util.soft_remove(self.path)
        self.assertNotExists(self.path)

    def test_soft_remove_silent_on_no_file(self):
        try:
            util.soft_remove(self.path + 'XXX')
        except OSError:
            self.fail('OSError when removing path')

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
