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

"""Tests for the general importer functionality.
"""
import unittest
import os
import shutil

import _common
from beets import library
from beets import importer
from beets import mediafile

TEST_TITLES = ('The Opener', 'The Second Track', 'The Last Track')
class NonAutotaggedImportTest(unittest.TestCase):
    def setUp(self):
        self.io = _common.DummyIO()
        self.io.install()

        self.libdb = os.path.join(_common.RSRC, 'testlib.blb')
        self.lib = library.Library(self.libdb)
        self.libdir = os.path.join(_common.RSRC, 'testlibdir')
        self.lib.directory = self.libdir
        self.lib.path_formats = {
            'default': os.path.join('$artist', '$album', '$title')
        }

        self.srcdir = os.path.join(_common.RSRC, 'testsrcdir')

    def tearDown(self):
        self.io.restore()
        if os.path.exists(self.libdb):
            os.remove(self.libdb)
        if os.path.exists(self.libdir):
            shutil.rmtree(self.libdir)
        if os.path.exists(self.srcdir):
            shutil.rmtree(self.srcdir)

    def _create_test_file(self, filepath, metadata):
        """Creates an mp3 file at the given path within self.srcdir.
        filepath is given as an array of folder names, ending with the
        file name. Sets the file's metadata from the provided dict.
        Returns the full, real path to the file.
        """
        realpath = os.path.join(self.srcdir, *filepath)
        if not os.path.exists(os.path.dirname(realpath)):
            os.makedirs(os.path.dirname(realpath))
        shutil.copy(os.path.join(_common.RSRC, 'full.mp3'), realpath)

        f = mediafile.MediaFile(realpath)
        for attr in metadata:
            setattr(f, attr, metadata[attr])
        f.save()

        return realpath

    def _run_import(self, titles=TEST_TITLES, delete=False, threaded=False,
                    singletons=False):
        # Make a bunch of tracks to import.
        paths = []
        for i, title in enumerate(titles):
            paths.append(self._create_test_file(
                ['the_album', 'track_%s.mp3' % (i+1)],
                {
                    'track': (i+1),
                    'artist': 'The Artist',
                    'album': 'The Album',
                    'title': title,
                }))

        # Run the UI "beet import" command!
        importer.run_import(
                lib=self.lib,
                paths=[os.path.dirname(paths[0])],
                copy=True,
                write=True,
                autot=False,
                logfile=None,
                art=False,
                threaded=threaded,
                color=False,
                delete=delete,
                quiet=True,
                resume=False,
                quiet_fallback='skip',
                choose_match_func = None,
                should_resume_func = None,
                singletons = singletons,
                choose_item_func = None,
                timid = False,
        )

        return paths

    def test_album_created_with_track_artist(self):
        self._run_import()
        albums = self.lib.albums()
        self.assertEqual(len(albums), 1)
        self.assertEqual(albums[0].albumartist, 'The Artist')

    def _copy_arrives(self):
        artist_folder = os.path.join(self.libdir, 'The Artist')
        album_folder = os.path.join(artist_folder, 'The Album')
        self.assertEqual(len(os.listdir(artist_folder)), 1)
        self.assertEqual(len(os.listdir(album_folder)), 3)

        filenames = set(os.listdir(album_folder))
        destinations = set('%s.mp3' % title for title in TEST_TITLES)
        self.assertEqual(filenames, destinations)
    def test_import_copy_arrives(self):
        self._run_import()
        self._copy_arrives()
    def test_threaded_import_copy_arrives(self):
        self._run_import(threaded=True)
        self._copy_arrives()

    def test_import_no_delete(self):
        paths = self._run_import(['sometrack'], delete=False)
        self.assertTrue(os.path.exists(paths[0]))

    def test_import_with_delete(self):
        paths = self._run_import(['sometrack'], delete=True)
        self.assertFalse(os.path.exists(paths[0]))

    def test_import_singleton(self):
        paths = self._run_import(['sometrack'], singletons=True)
        self.assertTrue(os.path.exists(paths[0]))

# Utilities for invoking the apply_choices coroutine.
def _call_apply(coros, items, info):
    task = importer.ImportTask(None, None, None)
    task.is_album = True
    task.set_choice((info, items))
    if not isinstance(coros, list):
        coros = [coros]
    for coro in coros:
        task = coro.send(task)
def _call_apply_choice(coro, items, choice):
    task = importer.ImportTask(None, None, items)
    task.is_album = True
    task.set_choice(choice)
    coro.send(task)

