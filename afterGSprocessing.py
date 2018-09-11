import matplotlib.pyplot as plt
import numpy as np
import sys
from xlrd import *
from datetime import datetime

###########
## currently afterGS is hardcoded so please change that

aftergs="C:\Users\Austin\Downloads\logAfterGoldStandard.xlsx"
wb = open_workbook(aftergs)

umlsgrps = ["Activities and Behaviors", "Anatomy", "Chemicals and Drugs", "Concepts and Ideas", "Devices", "Disorders", "Genes and Molecular Sequences", "Geographic Areas", "Living Beings", "Objects", "Occupations", "Organizations", "Phenomena", "Physiology", "Procedures"]
semGrp = "SemanticGroup"
dates = "Timestamp"
dateList = []
grpDict = {}


for s in wb.sheets():
    semanticGroupInd = 0
    dateInd = 0
    dateHash = {}
    
    nonClassified = 0
    
     # Get Heading Indices
 # =============================================================================
    for col in range(s.ncols):
        if(s.cell(0,col).value == (semGrp)):
            semanticGroupInd=col
        elif(s.cell(0,col).value == (dates)):
            dateInd=col
    if(dateInd==0 and semanticGroupInd == 0):
        print("Headings not found. Please label SemanticGroup or Timestamp")
        sys.exit(1)

    # If Semantic Group is null then skip
#=============================================================================
 
    a1 = s.cell(1,5).value
    print(a1)
    a1_datetime = datetime(*xlrd.xldate_as_tuple(a1, wb.datemode))
    print 'datetime: %s' % a1_datetime
#    print(type(a1_datetime))
#    #dt_object = datetime.strptime(a1_datetime, "%Y-%b-%d")
#    

    for row in range(1, s.nrows):
        current_semgrp = s.cell(row,semanticGroupInd).value
        if(current_semgrp == "" or current_semgrp == u''):
            nonClassified+=1
            continue
        day_val = datetime(*xlrd.xldate_as_tuple(s.cell(row,dateInd).value, wb.datemode))
#        for col in range(s.ncols):
#            val.append(str(s.cell(row,col).value))
        day_val = str(day_val.month) + str( day_val.day) + str(day_val.year)
        if( day_val not in dateHash):
            dateHash[day_val] = []
            dateList.append(day_val)
        dateHash[day_val].append(s.cell(row,semanticGroupInd).value)
   # print(dateHash)
    
#   process results
#=============================
maxcount = 0

countSemGrpLst ={}
for day in dateHash:
    grpInc = {}
    semGrpLst = dateHash[day]
    for grp in semGrpLst:
        if( grp not in grpInc):
            grpInc[grp] = 0
        else:
            grpInc[grp] += 1
    for key in grpInc:
        count = grpInc[key]
        if count > maxcount:
            maxcount = count
        
    countSemGrpLst[day] = grpInc
    print(grpInc)
print(countSemGrpLst)
print("nonclassified rows:" + str(nonClassified))
    #=============================================================================
## test 1 for one val
## 
    
def plot_a_graph(ax, grp, onegrp):
    plt.plot(dateList, onegrp, lw=2, alpha=1, label = grp)

 
def one_grp_plot(grp):
    onegrp = []
    for day in dateList:
        if grp not in countSemGrpLst[day]:
            onegrp.append(0)
        else:
            onegrp.append(countSemGrpLst[day][grp])
    return onegrp
#grp = u'Physiology'

#_, ax = plt.subplots()
plt.figure(figsize=(30, 40))
for grp in umlsgrps:
    values = one_grp_plot(grp)
    plot_a_graph(plt, grp, values)

#plt.set_xlabel("Dates")
#plt.set_ylabel("Count")

plt.legend()
plt.show()
