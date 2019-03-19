#!user/bin/python3
import gzip
import pickle

import numpy as np
import pandas as pd


class sequence:
    def __init__(self):
        self.meta = dict()
        self.seq = dict()
        self._seqbuild = []
        self._current_key = None
        self.length = 0

    def from_gz_file(self, fname):
        with gzip.open(fname, 'rb') as fin:
            for line in fin.readlines():
                if line != '\n':
                    self.update(line.decode().replace('\n', ''))

    def update(self, line):
        if line[0] == '>':
            newline = line.replace('>', '')
            self.length += 1
            if self._current_key:
                self.seq[self._current_key] = "".join(self._seqbuild)
            self._seqbuild = []
            metadata = newline.split('|', maxsplit=2)
            self._current_key = "".join(metadata[:2])
            values = newline
            if self._current_key not in self.meta:  # TODO make sure we are not loosing information
                self.meta[self._current_key] = values
        else:
            self._seqbuild.append(line)

    def get_dataframe(self):
        _seq = pd.DataFrame.from_dict(self.seq, orient='index', columns=['Sequence'])
        new_cols = []

        for i, detail in enumerate(self.meta.values()):
            spl = detail.split('|')
            new_cols.append(np.array([spl[0], spl[1], spl[2], spl[3], spl[4]], dtype='str'))

        _meta = pd.DataFrame(data=np.array(new_cols), index=self.meta,
                             columns=['NCBI_1', 'Key_1', 'NCBI_2', 'Key_2', 'Details'])
        _meta = _meta.astype(dtype='float', errors='ignore')
        return _meta, _seq


def generate_pickles():
    _main()


def _main():
    fna = sequence()
    fna.from_gz_file('influenza.fna.gz')

    with gzip.open('influenza.fna.pklz', 'wb') as fp:
        try:
            pickle.dump(fna, fp, 4)
        except pickle.PickleError:
            print('failed')

    faa = sequence()
    faa.from_gz_file('influenza.faa.gz')

    with gzip.open('influenza.faa.pklz', 'wb') as fp:
        try:
            pickle.dump(faa, fp, 4)
        except pickle.PickleError:
            print('failed')


if __name__ == '__main__':
    _main()
