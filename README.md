# Laurent
Compound_Heterozygous

###################################
# COMPOUND HETEROZYGOUS RESEARCH  #
#  WITH EXOME SEQUENCING DATA     #
###################################

###################################
#        Louis CHAUVIERE          #
#     	    UMR-S 1155            #
#           14/09/2016            #
###################################


#######################################
##Zip the three vcf files
#bgzip <FATHER>.exome.snp.vcf
#bgzip <MOTHER>.exome.snp.vcf
#bgzip <CHILD>.exome.snp.vcf
#######################################


#######################################
##Index vcf files
#tabix -p vcf <FATHER>.exome.snp.vcf.gz
#tabix -p vcf <MOTHER>.exome.snp.vcf.gz
#tabix -p vcf <CHILD>.exome.snp.vcf.gz
#######################################

#######################################
##      Merge vcf files              ##
#bcftools merge <FATHER>.exome.snp.vcf.gz <MOTHER>.exome.snp.vcf.gz <CHILD>.exome.snp.vcf.gz -o <MERGED_OUT>.vcf
#######################################


#######################################
##   Annotate vcf file with Annovar  ##
#perl ~/Documents/annovar/table_annovar.pl <MERGED_OUT>.vcf ~/Documents/annovar/humandb/ -buildver hg19 -out Annotes_<MERGED_OUT>.vcf -remove -protocol refGene,cytoBand,genomicSuperDups,esp6500siv2_all,1000g2014oct_all,1000g2014oct_afr,1000g2014oct_eas,1000g2014oct_eur,snp138,ljb26_all,exac03 -operation g,r,r,f,f,f,f,f,f,f,f -nastring . -vcfinput
#######################################


######################################################
##   Options for Compound  Heterozygous research    ##
##Nonsynonymous variants : only the vcf file must be in the folder
#bash synsplic.sh

##Search variants that have a good quality and a good coverage
##Search variant present in one of the two parents and heterozygous in the child
#python FirstCandidatesList.py [-h] [-d] inputfile outputfile

##Search variants that are in the same exon of the same gene
##This is an optional step: but faster for the next steps
#SameExon.py [-h] [-d] inputfile outputfile

##Search variants that are in the same domain
#python SearchDomains.py [-h] inputfile outputfile

##Search real Compound Heterozygous variants
#python CompoundHeterozygous.py [-h] [-d] inputfile outputfile
#######################################################
