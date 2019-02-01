#!user/bin/python3
from ftplib import FTP
from io import StringIO
import pandas as pd

ftp_addr = "ftp.ncbi.nih.gov"
cds = "/genomes/INFLUENZA/influenza.cds"


if __name__ =='__main__':
    ftp = FTP("ftp.ncbi.nih.gov")
    ftp.login()
    r = StringIO()
    ftp.retrlines("RETR /genomes/INFLUENZA/influenza.faa", r.write)
    ftp.close()

    faa = pd.DataFrame(columns=["SeqID", "Description", "Sequence"])

    for sequence in list(filter(None, str(r).split('>'))):
        print(sequence.split('\n'))
