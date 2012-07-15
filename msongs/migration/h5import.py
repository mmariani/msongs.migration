#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time

import h5py
import pymongo

import logging

log = logging.getLogger(__name__)


HOST, PORT = '127.0.0.1', 27017

PROGRESS_TICKER_SIZE = 23


def h5j(obj):
    if isinstance(obj, h5py._hl.group.Group):
        return {
                key: h5j(obj[key])
                for key in obj
                }
    elif isinstance(obj, h5py._hl.dataset.Dataset):
        # XXX it's a little more complicated than that
        if len(obj):
            return obj.value.tolist()
        else:
            return []
    else:
        raise TypeError(u"object of type '%s' not supported" % type(obj))



class SongLoader(object):
    def __init__(self, db, data_dir, fprog=None):
        self.db = db
        self.coll_songs = db['songs']
        self.data_dir = data_dir
        self.t0 = time.time()
        self.fprog = fprog

        if self.fprog:
            fprog.write('loading songs: ')


    def progress(self, n, end=False):
        if not self.fprog:
            return

        if not end and n % PROGRESS_TICKER_SIZE:
            return

        self.fprog.write('%d' % n)

        if end:
            elapsed = time.time()-self.t0
            self.fprog.write(' (%s secs - %d/s).\n' % (int(elapsed), n/elapsed))
        else:
            self.fprog.write(chr(8)*len(str(n)))

        self.fprog.flush()


    def to_json(self, hdata):
        return {
                'analysis': h5j(hdata['analysis']),
                'metadata': h5j(hdata['metadata']),
                'musicbrainz': h5j(hdata['musicbrainz']),
                }


    def iter_songs(self):
        for root, dirs, files in os.walk(self.data_dir):
            for filename in files:
                if re.match('TR[A-Z0-9]{16}.h5', filename):
                    fpath = os.path.join(root, filename)
                    with h5py.File(fpath) as f:
                        yield f


    def load(self):
        for idx, hdata in enumerate(self.iter_songs(), 1):
            self.progress(idx)
            jdata = self.to_json(hdata)
            self.coll_songs.insert(jdata)

        self.progress(idx, end=True)




def main(data_dir):
    conn = pymongo.Connection(HOST, PORT)

    db = conn['msd']

    # purge the old data before loading
    db.drop_collection('songs')

    coll_songs = db['songs']

    for loader_factory in [
            SongLoader,
        ]:
        loader = loader_factory(db=db, data_dir=data_dir, fprog=sys.stdout)
        loader.load()


