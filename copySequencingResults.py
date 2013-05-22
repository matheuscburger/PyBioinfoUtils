#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Matheus Carvalho Bürger'
__license__ = 'gpl'

import os
import shutil
import sys
from zipfile import ZipFile

if __name__ == "__main__":
	"""
	Objetivo: copiar resultados da analise dos dados provenientes do sequenciador
	para diretório acesso
	"""
	print (sys.version)
	originBase = "/home/solid/runsSOLEXA/"
	destBase = "/home/NGS/seqweb/htdocs/"
	fastQCDir =  'raw/fastQCresult/'
	resultsDir = [fastQCDir, 'mapping/vcf/', 'mapping/snv/' ]
	runs = os.listdir(originBase)
	for r in runs:
		if os.path.isdir(os.path.join(originBase, r)):
			print r
			try:
				os.mkdir(os.path.join(destBase, r))
			except OSError, e:
				print >>sys.stderr, "Não foi possivel criar diretório", e
			for results in resultsDir:
				try:
					shutil.copytree(os.path.join(originBase, r, results), os.path.join(destBase, r, results), ignore=shutil.ignore_patterns("*.pl", "*.py", "*pyc", "*.sh"))
				except OSError, e:
					print >>sys.stderr, "Não foi possivel copiar resultados", e
			try:
				for zipfilename in os.listdir(os.path.join(destBase, r, fastQCDir)):
					zip = ZipFile(os.path.join(destBase, r, fastQCDir, zipfilename), "r")
					zip.extractall(os.path.join(destBase, r, fastQCDir))
					zip.close()
			except OSError, e:
				print >>sys.stderr, "Não foi possivel descompactar resultados", e
	




			
