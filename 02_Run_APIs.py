#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:33:33 2018

@author: dan.wendling@nih.gov

Last modified: 2018-07-09


----------------
SCRIPT CONTENTS
----------------

1. Start-up
2. UmlsApi1 - Normalized string matching
3. Isolate entries updated by API, complete tagging, and match to the 
   current version of the search log - logAfterUmlsApi
4. Create logAfterUmlsApi as an update to logAfterGoldStandard by appending 
   newUmlsWithSemanticGroupData
5. Update GoldStandard
6. Create new 'uniques' dataframe/file for fuzzy matching


7. Google Translate API, https://cloud.google.com/translate/
But it's not free; https://stackoverflow.com/questions/37667671/is-it-possible-to-access-to-google-translate-api-for-free

8. UmlsApi2 - Tag non-English terms in Roman character sets



7. UmlsApi3 - Word matching (relax prediction rules )

8. RxNorm API

9. UmlsApi4 - Re-run first config - Create logAfterUmlsApi4 as an 
   update to logAfterUmlsApi by 
   
   append newUmlsWithSemanticGroupData
   
10. Create updated training file (GoldStandard) for ML script


----------------------------------
FIXME - DAN'S TO-DO ITEMS FOR DAN
----------------------------------

Change SemanticNetworkReference.UniqueID to SemanticTypeCode
Add SemanticNetworkReference.SemanticTypeCode to what goes into the logs, for ML.


----------
RESOURCES
----------

