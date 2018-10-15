#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:33:33 2018

@authors: dan.wendling@nih.gov, 

Last modified: 2018-10-15

** Site-search log file analyzer, Part 3 **

Purpose: Run unmatched search queries against UMLS API.

The first UMLS API run uses normalized string matching, which is conservative
enough to assume that almost all the matches are correct. Some clean-up will 
be needed, later.


----------------
SCRIPT CONTENTS
----------------

1. Start-up
2. Umls Api 1 - Normalized string matching
3. Isolate entries updated by API, complete tagging, and match to the
   new version of the search log - logAfterUmlsApi1
4. Append new API results to GoldStandard
5. Create logAfterUmlsApi1 by updating logAfterGoldStandard - append assignedByUmlsApi
6. Create new 'uniques' dataframe/file for fuzzy matching
7. Start new 'uniques' dataframe


----------
RESOURCES
----------

Register at UMLS, get a UMLS-UTS API key, and add it below. This is the
primary source for Semantic Type classifications.
- UMLS quick start: https://www.nlm.nih.gov/research/umls/quickstart.html
- https://www.nlm.nih.gov/research/umls/
- https://documentation.uts.nlm.nih.gov/rest/authentication.html
- https://documentation.uts.nlm.nih.gov/rest/home.html
- https://documentation.uts.nlm.nih.gov/rest/concept/
- UMLS description of what Normalized String option is,
https://uts.nlm.nih.gov/doc/devGuide/webservices/metaops/find/find2.html
"""


#%%
# ============================================
# 1. Start-up / What to put into place, where
# ============================================
'''
# Re-starting?
listOfUniqueUnassignedAfterGS = pd.read_excel('01_Import-transform_files/listOfUniqueUnassignedAfterGS.xlsx')
'''

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import requests
import json
import os
import lxml.html as lh
from lxml.html import fromstring
# import hunspell
# https://anaconda.org/conda-forge/hunspell
# hunspell doc: http://hunspell.github.io/
import numpy as np
# import time


# Set working directory
os.chdir('/Users/user/Projects/webDS/_util')

localDir = '02_Run_APIs_files/'


# Get local API key (after you have set it)
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


# UMLS Terminology Services (UTS): Generate a one-day Ticket-Granting-Ticket (TGT)
tgt = requests.post('https://utslogin.nlm.nih.gov/cas/v1/api-key', data = {'apikey':myUTSAPIkey})
# For API key get a license from https://www.nlm.nih.gov/research/umls/
# tgt.text
response = fromstring(tgt.text)
todaysTgt = response.xpath('//form/@action')[0]

uiUri = "https://uts-ws.nlm.nih.gov/rest/search/current?"
semUri = "https://uts-ws.nlm.nih.gov/rest/content/current/CUI/"



#%%
# ===========================================
# 2. Umls Api 1 - Normalized string matching
# ===========================================
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

# listToCheck1 = pd.read_excel(localDir + 'listToCheck1.xlsx')

# -------------------------------------------
# Batch rows if you want to do separate runs
# Arbitrary max of 5,000 rows per run...
# -------------------------------------------

# uniqueSearchTerms = search['adjustedQueryCase'].unique()

# Reduce entry length, to focus on single concepts that UTS API can match
# listOfUniqueUnassignedAfterGS = listOfUniqueUnassignedAfterGS.loc[(listOfUniqueUnassignedAfterGS['adjustedQueryCase'].str.len() <= 20) == True]

listToCheck1 = listOfUniqueUnassignedAfterGS

# listToCheck1 = unassignedAfterGS.iloc[0:20]
# listToCheck1 = listOfUniqueUnassignedAfterGS.iloc[0:10]
'''
listToCheck2 = listOfUniqueUnassignedAfterGS.iloc[6001:12000]
listToCheck3 = listOfUniqueUnassignedAfterGS.iloc[12001:18000]
'''


# If multiple sessions required, saving to file might help
writer = pd.ExcelWriter(localDir + 'listToCheck1.xlsx')
listToCheck1.to_excel(writer,'listToCheck1')
# df2.to_excel(writer,'Sheet2')
writer.save()

'''
writer = pd.ExcelWriter(localDir + 'apiGetNormalized1.xlsx')
apiGetNormalizedString.to_excel(writer,'listToCheck1')
# df2.to_excel(writer,'Sheet2')
writer.save()
'''


'''
OPTION - Bring in from file
listToCheck3 = pd.read_excel(localDir + 'listToCheck3.xlsx')
'''


#%%
# ----------------------------------------------------------
# Run this block after changing listToCheck top and bottom
# ----------------------------------------------------------

# Create df
apiGetNormalizedString = pd.DataFrame()
apiGetNormalizedString['adjustedQueryCase'] = ""
apiGetNormalizedString['preferredTerm'] = ""
apiGetNormalizedString['SemanticTypeName'] = list()


#%%

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


# OLD VERSION PLUS SUCCESSFUL CAPTURE OF MULTIPLE SemanticType ENTRIES

for index, row in listToCheck1.iterrows():
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
                                                       'SemanticTypeName': currSemTypes}), ignore_index=True)
        print('{} --> {}'.format(currLogTerm, currSemTypes)) # Write progress to console
        # time.sleep(.06)
    else:
       # Post "NONE" to database and restart loop
        apiGetNormalizedString = apiGetNormalizedString.append(pd.DataFrame({'adjustedQueryCase': currLogTerm, 'preferredTerm': "NONE"}, index=[0]), ignore_index=True)
        print('{} --> NONE'.format(currLogTerm, )) # Write progress to console
        # time.sleep(.06)
print ("* Done *")


writer = pd.ExcelWriter(localDir + 'apiGetNormalizedString3.xlsx')
apiGetNormalizedString.to_excel(writer,'apiGetNormalizedString')
# df2.to_excel(writer,'Sheet2')
writer.save()


#%%

# NEW VERSION

def getStuffFromAPI(currLogTerm): #Fetch from API
# === Get 'preferred term' and its concept identifier (CUI/UI) =========
    stTicket = requests.post(todaysTgt, data = {'service':'http://umlsks.nlm.nih.gov'}) # Get single-use Service Ticket (ST)
    # Example: GET https://uts-ws.nlm.nih.gov/rest/search/current?string=tylenol&sabs=MSH&ticket=ST-681163-bDfgQz5vKe2DJXvI4Snm-cas
    tQuery = {'string':currLogTerm, 'searchType':'normalizedString', 'ticket':stTicket.text} # removed 'sabs':'MSH',
    getPrefTerm = requests.get(uiUri, params=tQuery)
    getPrefTerm.encoding = 'utf-8'
    tItems  = json.loads(getPrefTerm.text)
    tJson = tItems["result"]
    return tJson

def getSemanticType(currUi): #Send Stuff to the API
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
    return currSemTypes

def postToDataFrame(currSemTypes, currPrefTerm, currLogTerm,apiGetNormalizedString):
 # === Post to dataframe =========
    apiGetNormalizedString = apiGetNormalizedString.append(pd.DataFrame({'adjustedQueryCase': currLogTerm,
                                               'preferredTerm': currPrefTerm,
                                               'SemanticTypeName': currSemTypes}), ignore_index=True)
    return apiGetNormalizedString


#initialize spellchecker
bj = hunspell.HunSpell('/home/ubuntu/umls/sortedvocab.txt.dic', '/home/ubuntu/umls/sortedvocab.txt.aff')
for index, row in listToCheck1.iterrows():
    currLogTerm = row['adjustedQueryCase']
    tJson = getStuffFromAPI(currLogTerm)
    if tJson["results"][0]["ui"] != "NONE": # Sub-loop to resolve "NONE"
        currUi = tJson["results"][0]["ui"]
        currPrefTerm = tJson["results"][0]["name"]
          
        currSemTypes = getSemanticType(currUi)
        # === Post to dataframe =========
        apiGetNormalizedString = postToDataFrame(currSemTypes, currPrefTerm, currLogTerm,apiGetNormalizedString)
        print('{} --> {}'.format(currLogTerm, currSemTypes)) # Write progress to console
        # time.sleep(.06)
    else:
        original = currLogTerm
        suggestion = bj.suggest(currLogTerm)
        if len(suggestion) > 0 and  (suggestion[0] != "["+original):
            currLogTerm = suggestion[0]
            tJson = getStuffFromAPI(currLogTerm)
            currUi = tJson["results"][0]["ui"]
            currPrefTerm = tJson["results"][0]["name"]

            currSemTypes = getSemanticType(currUi)
            # === Post to dataframe =========
            apiGetNormalizedString = postToDataFrame(currSemTypes, currPrefTerm, currLogTerm, apiGetNormalizedString)
            print('{}: {} --> {}'.format(original, currLogTerm, currSemTypes)) # Write progress to console
        else:
	    # Post "NONE" to database and restart loop
            apiGetNormalizedString = apiGetNormalizedString.append(pd.DataFrame({'adjustedQueryCase': currLogTerm, 'preferredTerm': "NONE"}, index=[0]), ignore_index=True)
            print('{} --> NONE'.format(currLogTerm, )) # Write progress to console
            # time.sleep(.06)
print ("* Done *")



writer = pd.ExcelWriter(localDir + 'apiGetNormalizedString1.xlsx')
apiGetNormalizedString.to_excel(writer,'apiGetNormalizedString')
# df2.to_excel(writer,'Sheet2')
writer.save()

# Free up memory: Remove listToCheck, listToCheck1, listToCheck2, listToCheck3,
# listToCheck4, nonForeign, searchLog, unassignedAfterGS


#%%
# ==================================================================
# 3. Combine multiple files if needed
# ==================================================================
'''
If you ran multiple runs and need to combine parts.

Re-starting? If using old version, the 'for' loop, use digit such asapiGetNormalizedString1
apiGetNormalizedString = pd.read_excel('02_Run_APIs_files/apiGetNormalizedString.xlsx')

apiGetNormalizedString = apiGetNormalizedString1
'''

"""
# Bring in stored info
newAssignments1 = pd.read_excel('02_Run_APIs_files/apiGetNormalizedString1.xlsx')
newAssignments2 = pd.read_excel('02_Run_APIs_files/apiGetNormalizedString2.xlsx')
newAssignments3 = pd.read_excel('02_Run_APIs_files/apiGetNormalizedString3.xlsx')

