import os
import lxml.etree
import xml.etree.ElementTree as ET
import numpy as np
from weighted_levenshtein import lev, osa, dam_lev

insert_costs = np.ones(128, dtype=np.float64)
delete_costs = np.ones(128, dtype=np.float64)
# ebb: On weighted levenshtein w numpy see https://weighted-levenshtein.readthedocs.io/en/master/
# make an array of all 1's of size 128, the number of ASCII characters
substitute_costs = np.ones((128, 128), dtype=np.float64)
# This array is 2-dimensional, unlike the others.)
transpose_costs = np.ones((128, 128), dtype=np.float64)
# ebb: Let's try altering this transpose score to .5 if a condition is met below:
# ONLY when the MS witness is present in a rdgGrp,
# since MS features many tiny and probably not very interesting transpositions


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

Root = ET.Element("xml")

f = open('spineData-ascii.txt')
f.readline() # read and ignore the first line
for line in f: # iterate over the remaining lines
    v = line.split('\t')
    app = v[0]
    rg1_2 = v[1] + '::' + v[3]
    if '#fMS' in rg1_2:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist1_2 = dam_lev(v[2], v[4], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist1_2 = dam_lev(v[2], v[4])

    rg1_3 = v[1] + '::' + v[5]
    if '#fMS' in rg1_3:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist1_3 = dam_lev(v[2], v[6], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist1_3 = dam_lev(v[2], v[6])

    rg1_4 = v[1] + '::' + v[7]
    if '#fMS' in rg1_4:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist1_4 = dam_lev(v[2], v[8], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist1_4 = dam_lev(v[2], v[8])

    rg1_5 = v[1] + '::' + v[9]
    if '#fMS' in rg1_5:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist1_5 = dam_lev(v[2], v[10], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist1_5 = dam_lev(v[2], v[10])

    rg2_3 = v[3] + '::' + v[5]
    if '#fMS' in rg2_3:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist2_3 = dam_lev(v[4], v[6], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist2_3 = dam_lev(v[4], v[6])

    rg2_4 = v[3] + '::' + v[7]
    if '#fMS' in rg2_4:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist2_4 = dam_lev(v[4], v[8], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist2_4 = dam_lev(v[4], v[8])

    rg2_5 = v[3] + '::' + v[9]
    if '#fMS' in rg2_5:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist2_5 = dam_lev(v[4], v[10], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist2_5 = dam_lev(v[4], v[10])

    rg3_4 = v[5] + '::' + v[7]
    if '#fMS' in rg3_4:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist3_4 = dam_lev(v[6], v[8], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist3_4 = dam_lev(v[6], v[8])

    rg3_5 = v[5] + '::' + v[9]
    if '#fMS' in rg3_5:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist3_5 = dam_lev(v[6], v[10], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist3_5 = dam_lev(v[6], v[10])

    rg4_5 = v[7] + '::' + v[9]
    if '#fMS' in rg4_5:
        print('#fMS is here')
        transpose_costs = np.full((128, 128), 0.25, dtype=np.float64)
        dist4_5 = dam_lev(v[8], v[10], transpose_costs=transpose_costs)
    else:
        transpose_costs = np.ones((128, 128), dtype=np.float64)
        dist4_5 = dam_lev(v[8], v[10])

    FS = ET.SubElement(Root, 'fs', attrib={'feats': app})
    f1_2 = ET.SubElement(FS, 'f', attrib={'name': rg1_2, 'fVal': str(dist1_2)})
    f1_3 = ET.SubElement(FS, 'f', attrib={'name': rg1_3, 'fVal': str(dist1_3)})
    f1_4 = ET.SubElement(FS, 'f', attrib={'name': rg1_4, 'fVal': str(dist1_4)})
    f1_5 = ET.SubElement(FS, 'f', attrib={'name': rg1_5, 'fVal': str(dist1_5)})
    f2_3 = ET.SubElement(FS, 'f', attrib={'name': rg2_3, 'fVal': str(dist2_3)})
    f2_4 = ET.SubElement(FS, 'f', attrib={'name': rg2_4, 'fVal': str(dist2_4)})
    f2_5 = ET.SubElement(FS, 'f', attrib={'name': rg2_5, 'fVal': str(dist2_5)})
    f3_4 = ET.SubElement(FS, 'f', attrib={'name': rg3_4, 'fVal': str(dist3_4)})
    f3_5 = ET.SubElement(FS, 'f', attrib={'name': rg3_5, 'fVal': str(dist3_5)})
    f4_5 = ET.SubElement(FS, 'f', attrib={'name': rg4_5, 'fVal': str(dist4_5)})

tree = ET.ElementTree(Root)
tree.write('FV_LevDists-weighted.xml')
f.close()