class ImportApplyTest(unittest.TestCase, _common.ExtraAsserts):
    def setUp(self):
        self.libdir = os.path.join(_common.RSRC, 'testlibdir')
        os.mkdir(self.libdir)
        self.lib = library.Library(':memory:', self.libdir)
        self.lib.path_formats = {
            'default': 'one',
            'comp': 'two',
            'singleton': 'three',
        }

        self.srcpath = os.path.join(self.libdir, 'srcfile.mp3')
        shutil.copy(os.path.join(_common.RSRC, 'full.mp3'), self.srcpath)
        self.i = library.Item.from_path(self.srcpath)
        self.i.comp = False

        trackinfo = {'title': 'one', 'artist': 'some artist',
                     'track': 1, 'length': 1, 'id': 'trackid'}
        self.info = {
            'artist': 'some artist',
            'album': 'some album',
            'tracks': [trackinfo],
            'va': False,
            'album_id': 'albumid',
            'artist_id': 'artistid',
            'albumtype': 'soundtrack',
        }

    def tearDown(self):
        shutil.rmtree(self.libdir)

    def test_finalize_no_delete(self):
        config = _common.iconfig(self.lib, delete=False)
        applyc = importer.apply_choices(config)
        applyc.next()
        finalize = importer.finalize(config)
        finalize.next()
        _call_apply([applyc, finalize], [self.i], self.info)
        self.assertExists(self.srcpath)

    def test_finalize_with_delete(self):
        config = _common.iconfig(self.lib, delete=True)
        applyc = importer.apply_choices(config)
        applyc.next()
        finalize = importer.finalize(config)
        finalize.next()
        _call_apply([applyc, finalize], [self.i], self.info)
        self.assertNotExists(self.srcpath)

    def test_apply_asis_uses_album_path(self):
        coro = importer.apply_choices(_common.iconfig(self.lib))
        coro.next() # Prime coroutine.
        _call_apply_choice(coro, [self.i], importer.action.ASIS)
        self.assertExists(
            os.path.join(self.libdir, self.lib.path_formats['default']+'.mp3')
        )

    def test_apply_match_uses_album_path(self):
        coro = importer.apply_choices(_common.iconfig(self.lib))
        coro.next() # Prime coroutine.
        _call_apply(coro, [self.i], self.info)
        self.assertExists(
            os.path.join(self.libdir, self.lib.path_formats['default']+'.mp3')
        )

    def test_apply_tracks_uses_singleton_path(self):
        coro = importer.apply_choices(_common.iconfig(self.lib))
        coro.next() # Prime coroutine.

        task = importer.ImportTask.item_task(self.i)
        task.set_choice(self.info['tracks'][0])
        coro.send(task)

        self.assertExists(
            os.path.join(self.libdir, self.lib.path_formats['singleton']+'.mp3')
        )

    def test_apply_sentinel(self):
        coro = importer.apply_choices(_common.iconfig(self.lib))
        coro.next()
        coro.send(importer.ImportTask.done_sentinel('toppath'))
        # Just test no exception for now.

class AsIsApplyTest(unittest.TestCase):
    def setUp(self):
        self.dbpath = os.path.join(_common.RSRC, 'templib.blb')
        self.lib = library.Library(self.dbpath)
        self.config = _common.iconfig(self.lib, write=False, copy=False)

        # Make an "album" that has a homogenous artist. (Modified by
        # individual tests.)
        i1 = _common.item()
        i2 = _common.item()
        i3 = _common.item()
        i1.title = 'first item'
        i2.title = 'second item'
        i3.title = 'third item'
        i1.comp = i2.comp = i3.comp = False
        i1.albumartist = i2.albumartist = i3.albumartist = ''
        self.items = [i1, i2, i3]

    def tearDown(self):
        os.remove(self.dbpath)

    def _apply_result(self):
        """Run the "apply" coroutine and get the resulting Album."""
        coro = importer.apply_choices(self.config)
        coro.next()
        _call_apply_choice(coro, self.items, importer.action.ASIS)

        return self.lib.albums()[0]

    def test_asis_homogenous_va_not_set(self):
        alb = self._apply_result()
        self.assertFalse(alb.comp)
        self.assertEqual(alb.albumartist, self.items[2].artist)

    def test_asis_heterogenous_va_set(self):
        self.items[0].artist = 'another artist'
        self.items[1].artist = 'some other artist'
        alb = self._apply_result()
        self.assertTrue(alb.comp)
        self.assertEqual(alb.albumartist, 'Various Artists')

    def test_asis_majority_artist_va_not_set(self):
        self.items[0].artist = 'another artist'
        alb = self._apply_result()
        self.assertFalse(alb.comp)
        self.assertEqual(alb.albumartist, self.items[2].artist)

