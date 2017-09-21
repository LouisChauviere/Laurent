#!/usr/bin/python

import os
import re
import argparse

"""
Louis Chauviere
03/11/2016
Inserm UMR-S 1155

Script that will filter an Annotated Annovar file that describe genotypes from a trio (Father, Mother, Child).
It will return variants that can be considered as Compound Heterozygous in Annotated Annovar file.
"""


def main():
	inputfile, outputfile = commandLine()
	fich = open(inputfile,'r')
	out = open(outputfile, 'w')
	for lines in fich:
		matchHeader = re.search(r'Func.refGene', lines)
		if matchHeader:
			out.write(lines)
		else:
			line = lines.split("\t")
			genoChild = line[65].split(":")[0]
			genoFather = line[63].split(":")[0]
			genoMother = line[64].split(":")[0]
			matchBarre = re.search(r'\|', genoChild)
			if matchBarre:
				homoChild = homoOrNot("|", genoChild)
				orNotGenoFather = noGeno("|", genoFather)
				orNotGenoMother = noGeno("|", genoMother)
			else:
				homoChild = homoOrNot("/", genoChild)
				orNotGenoFather = noGeno("/", genoFather)
				orNotGenoMother = noGeno("/", genoMother)
			#Interesting variant must not be homozygous in child
			if not homoChild:
				#Qphred > 30 and coverage > 20
				if quality(65, line):
					#The alternative variant must be present in Mother or Father but not in both parents
					if not orNotGenoFather and orNotGenoMother and quality(63, line):
						out.write(lines)
					elif not orNotGenoMother and orNotGenoFather and quality(64, line):
						out.write(lines)
	out.close()
	fich.close()

#Will return True if a variant is homozygous reference for an individual
def noGeno(symbol, geno):
	if geno == "0" + symbol + "0" or geno == "." + symbol + ".":
		return True
	else:
		return False

#Will return True if a variant is homozygous for an individual
def homoOrNot(symbol, geno):
	print geno + "  " + symbol
	if geno.split(symbol)[0] == geno.split(symbol)[1]:
		return True
	else:
		return False

#Qphred >= 30 and coverage >= 20
def quality(nb, line):
	if int(line[nb].split(":")[2]) >= 30 and int(line[nb].split(":")[3]) >= 20:
		return True
	else:
		return False

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
