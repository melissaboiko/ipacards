#!/usr/bin/env python3
#import nltk
import os
import sys
import csv
from subprocess import check_output
from tqdm import tqdm

pkgdir = os.path.dirname(os.path.dirname(__file__))
datadir = pkgdir + '/data'
gendir = pkgdir + '/generated'
FREQDATA= datadir + '/' + 'SUBTLEX-UK.txt'
GENFILE = gendir + '/' + 'freq_ipa.tsv'
WORDLIST = datadir + '/' + 'british-english-large'
EXTRACT=1000

def to_ipa(word):
    return(check_output(['espeak',
                  '-q',
                  '--ipa=2',
                  '-v',
                  'en-uk-rp',
                   word]).decode('utf-8').strip())
wordlist = set() # lol
with open(WORDLIST, 'rt') as f:
    for line in f:
        wordlist.add(line.strip())

ipatable = []
freqdata_total = sum(1 for line in open(FREQDATA, 'rt')) # for tqdm bar

with(open(FREQDATA, 'rt')) as f:
    r = csv.reader(f, delimiter="\t")
    for row in tqdm(r, total=freqdata_total): # tqdm = progress bar
        try:
            freq = int(row[1])
            word = row[0]
            if word not in wordlist:
                continue
            ipa = to_ipa(word)
            ipatable.append((freq, word, ipa))
        except ValueError:
            # no freq information; int(row[1]) fails
            pass

ipatable.sort(reverse=True)

if os.path.isfile(GENFILE):
    os.unlink(GENFILE) # needed when it's read-only

with open(GENFILE, 'wt') as f:
    order=0 # increasing int for easy Anki sorting
    for (freq, word, ipa) in ipatable:
        order+=1
        f.write("\t".join([
            str(order),
            word,
            ipa,
            str(freq)
        ]))
        f.write("\n")
os.chmod(GENFILE, 0o444) # make it read-only

with open(GENFILE, 'rt') as f_in:
    with open(GENFILE + '.top' + str(EXTRACT), 'wt') as f_out:
        i = 0
        for line in f_in:
            f_out.write(line)
            i += 1
            if i >= 1000:
                break
