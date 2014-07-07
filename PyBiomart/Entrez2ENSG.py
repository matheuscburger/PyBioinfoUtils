#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Matheus Carvalho Bürger'
__license__ = 'gpl'

from PyBiomart import PyBiomart
import sys

if __name__=="__main__":
	flentrez = open("entrezid.txt", "r")
	entrez = []
	for line in flentrez:
		entrez.append(line.strip())
	pbm = PyBiomart(store=True)
	pbm.setDataset("hsapiens_gene_ensembl")
	pbm.addFilter("entrezgene")
	pbm.addFilterValues("entrezgene", entrez)
	pbm.addAttribute("ensembl_gene_id")
	dict = pbm.convert("entrezgene", "ensembl_gene_id")
	for key in dict:
		print key,"\t",
		for value in dict[key]:
			print "%s," % (value), 
		print
	
