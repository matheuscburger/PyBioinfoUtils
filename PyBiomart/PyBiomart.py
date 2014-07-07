#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Matheus Carvalho Bürger'
__email__ = 'matheus.cburger@gmail.com'
__license__ = 'gpl'

import urllib2, sys

class PyBiomart(object):
	def __init__(self, mart="ensembl", server="http://www.biomart.org/biomart/", store=True):
		self.mart = mart
		self.server = server
		self.dataset = None
		self.filters = {}
		self.attributes = []
		self.store = store
		self.__lDatasets = None
		self.__lFilters = None
		self.__lAttributes = None

	def __str__(self):
		str = self.__repr__()
		str += '\nMart :\t%s\n' % self.mart
		str += 'Dataset :\t%s\n' % self.dataset
		str += '#Filters :\t%s\n' % len(self.filters)
		str += '#Attr :\t%s\n' % len(self.attributes)
		return str

	def listDatasets(self):
		if not self.__lDatasets:
			query = "%s/martservice?type=datasets&mart=%s" % (self.server,self.mart)
			result = []
			try:
				fl = urllib2.urlopen(query)
			except urllib2.URLError,e:
				sys.stderr.write("Unable to open URL: %s", str(e.code))
				raise
			except:
				sys.stderr.write("Unexpected error!\n")
				raise
			for line in fl:
				line = line.strip()
				if len(line):
					result.append(line.split('\t')[1:3])
			fl.close()
			if self.store:
				self.__lDatasets = result

		else:
			result = self.__lDatasets
		return result

	def setDataset(self, dataset):
		datasets = set([i[0] for i in self.listDatasets()])
		if dataset in datasets:
			self.dataset = dataset
		else:
			sys.stderr.write("Error! Please choose a mart.\n")

	def getDataset(self):
		return self.dataset


	def listFilters(self):
		if not self.dataset:
			sys.stderr.write("Please choose a dataset.")
			return
		if not self.__lFilters:
			query = "%s/martservice?type=filters&dataset=%s" % (self.server,self.dataset)
			result = []
			try:
				fl = urllib2.urlopen(query)
			except urllib2.URLError,e:
				sys.stderr.write("Unable to open URL: %s", str(e.code))
				raise
			for line in fl:
				line = line.strip()
				if len(line):
					result.append(line.split('\t')[0:2])
			fl.close()
			if self.store:
				self.__lFilters = result
		else:
			result = self.__lFilters
		return result

	def addFilter(self, filter):
		filters = set([i[0] for i in self.listFilters()])
		if not self.filters.has_key(filter):
			if filter in filters:
				self.filters[filter] = []
			else:
				sys.stderr.write("Error! Please choose a valid filter.\n")

	def getFilters(self):
		return self.filters


	def addFilterValues(self, filter, values):
		if self.filters.has_key(filter):
			self.filters[filter].extend(values)
		else:
			sys.stderr.write("Error! Please choose a valid filter.\n")

	def listAttributes(self):
		if not self.dataset:
			sys.stderr.write("Please choose a dataset.")
			return
		if not self.__lAttributes:
			query = "%s/martservice?type=attributes&dataset=%s" % (self.server,self.dataset)
			result = []
			try:
				fl = urllib2.urlopen(query)
			except urllib2.URLError,e:
				sys.stderr.write("Unable to open URL: %s", str(e.code))
				raise
			for line in fl:
				line = line.strip()
				if len(line):
					result.append(line.split('\t')[0:2])
			fl.close()
			if self.store:
				self.__lAttributes = result
		else:
			result = self.__lAttributes
		return result

	def addAttribute(self, attr):
		attrs = set([i[0] for i in self.listAttributes()])
		if attr in attrs:
			self.attributes.append(attr)
		else:
			sys.stderr.write("Error! Please choose a valid attribute.\n")

	def getAttributes(self):
		return self.attributes

	def setMart(self, mart):
		self.mart = mart

	def getMart(self):
		return self.mart
	
	def getQuery(self):
		if not self.dataset:
			sys.stderr.write("Please choose a dataset.")
			return
		query = 'query=<!DOCTYPE Query> <Query client="biomartclient" processor="TSV" limit="-1" header="1" uniqueRows="1">\
		<Dataset name="%s" config="%s_config">' % (self.dataset, self.dataset)
		for filter in self.filters:
			query += '<Filter name="%s" value="' % (filter)
			for value in self.filters[filter]:
				query += '%s,' % (value)
			query += '"/>'
		for attr in self.attributes:
			query += '<Attribute name="%s" />' % (attr)
		query += '</Dataset></Query>'
		return query


	def query(self):
		query = self.getQuery()
		try:
			req = urllib2.Request(url=self.server+"/martservice/results", data=query)
			fl = urllib2.urlopen(req)
		except urllib2.URLError,e:
			sys.stderr.write("Unable to open URL: %s", str(e.code))
			raise
		except:
			sys.stderr.write("Unexpected error!\n")
			raise

		return fl.read()

	def __convertQuery__(self, filter, attr):
		if not self.dataset:
			sys.stderr.write("Please choose a dataset.")
			return
		query = 'query=<!DOCTYPE Query> <Query client="biomartclient" processor="TSV" limit="-1" header="1" uniqueRows="1">\
		<Dataset name="%s" config="%s_config">' % (self.dataset, self.dataset)
		query += '<Filter name="%s" value="' % (filter)
		for value in self.filters[filter]:
			query += '%s,' % (value)
		query += '"/> <Attribute name="%s" /> <Attribute name="%s" /> </Dataset></Query>' % (filter, attr)
		try:
			req = urllib2.Request(url=self.server+"/martservice/results", data=query)
			fl = urllib2.urlopen(req)
		except urllib2.URLError,e:
			sys.stderr.write("Unable to open URL: %s", str(e.code))
			raise
		except:
			sys.stderr.write("Unexpected error!\n")
			raise
		return fl

	def convert(self, filter, attr):
		result = {}
		if self.filters.has_key(filter) and (attr in set(self.attributes)):
			fl = self.__convertQuery__(filter, attr)
			fl.readline()
			for line in fl:
				vline = line.strip().split("\t")
				if len(vline) > 1:
					if not result.has_key(vline[0]):
						result[vline[0]] = []
					result[vline[0]].append(vline[1])
		else:
			sys.stderr.write("Please, choose valid filter and attribute!\n")
			return
		return result	




if __name__ == "__main__":
	pbm = PyBiomart(store=False)
	print "Mart :", pbm.getMart()
	#print "Datasets :", pbm.listDatasets()
	pbm.setDataset("hsapiens_gene_ensembl")
	#print "Filters :", pbm.listFilters()
	pbm.addFilter("entrezgene")
	print "Filters :", pbm.getFilters()
	pbm.addFilterValues('entrezgene', ['596', '7157', '10211'])
	print "Filters :", pbm.getFilters()
	#print pbm.listAttributes()
	pbm.addAttribute("entrezgene")
	pbm.addAttribute("ensembl_gene_id")
	pbm.addAttribute("hgnc_symbol")
	print "Attributes :", pbm.getAttributes()
	print "QUERY :", pbm.getQuery()
	print "RESULT :", pbm.query()
	print pbm.convert("entrezgene", "ensembl_gene_id")
	print pbm.convert("entrezgene", "hgnc_symbol")



#class BMError(Exception):
#	def __init__(self, value):
#		self.value = value
#	def __str__()
