#!/usr/bin/python

import os 
import re
import sys, getopt
import argparse
import urllib




"""
Louis Chauviere
Inserm UMR-S 1155
16/09/2016

UniprotKB parsing to get domains of each protein that have potential
compound heterozygous. Will select two variants that are on the same 
proteic domain.
"""

#!!! TO CHANGE : OR TO REDO CompoundHeterozygous.py OR TO DO BEFORE CompoundHeterozygous.py


def main():
	inputfile, outputfile = commandLine()
	fich = open(inputfile, 'r')
	out = open(outputfile, 'w')
	dicoHetero = dict()
	listLines = list()
	for lines in fich:
		matchHeader = re.search(r'Func.refGene', lines)
		line = lines.split("\t")
		if matchHeader:
			out.write(lines)
		else:
			if line[6] not in dicoHetero:
				dicoHetero[line[6]] = list()
			print line[9].split(":p.")[1]
			dicoHetero[line[6]].append(line[9].split(":p.")[-1])
			listLines.append(lines)
	fich.close()
	print dicoHetero
	for gene in dicoHetero:
		listPos = dicoHetero[gene]
		listSameDomain, ok = readUrlFile(gene, listPos)
		if ok:
			for elmt in listLines:
				if elmt.split("\t")[6] == gene and int(elmt.split("\t")[9].split(":p.")[-1][1:-1]) in listSameDomain:
					print elmt
					out.write(elmt)



	
def readUrlFile(gene, listPos):
	findUrl = urllib.urlopen("http://www.uniprot.org/uniprot/?query=" + gene + "+AND+reviewed%3Ayes+organism%3AHomo+sapiens&sort=score&format=xml&offset=1&limit=1")
	linesUrl = findUrl.readlines()
	dom = False
	begin = ""
	end = ""
	postest = 0
	listSameDomain = list()
	#XML file parsing
	for lineUrl in linesUrl:
		matchDomain = re.search(r'<feature type="domain"', lineUrl)
		matchPosBegin = re.search(r'<begin position=', lineUrl)
		matchPosEnd = re.search(r'<end position=', lineUrl)
		if matchDomain:
			dom = True
		if dom == True and matchPosBegin:
			begin = int(lineUrl.split("\"")[1])
		if dom == True and matchPosEnd:
			end = int(lineUrl.split("\"")[1])
			dom = False
			i = 0
			for pos in listPos:
				if int(pos[1:-1]) >= begin and int(pos[1:-1]) <= end:
					if i >= 1 and int(pos[1:-1]) not in listSameDomain:
						if i == 1 and postest not in listSameDomain:
							listSameDomain.append(postest)
						listSameDomain.append(int(pos[1:-1]))
						i += 1
					if int(pos[1:-1]) not in listSameDomain and i == 0:
						postest = int(pos[1:-1])
						i += 1
	print gene 
	print listSameDomain
	if listSameDomain:
		ok = True
	else:
		ok = False
	return listSameDomain, ok
	



#Use argparse for the command line	
def commandLine():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputfile', action='store', help='Store the input file path : results for genetic coumpound heterozygous')
	parser.add_argument('outputfile', action='store', help='Store path for the outputfile')
	
	results = parser.parse_args()
	return results.inputfile, results.outputfile
	
	
if __name__ == '__main__':
	main()
