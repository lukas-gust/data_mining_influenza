#!user/bin/python3
from ftplib import FTP
from io import StringIO
import pandas as pd

ftp_addr = "ftp.ncbi.nih.gov"

class sequence:
    def __init__(self):
        self.meta = dict()
        self.seq = dict()
        self._seqbuild = StringIO()
        self._current_key = None

    def write_to_dict(self, line):
        if line[0] == '>':
            if self._current_key:
                self.seq[self._current_key] = self._seqbuild.getvalue()
                self._seqbuild.close()
            self._seqbuild = StringIO()
            metadata = line.split('|', maxsplit=2)
            self._current_key = int(metadata[1])
            values = metadata[2]
            if self._current_key not in self.meta: # TODO make sure we are not loosing information
                self.meta[self._current_key] = values
        else:
            self._seqbuild.write(line)



if __name__ =='__main__':
    ftp = FTP(ftp_addr)
    ftp.login()
    r = sequence()
    ftp.retrlines("RETR /genomes/INFLUENZA/influenza.fna", r.write_to_dict)
    ftp.close()

    print(r.seq)
