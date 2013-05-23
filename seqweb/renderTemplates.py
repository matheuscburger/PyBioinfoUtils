#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Matheus Carvalho Bürger'
__license__ = 'gpl'

from jinja2 import Environment, PackageLoader

import os
import re
import sys


if __name__ == "__main__":

	### Variaveis iniciais
	htmlFilename = "index.html"
	runsDir = "/home/NGS/seqweb/htdocs"



	###
	env = Environment(loader=PackageLoader('core', 'templates'))
	runs_template = env.get_template("runs.html")
	runs = []
	print >>sys.stderr, os.listdir(runsDir)
	for f in os.listdir(runsDir):
		if re.search(r"run\d+", f):
			runs.append(f)
	runs.sort()
	print >>sys.stderr, runs
	with open(os.path.join(runsDir, "index.html"), 'w') as index:
		print >>index, runs_template.render(runs=runs, title="Runs")

	## Percorrendo runs
	op_template = env.get_template("runoptions.html")
	qual_template = env.get_template("qual.html")
	map_template = env.get_template("map.html")
	vcf_template = env.get_template("vcf.html")
	snv_template = env.get_template("snv.html")
	samplere = re.compile(r"(\S+)_fastqc")
	for r in runs:
		with open(os.path.join(runsDir, r, "index.html"), 'w') as index:
			print >>index, op_template.render(runname=r)
		samples = []
		try:
			for s in os.listdir(os.path.join(runsDir, r, 'raw', 'fastQCresult')):
				if os.path.isdir(os.path.join(runsDir, r, 'raw', 'fastQCresult', s)):
					match = samplere.search(s)
					samples.append(match.group(1))
			samples.sort()
			with open(os.path.join(runsDir, r, "qual.html"), 'w') as index:
				print >>index, qual_template.render(runname=r, samples=samples)
		except OSError, e:
			print >>sys.stderr, "Diretorio fastQCresult não existe: ",e
		with open(os.path.join(runsDir, r, "map.html"), 'w') as index:
			print >>index, map_template.render(runname=r)
		
		vcfs = []
		snvs = [] 
		sinvs = [] 
		#ignoresnvs = ["brca1"]	
		try:
			for vcffilenames in os.listdir(os.path.join(runsDir, r, 'mapping', 'vcf')):
				if re.search(r"\.vcf$",vcffilenames):
					vcfs.append(vcffilenames)
			vcfs.sort()
			with open(os.path.join(runsDir, r, "vcf.html"), 'w') as index:
				print >>index, vcf_template.render(runname=r, vcfs=vcfs)

			for snvfilenames in os.listdir(os.path.join(runsDir, r, 'mapping', 'snv')):
				if re.search(r"\.snv",snvfilenames):
					snvs.append(snvfilenames)
				elif re.search(r"\.sinv",snvfilenames):
					sinvs.append(snvfilenames)
			snvs.sort()
			sinvs.sort()
			print >>sys.stderr, snvs
			with open(os.path.join(runsDir, r, "snv.html"), 'w') as index:
				print >>index, snv_template.render(runname=r,snvs=snvs, sinvs=sinvs)
		except OSError, e:
			print >>sys.stderr, "Diretorio mapping inexistente ou incompleto: ",e

		
