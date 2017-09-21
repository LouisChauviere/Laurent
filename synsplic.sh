#! /bin/bash

#################################################
#           Louis Chauviere                     #
#           June 02nd 2015                      #
#           Inserm UMR 702 			#
#################################################

#Filter for variant type: nonsynonymous, stopgain and splicing



for list in *
	do
	grep -E nonsynonymous\|Func.refGene\|stopgain\|stoploss $list > synsplic_$list
	done

#python ~/Documents/Vrai/scripts/eurinf1.py