class InferAlbumDataTest(unittest.TestCase):
    def setUp(self):
        i1 = _common.item()
        i2 = _common.item()
        i3 = _common.item()
        i1.title = 'first item'
        i2.title = 'second item'
        i3.title = 'third item'
        i1.comp = i2.comp = i3.comp = False
        i1.albumartist = i2.albumartist = i3.albumartist = ''
        i1.mb_albumartistid = i2.mb_albumartistid = i3.mb_albumartistid = ''
        self.items = [i1, i2, i3]

        self.task = importer.ImportTask(path='a path', toppath='top path',
                                        items=self.items)
        self.task.set_null_match()

    def _infer(self):
        importer._infer_album_fields(self.task)

    def test_asis_homogenous_single_artist(self):
        self.task.set_choice(importer.action.ASIS)
        self._infer()
        self.assertFalse(self.items[0].comp)
        self.assertEqual(self.items[0].albumartist, self.items[2].artist)

    def test_asis_heterogenous_va(self):
        self.items[0].artist = 'another artist'
        self.items[1].artist = 'some other artist'
        self.task.set_choice(importer.action.ASIS)

        self._infer()

        self.assertTrue(self.items[0].comp)
        self.assertEqual(self.items[0].albumartist, 'Various Artists')

    def test_asis_comp_applied_to_all_items(self):
        self.items[0].artist = 'another artist'
        self.items[1].artist = 'some other artist'
        self.task.set_choice(importer.action.ASIS)

        self._infer()

        for item in self.items:
            self.assertTrue(item.comp)
            self.assertEqual(item.albumartist, 'Various Artists')

    def test_asis_majority_artist_single_artist(self):
        self.items[0].artist = 'another artist'
        self.task.set_choice(importer.action.ASIS)

        self._infer()

        self.assertFalse(self.items[0].comp)
        self.assertEqual(self.items[0].albumartist, self.items[2].artist)

    def test_apply_gets_artist_and_id(self):
        self.task.set_choice(({}, self.items)) # APPLY

        self._infer()

        self.assertEqual(self.items[0].albumartist, self.items[0].artist)
        self.assertEqual(self.items[0].mb_albumartistid, self.items[0].mb_artistid)

    def test_apply_lets_album_values_override(self):
        for item in self.items:
            item.albumartist = 'some album artist'
            item.mb_albumartistid = 'some album artist id'
        self.task.set_choice(({}, self.items)) # APPLY

        self._infer()

        self.assertEqual(self.items[0].albumartist,
                         'some album artist')
        self.assertEqual(self.items[0].mb_albumartistid,
                         'some album artist id')

    def test_small_single_artist_album(self):
        self.items = [self.items[0]]
        self.task.items = self.items
        self.task.set_choice(importer.action.ASIS)
        self._infer()
        self.assertFalse(self.items[0].comp)

class DuplicateCheckTest(unittest.TestCase):
    def setUp(self):
        self.lib = library.Library(':memory:')
        self.i = _common.item()
        self.album = self.lib.add_album([self.i])

    def test_duplicate_album(self):
        res = importer._duplicate_check(self.lib, self.i.albumartist,
                                        self.i.album)
        self.assertTrue(res)

    def test_different_album(self):
        res = importer._duplicate_check(self.lib, 'xxx', 'yyy')
        self.assertFalse(res)

    def test_duplicate_va_album(self):
        self.album.albumartist = 'an album artist'
        res = importer._duplicate_check(self.lib, 'an album artist',
                                        self.i.album)
        self.assertTrue(res)

    def test_duplicate_item(self):
        res = importer._item_duplicate_check(self.lib, self.i.artist,
                                             self.i.title)
        self.assertTrue(res)

    def test_different_item(self):
        res = importer._item_duplicate_check(self.lib, 'xxx', 'yyy')
        self.assertFalse(res)

    def test_recent_item(self):
        recent = set()
        importer._item_duplicate_check(self.lib, 'xxx', 'yyy', recent)
        res = importer._item_duplicate_check(self.lib, 'xxx', 'yyy', recent)
        self.assertTrue(res)

    def test_recent_album(self):
        recent = set()
        importer._duplicate_check(self.lib, 'xxx', 'yyy', recent)
        res = importer._duplicate_check(self.lib, 'xxx', 'yyy', recent)
        self.assertTrue(res)

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
