#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Select Fragments.
Select fragments of a specified length.

Usage:
  select_frag.py [--in=FILE] [--out=FILE] <min> <max>
  select_frag.py <min> <max>
  select_frag.py (-h | --help)
  select_frag.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --in=FILE     Input file in fastq format
  --out=FILE    Output file in fasta format

"""


__author__ = 'Matheus Carvalho Bürger'
__email__ = "matheus.cburger@gmail.com"
__license__ = 'GPL'


from docopt import docopt
import logging
import sys

if __name__ == "__main__":
	## Get arguments
	arguments = docopt(__doc__, version='Select Fragments 0.1')
	infh = sys.stdin	# input file handle
	if arguments['--in']:
		infh = open(arguments['--in'])
	outfh = sys.stdout	# output file handle
	if arguments['--out']:
		outfh = open(arguments['--out'], "w")
	min_len = int(arguments['<min>'])
	max_len = int(arguments['<max>'])

	## logging config
	FORMAT = '%(asctime)-15s :: select_frag :: %(message)s'
	logging.basicConfig(format=FORMAT)
	logger = logging.getLogger('select_frag')

	## parse fastq
	seqname = ""
	for lnumber, line in enumerate(infh):
		line = line.strip()
		if seqname:
			if min_len <= len(line) <= max_len:
				outfh.write("%s\n" % seqname)
				outfh.write("%s\n" % line)
			seqname = ""
		if line.startswith("@"):
			if lnumber % 4 == 0:
				seqname = line
			else:
				logger.warning("Sequence identifier on wrong line, ignoring line : %s" % line)

	if arguments['--in']:
		infh.close()
	if arguments['--out']:
		outfh.close()
