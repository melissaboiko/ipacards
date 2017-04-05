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

with open(GENFILE, 'wt') as f:
    for (freq, word, ipa) in ipatable:
        f.write("\t".join([
            str(freq), word, ipa
        ]))
        f.write("\n")
