# Copyright (C) 2020 Andreas Füglistaler <andreas.fueglistaler@epfl.ch>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
import pandas as pd

from .chain import Chain
from .residue import Residue
from .atom import Atom

BB   = ["N", "CA", "C", "O"]

three21 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
            'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
            'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
            'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

aas = set(three21.keys())

one23 = {v: k for k, v in three21.items()}

class PDB:
    def __init__(self, pdb_file=sys.stdin):
        cspecs = [(0, 6), (6, 11), (12, 16), (16, 17), (17, 20), (21, 22),
                  (22, 26), (26, 27), (30, 38), (38, 46), (46, 54), (54, 60),
                  (60, 66), (76, 78), (78, 80)]

        df = pd.read_fwf(pdb_file, colspecs=cspecs, header=None,
                        names=["tag", "serial", "name", "altLoc", "resName",
                                "chainID", "resSeq", "iCode", "x", "y", "z",
                                "occupancy", "tempFactor", "element", "charge"])

        self._data = df[df.tag.isin(["ATOM", "TER", "END"])].reset_index(drop=True).copy()

    def __getitem__(self, i):
        return Chain(self._data, i)

    def residues(self):
        for i in range(len(self._data.res_r)):
            yield Residue(self._data, i)

    def chains(self):
        for i in range(len(self._data.chain_r)):
            yield Chain(self._data, i)

    def atoms(self):
        for i in range(self._data.length):
            yield Atom(self._data, i)

    def write(self, f=sys.stdout):
        for c in self.chains():
            for a in c.atoms():
                a.write(f)
            print("TER", file=f)
        print("END", file=f)
