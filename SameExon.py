#!/usr/bin/python

import os 
import re
import argparse

"""
Louis Chauviere
05/09/2016
Inserm UMR-S 1155


"""


def main():
	inputfile, outputfile = commandLine()
	fich = open(inputfile, 'r')
	out = open(outputfile, 'w')
	line_prec = ""
	exon_prec = ""
	gene_prec = ""
	geno_prec = ""
	pos_prec = 0
	for lines in fich:
		matchHeader = re.search(r'Func.refGene', lines)
		if matchHeader:
			out.write(lines)
		else:
			line = lines.split("\t")
			exon_name = line[9].split(":")[2]
			#print exon_name
			#print exon_prec
			if exon_prec != "":
				if exon_name == exon_prec or int(exon_name.split("exon")[1]) == int(exon_prec.split("n")[1]) + 1 or int(exon_name.split("exon")[1]) == int(exon_prec.split("n")[1]) - 1:
					
					if line[6] == gene_prec: 
						#and line[65].split(":")[0] != geno_prec:
						print exon_name
						dif = int(line[1]) - pos_prec
						if dif <= 100:
							out.write(line_prec)
							out.write(lines)
			line_prec = lines
			exon_prec = exon_name
			gene_prec = line[6]
			geno_prec = line[65].split(":")[0]
			pos_prec = int(line[1])


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