# Append
UmlsResult = newAssignments1.append([newAssignments2, newAssignments3]) # , sort=False
# afterUmlsApi = newAssignments1.append([newAssignments2, newAssignments3, newAssignments4, newAssignments5])
# Last run's data should be in a df already.


UmlsResult = newAssignments1.append([apiGetNormalizedString]) # , sort=False

Or if you only had one df:
UmlsResult = apiGetNormalizedString
"""


#%%
# ==========================================
# 4. Append new API results to GoldStandard
# ==========================================
'''
Improve future local matching and fuzzy matching.

# Open GoldStandard if needed
GoldStandard = pd.read_excel('01_Import-transform_files/GoldStandard_master.xlsx')

Re-start?
assignedByUmlsApi = pd.read_excel('02_Run_APIs_files/assignedByUmlsApi.xlsx')
'''




# Reduce to list of successful assignments
assignedByUmlsApi = UmlsResult.loc[(UmlsResult['preferredTerm'] != "NONE")]
assignedByUmlsApi = assignedByUmlsApi[~pd.isnull(assignedByUmlsApi['preferredTerm'])]
assignedByUmlsApi = assignedByUmlsApi.loc[(assignedByUmlsApi['preferredTerm'] != "Null Value")]
assignedByUmlsApi = assignedByUmlsApi[~pd.isnull(assignedByUmlsApi['adjustedQueryCase'])]

# Eyeball the df. If you need to remove rows...
# logAfterGoldStandard = logAfterGoldStandard.iloc[760:] # remove before index...


'''
# If you want to send to Excel
writer = pd.ExcelWriter(localDir + 'assignedByUmlsApi.xlsx')
assignedByUmlsApi.to_excel(writer,'assignedByUmlsApi')
# df2.to_excel(writer,'Sheet2')
writer.save()

assignedByUmlsApi = pd.read_excel('02_Run_APIs_files/assignedByUmlsApi.xlsx')
'''


GoldStandard = pd.read_excel('01_Import-transform_files/GoldStandard_master.xlsx')


# Append fully tagged UMLS API adds to GoldStandard
GoldStandard = GoldStandard.append(assignedByUmlsApi, sort=False)

# Sort, reset index
GoldStandard = GoldStandard.sort_values(by='adjustedQueryCase', ascending=True)
GoldStandard = GoldStandard.reset_index()
GoldStandard.drop(['index'], axis=1, inplace=True)

'''
Eyeball top and bottom of cols, remove rows by Index, if needed
GoldStandard.drop(58027, inplace=True)
'''

# Write out the updated GoldStandard
writer = pd.ExcelWriter('01_Import-transform_files/GoldStandard_master.xlsx')
GoldStandard.to_excel(writer,'GoldStandard')
writer.save()


#%%
# ============================================================================
# 5. Create logAfterUmlsApi1 by updating logAfterGoldStandard - append
# assignedByUmlsApi
# ============================================================================
'''
# Bring back in if needed
logAfterGoldStandard = pd.read_excel('01_Import-transform_files/logAfterGoldStandard.xlsx')
'''


# Join new UMLS API adds to the current search log master
logAfterUmlsApi1 = pd.merge(logAfterGoldStandard, assignedByUmlsApi, how='left', on='adjustedQueryCase')

logAfterUmlsApi1.columns
'''
'Referrer', 'Query', 'Timestamp', 'adjustedQueryCase',
       'preferredTerm_x', 'SemanticTypeName_x', 'SemanticTypeName_y',
       'preferredTerm_y'
'''

# Future: Look for a better way to do the above - MERGE WITH CONDITIONAL OVERWRITE. Temporary fix:
logAfterUmlsApi1['preferredTerm2'] = logAfterUmlsApi1['preferredTerm_x'].where(logAfterUmlsApi1['preferredTerm_x'].notnull(), logAfterUmlsApi1['preferredTerm_y'])
logAfterUmlsApi1['SemanticTypeName2'] = logAfterUmlsApi1['SemanticTypeName_x'].where(logAfterUmlsApi1['SemanticTypeName_x'].notnull(), logAfterUmlsApi1['SemanticTypeName_y'])
logAfterUmlsApi1.drop(['preferredTerm_x', 'preferredTerm_y',
                          'SemanticTypeName_x', 'SemanticTypeName_y'], axis=1, inplace=True)
logAfterUmlsApi1.rename(columns={'preferredTerm2': 'preferredTerm',
                                    'SemanticTypeName2': 'SemanticTypeName'}, inplace=True)


# Re-sort full file
logAfterUmlsApi1 = logAfterUmlsApi1.sort_values(by='adjustedQueryCase', ascending=True)
logAfterUmlsApi1 = logAfterUmlsApi1.reset_index()
logAfterUmlsApi1.drop(['index'], axis=1, inplace=True)

# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'logAfterUmlsApi1.xlsx')
logAfterUmlsApi1.to_excel(writer,'logAfterUmlsApi1')
# df2.to_excel(writer,'Sheet2')
writer.save()


# ------------------------------------
# Visualize results - logAfterUmlsApi1
# ------------------------------------

# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logAfterUmlsApi1)
unassigned = logAfterUmlsApi1['preferredTerm'].isnull().sum()
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=False, startangle=100)
plt.axis('equal')
plt.title("Status after 'UMLS API' processing - \n{} queries with {} unassigned".format(totCount, unassigned))
plt.show()


# Bar of SemanticTypeName categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterUmlsApi1['SemanticTypeName'].value_counts()[:20].plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Categories assigned after 'UMLS API' processing with {} of {} unassigned".format(unassigned, totCount), fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)


# Remove listOfUniqueUnassignedAfterGS, listToCheck1, etc., logAfterGoldStandard, logAfterUmlsApi11,
# newAssignments1 etc.


#%%
# ============================================================================
# 6. Start new 'uniques' dataframe that gets new column for each of the below
# listOfUniqueUnassignedAfterUmls1
# ============================================================================

# Unique queries with no assignments
listOfUniqueUnassignedAfterUmls = logAfterUmlsApi1[pd.isnull(logAfterUmlsApi1['preferredTerm'])]
listOfUniqueUnassignedAfterUmls = listOfUniqueUnassignedAfterUmls.groupby('adjustedQueryCase').size()
listOfUniqueUnassignedAfterUmls = pd.DataFrame({'timesSearched':listOfUniqueUnassignedAfterUmls})
listOfUniqueUnassignedAfterUmls = listOfUniqueUnassignedAfterUmls.sort_values(by='timesSearched', ascending=False)
listOfUniqueUnassignedAfterUmls = listOfUniqueUnassignedAfterUmls.reset_index()

# Send to file to preserve
writer = pd.ExcelWriter(localDir + 'listOfUniqueUnassignedAfterUmls.xlsx')
listOfUniqueUnassignedAfterUmls.to_excel(writer,'unassignedToCheck')

writer.save()
