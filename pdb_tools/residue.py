# Copyright (C) 2020 Andreas Füglistaler <andreas.fueglistaler@epfl.ch>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

from .atom import Atom

class Residue:
    """
    Class representing a protein residue. It has a pointer to the pdb-lines
    and the atom-indexes.
    """
    def __init__(self, lines, indexes):
        self._lines   = lines
        self._indexes = indexes
        self._length  = indexes.stop - indexes.start
        self._iter_i = 0

    def __getitem__(self, i):
        return Atom(self._lines, i)

    def __iter__(self):
        self._iter_i = 0
        return self

    def __next__(self):
        if self._iter_i < self._length:
            self._iter_i += 1
            return Atom(self._lines, self._indexes.start + self._iter_i - 1)

        raise StopIteration

    def __len__(self):
        return self._length

    @property
    def resName(self):
        return self._lines[self._indexes][0][3]

    @resName.setter
    def resName(self, value):
        rn = value[:3] # Making sure the formatting remains correct
        for l in self._lines[self._indexes]:
            l[3] = rn

    @property
    def resSeq(self):
        return int(self._lines[self._indexes][0][5])

    @resSeq.setter
    def resSeq(self, value):
        rs = ("%4d"%value)[:4] # Making sure the formatting remains correct
        for l in self._lines[self._indexes]:
            l[5] = rs

    def write(self, f=sys.stdout):
        for l in self._lines[self._indexes]:
            f.write(f"ATOM  {l[0]} "
                f"{l[1]}{l[2]}{l[3]} "
                f"{l[4]}{l[5]}{l[6]}   "
                f"{l[7]}{l[8]}{l[9]}{l[10]}{l[11]}          "
                f"{l[12]}{l[13]}\n")
        f.write("TER\n")
