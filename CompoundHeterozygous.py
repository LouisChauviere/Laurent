#!/usr/bin/python

import os 
import re
import argparse

"""
Louis Chauviere
03/11/2016
Inserm UMR-S 1155

Search couples of compound heterozygous. 
Distance between two variants is not seen with this filtering.
"""

def main():
	inputfile, outputfile = commandLine()
	fich = open(inputfile, 'r')
	out = open(outputfile, 'w')
	gene_prec = ""
	heredity = ""
	compound = False
	geneDict = dict()
	for lines in fich:
		matchHeader = re.search(r'Func.refGene', lines)
		if matchHeader:
			out.write(lines)
		else:
			geneDict = createGenesLinesDictionaries(lines, geneDict)
			#is there two lines with the same gene name
	for gene in geneDict:
		if len(geneDict[gene]) > 1:
			father = False
			mother = False
			for elmts in geneDict[gene]:
				elmt = elmts.split("\t")
				matchPtsFather = re.search(r'\.', elmt[63].split(":")[0])
				matchPtsMother = re.search(r'\.', elmt[64].split(":")[0])
				matchZeroFather = re.search(r'0[\|/]0', elmt[63].split(":")[0])
				matchZeroMother = re.search(r'0[\|/]0', elmt[64].split(":")[0])
				if matchPtsFather or matchZeroFather:
					father = True
					#print elmts
				if matchPtsMother or matchZeroMother:
					#print gene
					mother = True
			print str(mother) + " " + str(father)
			if father and mother:
				#print "aaaa"
				for elmts2 in geneDict[gene]:
					out.write(elmts2)

def createGenesLinesDictionaries(lines, geneDict):
	line = lines.split("\t")
	if line[6] not in geneDict:
		geneDict[line[6]] = list()
	if lines not in geneDict[line[6]]:
		geneDict[line[6]].append(lines)
	#print geneDict
	return geneDict

#Use argparse for the command line
def commandLine():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputfile', action='store', help='Store the input file pathway : Annovar annotated file with in order Father, Mother, Child')
	parser.add_argument('outputfile', action='store', help='Store path for the outputfile : same annotated file, but after filtering')
	parser.add_argument("-d", "--description", help="Script description", action="store_true")

	results = parser.parse_args()
	if results.description:
		print "Script that will filter an Annotated Annovar file that describe genotypes from a trio (Father, Mother, Child)."
		print "It will return variants that can be considered as Compound Heterozygous"
	return results.inputfile, results.outputfile


	
if __name__ == '__main__':
	main()
