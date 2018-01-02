#! /bin/bash

#############################################
#             Louis Chauviere               #
#               17/11/2016                  #
#            Inserm UMR-S 1155              #
#############################################



path=~/path/to/vcf/files
vcf="_common_vcfname.vcf"
mother="MotherId"
father="FatherId"
child="ChildId"
family="familyId"


#If you have non zipped file : it can be zipped there
bgzip ${path}/${mother}${vcf}
bgzip ${path}/${father}${vcf}
bgzip ${path}/${child}${vcf}

#To index the vcf files
tabix -p vcf -f ${path}/${mother}${vcf}.gz
tabix -p vcf -f ${path}/${father}${vcf}.gz
tabix -p vcf -f ${path}/${child}${vcf}.gz

#To merge the vcf file.
#Order: FATHER, MOTHER, CHILD
bcftools merge $path/${father}${vcf}.gz ${path}/${mother}${vcf}.gz ${path}/${child}${vcf}.gz -o $path/merged_${family}.vcf

#Annotation with Annovar
perl ~/Documents/annovar/table_annovar.pl ${path}/merged_${family}.vcf ~/Documents/annovar/humandb/ -buildver hg19 -out ${path}/Annotes_merged_${family}.vcf -remove -protocol refGene,cytoBand,genomicSuperDups,esp6500siv2_all,1000g2014oct_all,1000g2014oct_afr,1000g2014oct_eas,1000g2014oct_eur,snp138,ljb26_all,exac03 -operation g,r,r,f,f,f,f,f,f,f,f -nastring . -vcfinput

#To get nonsynonymous SNPs
grep -E nonsynonymous\|Func.refGene\|stopgain\|stoploss ${path}/Annotes_merged_${family}.vcf.hg19_multianno.txt > ${path}/synsplic_${family}.vcf.hg19_multianno.txt


#Scripts to get Compound Heterozygous variants

python FirstCandidatesList.py ${path}/synsplic_${family}.vcf.hg19_multianno.txt ${path}/first_${family}.vcf.hg19_multianno.txt

python SameExon.py ${path}/first_${family}.vcf.hg19_multianno.txt ${path}/exon_first_${family}.vcf.hg19_multianno.txt

python SearchDomains.py ${path}/exon_first_${family}.vcf.hg19_multianno.txt ${path}/domain_exon_first_${family}.vcf.hg19_multianno.txt

python CompoundHeterozygous.py ${path}/domain_exon_first_${family}.vcf.hg19_multianno.txt ${path}/VoilaLesMagnifiquesHeterozygotesComposes_domain_exon_first_${family}.vcf.hg19_multianno.txt


