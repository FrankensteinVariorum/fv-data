import os
import lxml.etree
import xml.etree.ElementTree as ET
import numpy as np
from weighted_levenshtein import lev, osa, dam_lev

# ebb: There are five possible rdgGrps for each app location,
# producing the following possible combinations:
# RG1 to RG2
# RG1 to RG3
# RG1 to RG4
# RG1 to RG5
# RG2 to RG3
# RG2 to RG4
# RG2 to RG5
# RG3 to RG4
# RG3 to RG5
# RG4 to RG5
# We'll map these to feature structures elements (from the TEI), like this:
# <fs feats="appID">
#    <f

Root = ET.Element("xml")


f = open('spineData-ascii.txt')
f.readline() # read and ignore the first line
for line in f: # iterate over the remaining lines
	v = line.split('\t')
	app = v[0]
	dist1_2 = distance(v[2], v[4])
	dist1_3 = distance(v[2], v[6])
	dist1_4 = distance(v[2], v[8])
	dist1_5 = distance(v[2], v[10])
	dist2_3 = distance(v[4], v[6])
	dist2_4 = distance(v[4], v[8])
	dist2_5 = distance(v[4], v[10])
	dist3_4 = distance(v[6], v[8])
	dist3_5 = distance(v[6], v[10])
	dist4_5_= distance(v[8], v[10])



	## OLD element constructions from Mitford experiment:
	TR = ET.SubElement(Root, "fs", title="vars")
	TD1 = ET.SubElement(TR, "td")
	TD1.text = v[0]
	TD2 = ET.SubElement(TR, "td")
	TD2.text = str(dist1_2)
	TD3 = ET.SubElement(TR, "td")
	TD3.text = str(dist1_3)
	TD4 = ET.SubElement(TR, "td")
	TD4.text = str(dist1_4)
	TD5 = ET.SubElement(TR, "td")
	TD5.text = str(dist2_3)
	TD6 = ET.SubElement(TR, "td")
	TD6.text = str(dist2_4)
	TD7 = ET.SubElement(TR, "td")
	TD7.text = str(dist3_4)
	TRt = ET.SubElement(Table, "tr", title="texts")
	TDt0 = ET.SubElement(TRt, "td")
	TDt0.text = v[0]
	TDt1 = ET.SubElement(TRt, "td")
	TDt1.text = v[1]
	TDt2 = ET.SubElement(TRt, "td")
	TDt2.text = v[2]
	TDt3 = ET.SubElement(TRt, "td")
	TDt3.text = v[3]
	TDt4 = ET.SubElement(TRt, "td")
	TDt4.text = v[4]
	
#with open('LevDistsRienzi.xml','wb') as g:
#	g.write(lxml.etree.tostring(the_doc, pretty_print=True))
#print lxml.etree.tostring(the_doc, pretty_print=True)
tree = ET.ElementTree(Root)
tree.write('LevDistsRienziAll.xml')
f.close()

	#TRl = E.tr
	#TD = E.td
	#the_loop = TRl(
	#TD(dist1_2),
	#TD(dist1_3),
	#TD(dist1_4),
	#TD(dist2_3),
	#TD(dist2_4),
	#TD(dist3_4)
	#)
	    	
#the_doc = Root(
 #       	Table(
#        TR(TH('Locus'), TH('MS to 1828'), TH('MS to 1837'), TH('MS to 1854'), TH('1828 to 1837'), TH('1828 to 1854'), TH('1837 to 1854'))
		
	#	the_loop 
		#ebb: having trouble making a nested loop in constructed XML output. Running this produces a fatal error at this line. 
		#If I position the_doc and this tree builder to surround the for loop, this errors on the "for line in f:"
		#Does the for-loop and its dependents belong in a function?
        
     #   )
           
       # )  	
		