Register at UMLS, get a UMLS-UTS API key, and add it below. This is the 
primary source for Semantic Type classifications.
https://documentation.uts.nlm.nih.gov/rest/authentication.html
UMLS quick start: 
UMLS description of what Normalized String option is, 
https://uts.nlm.nih.gov/doc/devGuide/webservices/metaops/find/find2.html
"""


#%%
# ============================================
# 1. Start-up / What to put into place, where
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import numpy as np
import requests
import json
import lxml.html as lh
from lxml.html import fromstring
import time
import os

# Set working directory
os.chdir('/Users/johnsonnicl/Desktop/NIHHackathon/Python-app-to-analyze-the-site-search-logs-of-any-health-medical-life-sciences-site-')


localDir = '02_Run_APIs_files/'

# If you're starting a new session an this is not already open
listOfUniqueUnassignedAfterGS = 'listOfUniqueUnassignedAfterGS.xlsx'
listOfUniqueUnassignedAfterGS = pd.read_excel(listOfUniqueUnassignedAfterGS)

# Bring in historical file of (somewhat edited) matches
GoldStandard = 'GoldStandard.xlsx'
GoldStandard = pd.read_excel(GoldStandard)



# Get API key
def get_umls_api_key(filename=None):
    key = os.environ.get('UMLS_API_KEY', None)
    if key is not None:
        return key
    if filename is None:
          path = os.environ.get('HOME', None)
          if path is None:
               path = os.environ.get('USERPROFILE', None)
          if path is None:
               path = '.'
          filename = os.path.join(path, '.umls_api_key')
    with open(filename, 'r') as f:
           key = f.readline().strip()
    return key

myUTSAPIkey = get_umls_api_key()


'''
GoldStandard.xlsx - Already-assigned term list, from UMLS and other sources, 
    vetted.
'''


'''
SemanticNetworkReference - Customized version of the list at 
https://www.nlm.nih.gov/research/umls/META3_current_semantic_types.html, 
to be used to put search terms into huge bins. Should be integrated into 
GoldStandard and be available at the end of the ML matching process.
'''
SemanticNetworkReference = 'SemanticNetworkReference.xlsx'


''' 
- Run what remains against the UMLS API.

Requires having your own license and API key; see https://www.nlm.nih.gov/research/umls/
Not shown here: 
    - In huge files I sort by count and focus on terms searched by multiple
    or many people. The 'long tail' can be huge.
    - I have a database of terms aready assigned. I match these before 
    contacting UMLS; no need to check them again. Shortens processing time.
More options:
    https://documentation.uts.nlm.nih.gov/rest/home.html
    https://documentation.uts.nlm.nih.gov/rest/concept/

'''



# unassignedAfterUmls1 = pd.read_excel(localdir + 'unassignedAfterUmls1.xlsx')

'''
Register at RxNorm, get API key, and add it below. This is for drug misspellings.
'''

# Generate a one-day Ticket-Granting-Ticket (TGT)
tgt = requests.post('https://utslogin.nlm.nih.gov/cas/v1/api-key', data = {'apikey':myUTSAPIkey})
# For API key get a license from https://www.nlm.nih.gov/research/umls/
# tgt.text
response = fromstring(tgt.text)
todaysTgt = response.xpath('//form/@action')[0]

uiUri = "https://uts-ws.nlm.nih.gov/rest/search/current?"
semUri = "https://uts-ws.nlm.nih.gov/rest/content/current/CUI/"



#%%
# =========================================
# 2. UmlsApi1 - Normalized string matching
# =========================================
'''
In this run the API calls use the Normalized String setting. Example: 
for the input string Yellow leaves, normalizedString would return two strings, 
leaf yellow and leave yellow. Each string would be matched exactly to the 
strings in the normalized string index to return a result. 

Re-start:
# listOfUniqueUnassignedAfterGS = pd.read_excel('listOfUniqueUnassignedAfterGS.xlsx')

listToCheck6 = pd.read_excel(localDir + 'listToCheck6.xlsx')
listToCheck7 = pd.read_excel(localDir + 'listToCheck7.xlsx')
'''

# ---------------------------------------
# Batch rows so you can do separate runs
# Max of 5,000 rows per run
# ---------------------------------------

# uniqueSearchTerms = search['adjustedQueryCase'].unique()

# Reduce entry length, to focus on single concepts that UTS API can match
listOfUniqueUnassignedAfterGS = listOfUniqueUnassignedAfterGS.loc[(listOfUniqueUnassignedAfterGS['adjustedQueryCase'].str.len() <= 20) == True]


# listToCheck1 = unassignedAfterGS.iloc[0:20]
listToCheck1 = listOfUniqueUnassignedAfterGS.iloc[0:6000]
listToCheck2 = listOfUniqueUnassignedAfterGS.iloc[6001:12000]
listToCheck3 = listOfUniqueUnassignedAfterGS.iloc[12001:18000]
listToCheck4 = listOfUniqueUnassignedAfterGS.iloc[18001:24000]
listToCheck5 = listOfUniqueUnassignedAfterGS.iloc[24001:30000]
listToCheck6 = listOfUniqueUnassignedAfterGS.iloc[30001:36000]
listToCheck7 = listOfUniqueUnassignedAfterGS.iloc[36001:39523]



'''
listToCheck1 = unassignedToCheck.iloc[12497:20000]
listToCheck2 = unassignedToCheck.iloc[20001:26000]
listToCheck3 = unassignedToCheck.iloc[23225:28000]
listToCheck4 = unassignedToCheck.iloc[28001:31256]

mask = (unassignedToCheck['adjustedQueryCase'].str.len() <= 15)
listToCheck3 = listToCheck3.loc[mask]
listToCheck4 = listToCheck4.loc[mask]
'''


# If multiple sessions required, saving to file might help
writer = pd.ExcelWriter(localDir + 'listToCheck7.xlsx')
listToCheck7.to_excel(writer,'listToCheck7')
# df2.to_excel(writer,'Sheet2')
writer.save()

writer = pd.ExcelWriter(localDir + 'listToCheck2.xlsx')
listToCheck2.to_excel(writer,'listToCheck2')
# df2.to_excel(writer,'Sheet2')
writer.save()

'''
OPTIONS

# Bring in from file
listToCheck3 = pd.read_excel(localDir + 'listToCheck3.xlsx')
listToCheck4 = pd.read_excel(localDir + 'listToCheck4.xlsx')

listToCheck1 = unassignedAfterGS
listToCheck2 = unassignedAfterGS.iloc[5001:10000]
listToCheck1 = unassignedAfterGS.iloc[10001:11335]
'''


#%% 
# ----------------------------------------------------------
# Run this block after changing listToCheck# top and bottom
# ----------------------------------------------------------
'''
Until you put this into a function, you need to change listToCheck# 
and apiGetNormalizedString# counts every run!
Stay below 30 API requests per second. With 4 API requests per item
(2 .get and 2 .post requests)...
time.sleep commented out: 6,000 / 35 min = 171 per minute = 2.9 items per second / 11.4 requests per second
Computing differently, 6,000 items @ 4 Req per item = 24,000 Req, divided by 35 min+
686 Req/min = 11.4 Req/sec
time.sleep(.07):  ~38 minutes to do 6,000; 158 per minute / 2.6 items per second
'''

apiGetNormalizedString = pd.DataFrame()
apiGetNormalizedString['adjustedQueryCase'] = ""
apiGetNormalizedString['preferredTerm'] = ""
apiGetNormalizedString['SemanticTypeName'] = ""

'''
For file 6, 7/5/18 1:05 p.m.: SSLError: HTTPSConnectionPool(host='utslogin.nlm.nih.gov', 
port=443): Max retries exceeded with url: 
/cas/v1/api-key/TGT-480224-qLwYAMKl5cTfa7Jwb7RWZ3kfexPUm479HfddD7yVUKt79lZ0Ta-cas 
(Caused by SSLError(SSLError("bad handshake: SysCallError(60, 'ETIMEDOUT')",),))

Later, run 6 and 7
'''


for index, row in listToCheck7.iterrows():
    currLogTerm = row['adjustedQueryCase']
    # === Get 'preferred term' and its concept identifier (CUI/UI) =========
    stTicket = requests.post(todaysTgt, data = {'service':'http://umlsks.nlm.nih.gov'}) # Get single-use Service Ticket (ST)
    # Example: GET https://uts-ws.nlm.nih.gov/rest/search/current?string=tylenol&sabs=MSH&ticket=ST-681163-bDfgQz5vKe2DJXvI4Snm-cas
    tQuery = {'string':currLogTerm, 'searchType':'normalizedString', 'ticket':stTicket.text} # removed 'sabs':'MSH', 
    getPrefTerm = requests.get(uiUri, params=tQuery)
    getPrefTerm.encoding = 'utf-8'
    tItems  = json.loads(getPrefTerm.text)
    tJson = tItems["result"]
    if tJson["results"][0]["ui"] != "NONE": # Sub-loop to resolve "NONE"
        currUi = tJson["results"][0]["ui"]
        currPrefTerm = tJson["results"][0]["name"]
        # === Get 'semantic type' =========
        stTicket = requests.post(todaysTgt, data = {'service':'http://umlsks.nlm.nih.gov'}) # Get single-use Service Ticket (ST)
        # Example: GET https://uts-ws.nlm.nih.gov/rest/content/current/CUI/C0699142?ticket=ST-512564-vUxzyI00ErMRm6tjefNP-cas
        semQuery = {'ticket':stTicket.text}
        getPrefTerm = requests.get(semUri+currUi, params=semQuery)
        getPrefTerm.encoding = 'utf-8'
        semItems  = json.loads(getPrefTerm.text)
        semJson = semItems["result"]
        currSemTypes = []
        for name in semJson["semanticTypes"]:
            currSemTypes.append(name["name"]) #  + " ; "
        # === Post to dataframe =========
        apiGetNormalizedString = apiGetNormalizedString.append(pd.DataFrame({'adjustedQueryCase': currLogTerm, 
                                                       'preferredTerm': currPrefTerm, 
                                                       'SemanticTypeName': currSemTypes[0]}, index=[0]), ignore_index=True)
        print('{} --> {}'.format(currLogTerm, currSemTypes[0])) # Write progress to console
        # time.sleep(.06)
    else:
       # Post "NONE" to database and restart loop
        apiGetNormalizedString = apiGetNormalizedString.append(pd.DataFrame({'adjustedQueryCase': currLogTerm, 'preferredTerm': "NONE"}, index=[0]), ignore_index=True)
        print('{} --> NONE'.format(currLogTerm, )) # Write progress to console
        # time.sleep(.06)
print ("* Done *")


writer = pd.ExcelWriter(localDir + 'apiGetNormalizedString7.xlsx')
apiGetNormalizedString.to_excel(writer,'apiGetNormalizedString')
# df2.to_excel(writer,'Sheet2')
writer.save()


# Free up memory: Remove listToCheck, listToCheck1, listToCheck2, listToCheck3, 
# listToCheck4, nonForeign, searchLog, unassignedAfterGS


#%%
# ==================================================================
# 3. Isolate entries updated by API, complete tagging, and match to 
# the current version of the search log - logAfterUmlsApi
# ==================================================================
'''
To Do:

    Isolate new assignments and:
    - merge them into the master version of the log
    - add to GoldStandard for next time
 
 # Move unassigned entries into workflow for human identification
 
To re-start

unassignedAfterGS = pd.read_excel(localDir + 'unassignedAfterGS.xlsx')
logAfterGoldStandard = pd.read_excel(localDir + 'logAfterGoldStandard.xlsx')

listFromApi = pd.read_excel('listFromApi1-April-May.xlsx')
assignedByUmlsApi = pd.read_excel(localDir + 'assignedByUmlsApi.xlsx')

# Fix temporary issue of nulls in SemanticTypeName, and wrong col name semTypeName
 
listFromApi.drop(['SemanticTypeName'], axis=1, inplace=True)
listFromApi.rename(columns={'semTypeName': 'SemanticTypeName'}, inplace=True)

# listFromApi = listFromApi.dropna(subset=['SemanticTypeName'])
 '''
 

# If you stored output from UMLS API in files, re-open and unite
newAssignments1 = pd.read_excel(localDir + 'apiGetNormalizedString1.xlsx')
newAssignments2 = pd.read_excel(localDir + 'apiGetNormalizedString2.xlsx')
newAssignments3 = pd.read_excel(localDir + 'apiGetNormalizedString3.xlsx')
newAssignments4 = pd.read_excel(localDir + 'apiGetNormalizedString4.xlsx')
newAssignments5 = pd.read_excel(localDir + 'apiGetNormalizedString5.xlsx')
newAssignments6 = pd.read_excel(localDir + 'apiGetNormalizedString6.xlsx')
newAssignments7 = pd.read_excel(localDir + 'apiGetNormalizedString7.xlsx')


# Put dataframes together into one; df = df1.append([df2, df3])
afterUmlsApi1 = newAssignments1.append([newAssignments2, newAssignments3, newAssignments4, newAssignments5])
afterUmlsApi1 = newAssignments6.append([newAssignments7])


'''
afterUmlsApi1 = afterUmlsApi1.append(newAssignments3)
afterUmlsApi1 = afterUmlsApi1.append(newAssignments4)
'''


# If you only used one df for listFromApi
# afterUMLSapi = listFromApi
# assignedByUmlsApi = listFromApi


# Reduce to a version that has only successful assignments

# Remove various problem entries
assignedByUmlsApi1 = afterUmlsApi1.loc[(afterUmlsApi1['preferredTerm'] != "NONE")]
assignedByUmlsApi1 = assignedByUmlsApi1[~pd.isnull(assignedByUmlsApi1['preferredTerm'])]
assignedByUmlsApi1 = assignedByUmlsApi1.loc[(assignedByUmlsApi1['preferredTerm'] != "Null Value")]
assignedByUmlsApi1 = assignedByUmlsApi1[~pd.isnull(assignedByUmlsApi1['adjustedQueryCase'])]


# If you want to send to Excel
writer = pd.ExcelWriter(localDir + 'assignedByUmlsApi1.xlsx')
assignedByUmlsApi1.to_excel(writer,'assignedByUmlsApi1')
# df2.to_excel(writer,'Sheet2')
writer.save()


# Bring in subject category master file
# SemanticNetworkReference = pd.read_excel(localDir + 'SemanticNetworkReference.xlsx')
SemanticNetworkReference = pd.read_excel(SemanticNetworkReference)

# Reduce to required cols
SemTypeData = SemanticNetworkReference[['SemanticTypeName', 'SemanticGroupCode', 'SemanticGroup', 'CustomTreeNumber', 'BranchPosition']]
# SemTypeData.rename(columns={'SemanticTypeName': 'semTypeName'}, inplace=True) # The join col

# Add more semantic tagging to new UMLS API adds
newUmlsWithSemanticGroupData = pd.merge(assignedByUmlsApi1, SemTypeData, how='left', on='SemanticTypeName')


#%%
# ============================================================================
# 4. Create logAfterUmlsApi as an update to logAfterGoldStandard by appending 
# newUmlsWithSemanticGroupData
# ============================================================================

'''
Depending on what you're processing, use this or the next section of the below.

Depends on how you choose to process - Like, down to one occurrence to API 
in first batch, or not.
'''


logAfterGoldStandard = 'logAfterGoldStandard.xlsx'
logAfterGoldStandard = pd.read_excel(logAfterGoldStandard)


'''
# FIXME - Remove after this is fixed within the fixme above.
logAfterGoldStandard = logAfterGoldStandard.sort_values(by='adjustedQueryCase', ascending=True)
logAfterGoldStandard = logAfterGoldStandard.reset_index()
logAfterGoldStandard.drop(['index'], axis=1, inplace=True)
'''


# Eyeball. If you need to remove rows...
# logAfterGoldStandard = logAfterGoldStandard.iloc[760:] # remove before index...

# Join new UMLS API adds to the current search log master
logAfterUmlsApi1 = pd.merge(logAfterGoldStandard, newUmlsWithSemanticGroupData, how='left', on='adjustedQueryCase')

logAfterUmlsApi1.columns

'''
['SessionID', 'StaffYN', 'Referrer', 'Query', 'Timestamp',
       'adjustedQueryCase', 'SemanticTypeName_x', 'SemanticGroup_x',
       'SemanticGroupCode_x', 'BranchPosition_x', 'CustomTreeNumber_x',
       'ResourceType', 'Address', 'EntrySource', 'contentSteward',
       'preferredTerm_x', 'SemanticTypeName_y', 'preferredTerm_y',
       'SemanticGroupCode_y', 'SemanticGroup_y', 'CustomTreeNumber_y',
       'BranchPosition_y']

'''


# Future: Look for a better way to do the above - MERGE WITH CONDITIONAL OVERWRITE. Temporary fix:
logAfterUmlsApi1['preferredTerm2'] = logAfterUmlsApi1['preferredTerm_x'].where(logAfterUmlsApi1['preferredTerm_x'].notnull(), logAfterUmlsApi1['preferredTerm_y'])
logAfterUmlsApi1['SemanticTypeName2'] = logAfterUmlsApi1['SemanticTypeName_x'].where(logAfterUmlsApi1['SemanticTypeName_x'].notnull(), logAfterUmlsApi1['SemanticTypeName_y'])
logAfterUmlsApi1['SemanticGroup2'] = logAfterUmlsApi1['SemanticGroup_x'].where(logAfterUmlsApi1['SemanticGroup_x'].notnull(), logAfterUmlsApi1['SemanticGroup_y'])
logAfterUmlsApi1['SemanticGroupCode2'] = logAfterUmlsApi1['SemanticGroupCode_x'].where(logAfterUmlsApi1['SemanticGroupCode_x'].notnull(), logAfterUmlsApi1['SemanticGroupCode_y'])
logAfterUmlsApi1['BranchPosition2'] = logAfterUmlsApi1['BranchPosition_x'].where(logAfterUmlsApi1['BranchPosition_x'].notnull(), logAfterUmlsApi1['BranchPosition_y'])
logAfterUmlsApi1['CustomTreeNumber2'] = logAfterUmlsApi1['CustomTreeNumber_x'].where(logAfterUmlsApi1['CustomTreeNumber_x'].notnull(), logAfterUmlsApi1['CustomTreeNumber_y'])
logAfterUmlsApi1.drop(['preferredTerm_x', 'preferredTerm_y',
                          'SemanticTypeName_x', 'SemanticTypeName_y',
                          'SemanticGroup_x', 'SemanticGroup_y',
                          'SemanticGroupCode_x', 'SemanticGroupCode_y',
                          'BranchPosition_x', 'BranchPosition_y', 
                          'CustomTreeNumber_x', 'CustomTreeNumber_y'], axis=1, inplace=True)
logAfterUmlsApi1.rename(columns={'preferredTerm2': 'preferredTerm',
                                    'SemanticTypeName2': 'SemanticTypeName',
                                    'SemanticGroup2': 'SemanticGroup',
                                    'SemanticGroupCode2': 'SemanticGroupCode',
                                    'BranchPosition2': 'BranchPosition',
                                    'CustomTreeNumber2': 'CustomTreeNumber'
                                    }, inplace=True)

# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'logAfterUmlsApi1.xlsx')
logAfterUmlsApi1.to_excel(writer,'logAfterUmlsApi1')
# df2.to_excel(writer,'Sheet2')
writer.save()

'''
To Do:
    - Create list of unmatched terms with freq
    - Cluster similar spellings together?
    
- Look at "Not currently matchable" terms with "high" frequency counts. Eyeball to see if these were incorrectly matched in the past; assign historical term or update all to new term, save in gold standard file.
- Process entries from the PubMed product page.
- If you haven't done so, update RegEx list to improve future matching.
- Every several months, through Flask interface, interactively update the gold standard, manually.

# Reduce logAfterUmlsApi to unique, unmatched entries, prep for ML

To re-start:
logAfterUmlsApi = pd.read_excel(localDir + 'logAfterUmlsApi.xlsx')
'''


# ------------------------------------
# Visualize results - logAfterUmlsApi
# ------------------------------------
    
# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logAfterUmlsApi1)
unassigned = logAfterUmlsApi1['SemanticGroup'].isnull().sum()
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=True, startangle=100)
plt.axis('equal')
plt.title("Status after 'UMLS API' processing")
plt.show()

# Bar of SemanticGroup categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterUmlsApi1['SemanticGroup'].value_counts().plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Categories assigned after 'UMLS API' processing", fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top 
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)

# Remove listOfUniqueUnassignedAfterGS, listToCheck1, etc., logAfterGoldStandard, logAfterUmlsApi1, 
# newAssignments1 etc.



#%%
# =======================
# 5. Update GoldStandard
# =======================

# Open GoldStandard if needed
GoldStandard = '01_Pre-processing_files/GoldStandard.xlsx'
GoldStandard = pd.read_excel(GoldStandard)

# Append fully tagged UMLS API adds to GoldStandard
GoldStandard = GoldStandard.append(newUmlsWithSemanticGroupData, sort=False)

# Reset index
GoldStandard = GoldStandard.reset_index()
GoldStandard.drop(['index'], axis=1, inplace=True)
# temp GoldStandard.drop(['adjustedQueryCase'], axis=1, inplace=True)

'''
Eyeball top and bottom of cols, remove rows by Index, if needed

GoldStandard.drop(58027, inplace=True)
'''


# Write out the updated GoldStandard
writer = pd.ExcelWriter('GoldStandard.xlsx')
GoldStandard.to_excel(writer,'GoldStandard')
writer.save()



#%%
# ============================================================================
# 6. Start new 'uniques' dataframe that gets new column for each of the below
# listOfUniqueUnassignedAfterUmls1
# ============================================================================

'''
To Do:
    - Create list of unmatched terms with freq
    - Cluster similar spellings together?
    
- Look at "Not currently matchable" terms with "high" frequency counts. Eyeball to see if these were incorrectly matched in the past; assign historical term or update all to new term, save in gold standard file.
- Process entries from the PubMed product page.
- If you haven't done so, update RegEx list to improve future matching.
- Every several months, through Flask interface, interactively update the gold standard, manually.

# Reduce logAfterUmlsApi to unique, unmatched entries, prep for ML

To re-start:
logAfterUmlsApi = pd.read_excel(localDir + 'logAfterUmlsApi.xlsx')
'''

listOfUniqueUnassignedAfterUmls1 = logAfterUmlsApi1[pd.isnull(logAfterUmlsApi1['SemanticGroup'])]
listOfUniqueUnassignedAfterUmls1 = listOfUniqueUnassignedAfterUmls1.groupby('adjustedQueryCase').size()
listOfUniqueUnassignedAfterUmls1 = pd.DataFrame({'timesSearched':listOfUniqueUnassignedAfterUmls1})
listOfUniqueUnassignedAfterUmls1 = listOfUniqueUnassignedAfterUmls1.sort_values(by='timesSearched', ascending=False)
listOfUniqueUnassignedAfterUmls1 = listOfUniqueUnassignedAfterUmls1.reset_index()

writer = pd.ExcelWriter(localDir + 'listOfUniqueUnassignedAfterUmls11.xlsx')
listOfUniqueUnassignedAfterUmls1.to_excel(writer,'unassignedToCheck')
writer.save()

# FY 18 Q3: 57,287


#%%
# =============================================================
# 5. Google Translate API, https://cloud.google.com/translate/
# =============================================================
'''
But it's not free; https://stackoverflow.com/questions/37667671/is-it-possible-to-access-to-google-translate-api-for-free
'''


#%%
# ==========================================================================
# 5. UmlsApi2 - Tag non-English terms in Roman character sets
# ==========================================================================
'''
Some foreign terms can be matched. This run does not return a preferred term,
just returns what vocabulary the term is found in. 

Queries with words not in English are ignored by the first API run using
"normalized string" matching. Here, try flagging what you can and take them 
out of the percent-complete calculation.

The API apparently only supports U.S. English. RegEx could be used to convert
UTF-8 Roman characters that are not English... Non-Roman languages (Chinese, 
Cyrillic, Arabic, Japanese, etc.) are not supported by the API; these should 
be kept out of the API runs entirely.

6/22/18, from David of UMLS support, TRACKING:000308010

> Can the UMLS REST API tell me the term's language? 

One option would be to specify returnIdType=sourceUi for your search 
request. For example: 
 
https://uts-ws.nlm.nih.gov/rest/search/current?string=Infarto de miocardio&returnIdType=sourceUi&ticket=

This will give you a set of codes back where there is a match, but will 
also return a vocabulary (rootSource). If you have that, you can get 
the language (in this case, Spanish). The first result may be all you 
need. If you have the rootSource, you can match it to the "abbreviation" 
and look up the language here: https://uts-ws.nlm.nih.gov/rest/metadata/current/sources. 
 
It won't be perfect. I'm seeing some problems with accented characters. 
For example, coração returns no results, so that's not great, but may 
not matter. Some strings will appear in multiple languages, too. 
 
Let me know how that works for you. - David
'''


# ------------------------------------------------------
# Batch up your API runs. Re-starting, correcting, etc.
# ------------------------------------------------------

# uniqueSearchTerms = search['adjustedQueryCase'].unique()

# vocabCheck1 = unassignedAfterGS.iloc[0:20]
vocabCheck1 = listOfUniqueUnassignedAfterUmls1.iloc[0:5000]
# vocabCheck2 = listOfUniqueUnassignedAfterUmls1.iloc[5001:10678]


# If multiple sessions required, saving to file might help
writer = pd.ExcelWriter(localDir + 'vocabCheck1.xlsx')
vocabCheck1.to_excel(writer,'vocabCheck')
# df2.to_excel(writer,'Sheet2')
writer.save()


'''
writer = pd.ExcelWriter(localDir + 'listToCheck2.xlsx')
listToCheck2.to_excel(writer,'listToCheck2')
# df2.to_excel(writer,'Sheet2')
writer.save()
'''


'''
OPTIONS

# Bring in from file
listToCheck3 = pd.read_excel('listToCheck3.xlsx')
listToCheck4 = pd.read_excel('listToCheck4.xlsx')

listToCheck1 = unassignedAfterGS
listToCheck2 = unassignedAfterGS.iloc[5001:10000]
listToCheck1 = unassignedAfterGS.iloc[10001:11335]
'''


'''
Work with PostMan app to test/approve

David from UMLS: One option would be to specify returnIdType=sourceUi for 
your search request. For example:
 
https://uts-ws.nlm.nih.gov/rest/search/current?string=Infarto de miocardio&returnIdType=sourceUi&ticket=

This will give you a set of codes back where there is a match, but will 
also return a vocabulary (rootSource). If you have that, you can get the 
language (in this case, Spanish). The first result may be all you need. 
If you have the rootSource, you can match it to the "abbreviation" and 
look up the language here: https://uts-ws.nlm.nih.gov/rest/metadata/current/sources. 
 
It won't be perfect. I'm seeing some problems with accented characters. 
For example, coração returns no results, so that's not great, but may 
not matter. Some strings will appear in multiple languages, too. 
 
Let me know how that works for you.
'''

'''
FIXME - Unfinished.

TGT-16294-ajZgfOTNGBxvzAXAvQslZtuL2U0HksFsED6tZ0ajoewNBNdSVz-cas


# THIS IS SOURCE VOCAB CODE

https://uts-ws.nlm.nih.gov/rest/search/current?string=Infarto de miocardio&returnIdType=sourceUi&ticket=
'''


#%%
# -----------------------------------
# Gather list of source vocabularies
# -----------------------------------

uiUri = "https://uts-ws.nlm.nih.gov/rest/search/current?returnIdType=sourceUi"

listOfSourceVocabularies = pd.DataFrame()
listOfSourceVocabularies['adjustedQueryCase'] = ""
listOfSourceVocabularies['sourceVocab'] = ""

for index, row in listToCheck1.iterrows():
    currLogTerm = row['adjustedQueryCase']
    # === Get 'source vocab' =========
    stTicket = requests.post(todaysTgt, data = {'service':'http://umlsks.nlm.nih.gov'}) # Get single-use Service Ticket (ST)
    # Example: GET https://uts-ws.nlm.nih.gov/rest/search/current?string=tylenol&sabs=MSH&ticket=ST-681163-bDfgQz5vKe2DJXvI4Snm-cas
    termQuery = {'string':currLogTerm, 'ticket':stTicket.text} # removed 'searchType':'word' (it's the default),      'sabs':'MSH', 
    getSourceVocab = requests.get(uiUri, params=termQuery)
    getSourceVocab.encoding = 'utf-8'
    tItems = json.loads(getSourceVocab.text)
    tJson = tItems["result"]
    if tJson["results"][0]["ui"] != "NONE": # Sub-loop to resolve "NONE"
        currUi = tJson["results"][0]["rootSource"]
        sourceVocab = tJson["results"][0]["rootSource"]
        # === Post to dataframe =========
        listOfSourceVocabularies = listOfSourceVocabularies.append(pd.DataFrame({'adjustedQueryCase': currLogTerm, 
                                                       'sourceVocab': sourceVocab}, index=[0]), ignore_index=True)
        print('{} --> {}'.format(currLogTerm, sourceVocab)) # Write progress to console
        time.sleep(.07)
    else:
       # Post "NONE" to database and restart loop
        listOfSourceVocabularies = listOfSourceVocabularies.append(pd.DataFrame({'adjustedQueryCase': currLogTerm, 'sourceVocab': "NONE"}, index=[0]), ignore_index=True)
        print('{} --> NONE'.format(currLogTerm, )) # Write progress to console
        time.sleep(.07)
print ("* Done *")


writer = pd.ExcelWriter(localDir + 'listOfSourceVocabularies.xlsx')
listOfSourceVocabularies.to_excel(writer,'listOfSourceVocabularies')
# df2.to_excel(writer,'Sheet2')
writer.save()

# Free up memory: Remove listToCheck, listToCheck1, listToCheck2, listToCheck3, 
# listToCheck4, nonForeign, searchLog, unassignedAfterGS


#%%

# Load external reference file: SourceVocabsForeign.xlsx

# F&R Foreign vocab names with the language name, "Spanish," "Swedish"

# Append to running list of updates



# ------------------------------------------------------
# Match vocabCheck 
# ------------------------------------------------------
'''
FIXME - RESULTING LIST NEEDS TO BE VETTED; START WITH HIGHEST-FREQUENCY USE.

Update naming? this is the result from the API run for languages

This custom list of vocabs does not include and English vocabs, therefore, 
only foreign matches are returned, which is what we want.

Re-start:
listOfSourceVocabularies = pd.read_excel(localDir + 'listOfSourceVocabularies.xlsx')
'''

# Load list of Non-English vocabularies
# 7/5/2018, https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html (English vocabs not included.)
UMLS_NonEnglish_Vocabularies = pd.read_excel(localDir + 'UMLS_Non-English_Vocabularies.xlsx')

# Inner join
foreignButEnglishChar = pd.merge(listOfSourceVocabularies, UMLS_NonEnglish_Vocabularies, how='inner', left_on='sourceVocab', right_on='Vocabulary')


# Get frequency count, reduce cols for easier manual checking
PerhapsForeign = pd.merge(foreignButEnglishChar, listOfUniqueUnassignedAfterUmls1, how='inner', on='adjustedQueryCase')

PerhapsForeign = PerhapsForeign.sort_values(by='timesSearched', ascending=False)
PerhapsForeign = PerhapsForeign.reset_index()
PerhapsForeign.drop(['index'], axis=1, inplace=True)
col = ['adjustedQueryCase', 'timesSearched', 'Language']
PerhapsForeign = PerhapsForeign[col]
PerhapsForeign.rename(columns={'Language': 'LanguageGuess'}, inplace=True)

# Send out for manual checking
writer = pd.ExcelWriter(localDir + 'PerhapsForeign.xlsx')
PerhapsForeign.to_excel(writer,'PerhapsForeign')
# df2.to_excel(writer,'Sheet2')
writer.save()

'''
In Excel or Flask, delete rows with terms that we use in English; check that 
tyhe remaining rows contain terms that most English speakers would think are 
foriegn. 
Supplement cols for the definite foreign terms, append to GoldStandard as 
foreign terms.
'''

#%%

# Update GoldStandard with edits from PerhapsForeign result

# Update current log file from PerhapsForeign result

# Create new 'uniques' list for FuzzyWuzzy






#%%
# ===========================================================================
# 5. Second UMLS API clean-up - Create logAfterUmlsApi2 as an 
# update to logAfterUmlsApi by appending newUmlsWithSemanticGroupData
# ===========================================================================
'''
Use this AFTER you do a SECOND run against the UMLS Metathesaurus API.

Re-start: 
logAfterUmlsApi2 = pd.read_excel(localDir + 'logAfterUmlsApi2.xlsx')
'''

logAfterUmlsApi2 = pd.read_excel(localDir + 'logAfterUmlsApi1.xlsx')

# FIXME - Remove after this is fixed within the fixme above.
logAfterUmlsApi2 = logAfterUmlsApi2.sort_values(by='adjustedQueryCase', ascending=False)
logAfterUmlsApi2 = logAfterUmlsApi2.reset_index()
logAfterUmlsApi2.drop(['index'], axis=1, inplace=True)


# Join new UMLS API adds to the current search log master
logAfterUmlsApi2 = pd.merge(logAfterUmlsApi, newUmlsWithSemanticGroupData, how='left', on='adjustedQueryCase')

# Future: Look for a better way to do the above - MERGE WITH CONDITIONAL OVERWRITE. Temporary fix:
logAfterUmlsApi2['preferredTerm2'] = logAfterUmlsApi2['preferredTerm_x'].where(logAfterUmlsApi2['preferredTerm_x'].notnull(), logAfterUmlsApi2['preferredTerm_y'])
logAfterUmlsApi2['SemanticTypeName2'] = logAfterUmlsApi2['SemanticTypeName_x'].where(logAfterUmlsApi2['SemanticTypeName_x'].notnull(), logAfterUmlsApi2['SemanticTypeName_y'])
logAfterUmlsApi2['SemanticGroupCode2'] = logAfterUmlsApi2['SemanticGroupCode_x'].where(logAfterUmlsApi2['SemanticGroupCode_x'].notnull(), logAfterUmlsApi2['SemanticGroupCode_y'])
logAfterUmlsApi2['SemanticGroup2'] = logAfterUmlsApi2['SemanticGroup_x'].where(logAfterUmlsApi2['SemanticGroup_x'].notnull(), logAfterUmlsApi2['SemanticGroup_y'])
logAfterUmlsApi2['BranchPosition2'] = logAfterUmlsApi2['BranchPosition_x'].where(logAfterUmlsApi2['BranchPosition_x'].notnull(), logAfterUmlsApi2['BranchPosition_y'])
logAfterUmlsApi2['CustomTreeNumber2'] = logAfterUmlsApi2['CustomTreeNumber_x'].where(logAfterUmlsApi2['CustomTreeNumber_x'].notnull(), logAfterUmlsApi2['CustomTreeNumber_y'])
logAfterUmlsApi2.drop(['preferredTerm_x', 'preferredTerm_y',
                          'SemanticTypeName_x', 'SemanticTypeName_y',
                          'SemanticGroup_x', 'SemanticGroup_y',
                          'SemanticGroupCode_x', 'SemanticGroupCode_y',
                          'BranchPosition_x', 'BranchPosition_y', 
                          'CustomTreeNumber_x', 'CustomTreeNumber_y'], axis=1, inplace=True)
logAfterUmlsApi2.rename(columns={'preferredTerm2': 'preferredTerm',
                                    'SemanticTypeName2': 'SemanticTypeName',
                                    'SemanticGroup2': 'SemanticGroup',
                                    'SemanticGroupCode2': 'SemanticGroupCode',
                                    'BranchPosition2': 'BranchPosition',
                                    'CustomTreeNumber2': 'CustomTreeNumber'
                                    }, inplace=True)

# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'logAfterUmlsApi2.xlsx')
logAfterUmlsApi2.to_excel(writer,'logAfterUmlsApi2')
# df2.to_excel(writer,'Sheet2')
writer.save()



# -----------------------------------------------
# Create files to assign Semantic Types manually
# -----------------------------------------------
'''
If you want to add matches manually using two spreadsheet windows
To do in Python - cluster:
    - Probable person names
    - Probable NLM products, services, web pages
    - Probable journal names
'''

col = ['SemanticGroup', 'SemanticTypeName', 'Definition', 'Examples']
SemRef = SemanticNetworkReference[col]

# Get class distributions if you want to bolster under-represented sem types

currentSemTypeCount = GoldStandard['SemanticTypeName'].value_counts()
currentSemTypeCount = pd.DataFrame({'TypeCount':currentSemTypeCount})
currentSemTypeCount.sort_values("TypeCount", ascending=True, inplace=True)
currentSemTypeCount = currentSemTypeCount.reset_index()
currentSemTypeCount = currentSemTypeCount.rename(columns={'index': 'SemanticTypeName'})



# ------------------------------------
# Visualize results - logAfterUmlsApi2
# ------------------------------------
    
# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logAfterUmlsApi2)
unassigned = logAfterUmlsApi2['SemanticGroup'].isnull().sum()
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=True, startangle=100)
plt.axis('equal')
plt.title("Status after 'UMLS API 2' processing")
plt.show()

# Bar of SemanticGroup categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterUmlsApi2['SemanticGroup'].value_counts().plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Categories assigned after 'UMLS API 2' processing", fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top 
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)



#%%
# ===========================================================================
# 6. Create new 'uniques' dataframe/file for fuzzy matching
# ===========================================================================
'''
Re-start

logAfterUmlsApi1 = pd.read_excel(localDir + 'logAfterUmlsApi1.xlsx')

# Set a date range
AprMay = logAfterUmlsApi1[(logAfterUmlsApi1['Timestamp'] > '2018-04-01 01:00:00') & (logAfterUmlsApi1['Timestamp'] < '2018-06-01 00:00:00')]

logAfterUmlsApi2 = AprMay

# Restrict to NLM Home
searchfor = ['www.nlm.nih.gov$', 'www.nlm.nih.gov/$']
logAfterUmlsApi2 = logAfterUmlsApi2[logAfterUmlsApi2.Referrer.str.contains('|'.join(searchfor))]

# Set a date range
AprMay = logAfterUmlsApi1[(logAfterUmlsApi1['Timestamp'] > '2018-04-01 01:00:00') & (logAfterUmlsApi1['Timestamp'] < '2018-06-01 00:00:00')]

logAfterUmlsApi2 = AprMay

'''



listOfUniqueUnassignedAfterUmls2 = logAfterUmlsApi2[pd.isnull(logAfterUmlsApi2['preferredTerm'])]
listOfUniqueUnassignedAfterUmls2 = listOfUniqueUnassignedAfterUmls2.groupby('adjustedQueryCase').size()
listOfUniqueUnassignedAfterUmls2 = pd.DataFrame({'timesSearched':listOfUniqueUnassignedAfterUmls2})
listOfUniqueUnassignedAfterUmls2 = listOfUniqueUnassignedAfterUmls2.sort_values(by='timesSearched', ascending=False)
listOfUniqueUnassignedAfterUmls2 = listOfUniqueUnassignedAfterUmls2.reset_index()

writer = pd.ExcelWriter(localDir + 'unassignedToCheck2.xlsx')
listOfUniqueUnassignedAfterUmls2.to_excel(writer,'unassignedToCheck')
writer.save()
