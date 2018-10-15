#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 09:20:01 2018

@authors: dan.wendling@nih.gov, 

Last modified: 2018-10-15

** Site-search log file analyzer, Part 1 **

This script: Import search log, clean up, match query entries against historical files.


----------------
SCRIPT CONTENTS
----------------

1. Start-up / What to put into place, where
2. Unite search log data in single dataframe; globally update columns and rows
3. Show baseline stats for this dataset
4. Clean up content to improve matching
5. Separate out the queries with non-English characters
6. Make special-case assignments with F&R, RegEx: Bibliographic, Numeric, Named entities
7. Create logAfterGoldStandard - Match to the "gold standard" file of historical matches
8. Apply matches in HighConfidenceGuesses.xlsx
9. Create 'uniques' dataframe/file for APIs


-----------
INFLUENCES
-----------

- McCray AT, Burgun A, Bodenreider O. (2001). Aggregating UMLS semantic types
    for reducing conceptual complexity. Stud Health Technol Inform. 84(Pt 1):216-20.
    PMID: 11604736. http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4300099/
    See also https://semanticnetwork.nlm.nih.gov/
- Lai KH, Topaz M, Goss FR, Zhou L. (2015). Automated misspelling detection 
    and correction in clinical free-text records. J Biomed Inform. 
    Jun;55:188-95. doi: 10.1016/j.jbi.2015.04.008. Epub 2015 Apr 24. PMID: 
    25917057. https://www.ncbi.nlm.nih.gov/pubmed/25917057
"""


#%%
# ============================================
# 1. Start-up / What to put into place, where
# ============================================
'''
Search log from internal site search. This script assumes an Excel file
with these columns (okay to have more):

| Referrer | Query | Search Timestamp |

Referrer         - Where the visitor was when the search was submitted
Query            - The query content
Search Timestamp - When the query was run

I import Excel because my source breaks CSV rows in export when the query 
has commas.
'''


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import numpy as np
import os
import string

'''
Before running script, copy the following new files to /00 SourceFiles/; 
adjust names below, as needed.
'''

# Set working directory and directory to write files to
os.chdir('/Users/user/Projects/webDS/_util')
localDir = '01_Import-transform_files/'

# What is your new log file named?
newSearchLogFile = localDir + 'week35.xlsx'


#%%
# =================================================================================
# 2. Unite search log data into single dataframe; globally update columns and rows
# =================================================================================
'''
# If csv or tab delimited, for example: pd.read_csv(filename, sep='\t')
searchLog = pd.read_csv(newSearchLogFile)

# My system writes 65,000 rows in Excel and then creates a new worksheet...
x2 = pd.read_excel(newSearchLogFile, 'Page1_2', skiprows=2)
x3 = pd.read_excel(newSearchLogFile, 'Page1_3', skiprows=2)
x4 = pd.read_excel(newSearchLogFile, 'Page1_4', skiprows=2)
x5 = pd.read_excel(newSearchLogFile, 'Page1_5', skiprows=2)
x6 = pd.read_excel(newSearchLogFile, 'Page1_6', skiprows=2)
# x5 = pd.read_excel('00 SourceFiles/2018-06/Queries-2018-05.xlsx', 'Page1_2', skiprows=2)
searchLog = pd.concat([x1, x2, x3, x4, x5, x6], ignore_index=True) # , x3, x4, x5, x6, x7

searchLog.head(n=5)
searchLog.shape
searchLog.info()
searchLog.columns
'''

# Search log from Excel
searchLog = pd.read_excel(newSearchLogFile, skiprows=2)

searchLog = searchLog.rename(columns={'Search Timestamp': 'Timestamp'})

# Remove https:// to become joinable with traffic data
searchLog['Referrer'] = searchLog['Referrer'].str.replace('https://', '')

# Dupe off the Query column into a lower-cased 'adjustedQueryCase', which 
# will be the column you match against
searchLog['adjustedQueryCase'] = searchLog['Query'].str.lower()

# Remove incomplete rows, which can cause errors later
searchLog = searchLog[~pd.isnull(searchLog['Referrer'])]
searchLog = searchLog[~pd.isnull(searchLog['Query'])]


#%%
# ================================================================
# 3. Show baseline stats for this dataset
# ================================================================
'''
Before we start altering content.
'''
# Row count
TotQueries = len(searchLog)

# Sort and count terms with more than 10 searches, percent share
quickCounts = searchLog['Query'].value_counts()
quickCounts = pd.DataFrame({'Count':quickCounts})
quickCounts = quickCounts.reset_index()
quickCounts = quickCounts.head(n=100)
quickCounts['PercentShare'] = quickCounts.Count / TotQueries * 100

#Show
print("\n\nTotal queries: {}".format(TotQueries))
print("\nTop searches with percent share\n{}".format(quickCounts))


#%%
# ========================================
# 4. Clean up content to improve matching
# ========================================
'''
NOTE: Not limiting to a-zA-Z0-9 because future step is to look at what the
non-English character sets are.

When time allows, compare below to: 
    searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.extract('(\w+)', expand = False)
'''

# Remove punctuation...
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('"', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("'", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("`", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('(', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace(')', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('.', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace(',', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('!', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('#NAME?', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('*', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('$', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('+', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('?', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('!', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('#', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('%', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace(':', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace(';', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('{', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('}', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('|', '')
# Remove control characters
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('\^', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('\[', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('\]', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('\<', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('\>', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('\\', '')
# Remove high ascii etc.
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('•', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("“", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("”", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("‘", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("’", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("«", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("»", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("»", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("¿", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("®", "")
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace("™", "")

# searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('-', '')

# First-character issues
# searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^[0-9]{4}") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^-") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^/") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^@") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^;") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^<") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^>") == False] # char entities

# If removing punct caused a preceding space, remove the space.
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^  ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^ ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^ ', '')

# Drop junk rows with entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.startswith("&#") == False] # char entities
searchLog = searchLog[searchLog.adjustedQueryCase.str.contains("^&[0-9]{4}") == False] # char entities

# Remove modified entries that are now dupes or blank entries
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('  ', ' ') # two spaces to one
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.strip() # remove leading and trailing spaces
searchLog = searchLog.loc[(searchLog['adjustedQueryCase'] != "")]


# Test - Does the following do anything, good or bad? Can't tell. Remove non-ASCII; https://www.quora.com/How-do-I-remove-non-ASCII-characters-e-g-%C3%90%C2%B1%C2%A7%E2%80%A2-%C2%B5%C2%B4%E2%80%A1%C5%BD%C2%AE%C2%BA%C3%8F%C6%92%C2%B6%C2%B9-from-texts-in-Panda%E2%80%99s-DataFrame-columns
# I think a previous operation converted these already, for example, &#1583;&#1608;&#1588;&#1606;
# def remove_non_ascii(Query):
#    return ''.join(i for i in Query if ord(i)<128)
# testingOnly = uniqueSearchTerms['Query'] = uniqueSearchTerms['Query'].apply(remove_non_ascii)
# Also https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space?rq=1

# Remove starting text that can complicate matching
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^benefits of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^cause of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^cause for ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^causes for ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^causes of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^definition for ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^definition of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^effect of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^etiology of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^symptoms of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^treating ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^treatment for ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^treatments for ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^treatment of ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^what are ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^what causes ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^what is a ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^what is ', '')

# Should investigate how this happens? Does one browser not remove "search" from input?
# Examples: search ketamine, searchmedline, searchcareers, searchtuberculosis
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^search ', '')
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^search', '')

# Is this one different than the above? Such as, pathology of the lung
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('^pathology of ', '')

# Space clean-up as needed
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.replace('  ', ' ') # two spaces to one
searchLog['adjustedQueryCase'] = searchLog['adjustedQueryCase'].str.strip() # remove leading and trailing spaces
searchLog = searchLog.loc[(searchLog['adjustedQueryCase'] != "")]

searchLog.head()


#%%
# ========================================================
# 5. Separate out the queries with non-English characters
# ========================================================

"""
# *** COMMENTED OUT TO AVOID DAMAGING IN AUTO-RUN ***
# Manual work: Eyeball df and remove (some) foreign-language entries that 
# the APIs can't match - non-Roman characters, etc.

# Sort; non-Roman will sort to the top
foreignToTop = searchLog.sort_values(by='adjustedQueryCase', ascending=False)
foreignToTop = foreignToTop.reset_index()
foreignToTop.drop(['index'], axis=1, inplace=True)

# Eyeball foreignToTop then update to remove down to the rows the APIs will be able to parse
reviewForeign = foreignToTop[:288] 

# If you want someone to review the non-Roman entries
writer = pd.ExcelWriter(localDir + 'reviewForeign.xlsx')
reviewForeign.to_excel(writer,'showForeign')
# df2.to_excel(writer,'Sheet2')
writer.save()

# Remove foreign at top
nonForeign = foreignToTop[289:] 

# Eyeball nonForeign, up and down column, sorting by adjustedQueryCase;
# remove specific useless rows as needed
nonForeign.drop(28337, inplace=True)


# Start new df so you can revert if needed
searchLogClean = nonForeign

# Okay to remove foreignToTop, reviewForeign, nonForeign, searchLog
"""


#%%
# =========================================================================================
# 6. Make special-case assignments with F&R, RegEx: Bibliographic, Numeric, Named entities
# =========================================================================================
'''
Later procedures can't match the below very well.
'''

# --- pmresources.html; outlier in site; if you want special handling... ---
# searchLogClean.loc[searchLogClean['Referrer'].str.contains('/bsd/pmresources.html'), 'preferredTerm'] = 'pmresources.html'
# ToTestThis = searchLogClean[searchLogClean.Referrer.str.contains("/bsd/pmresources.html") == True]


# Add SemanticTypeName column
searchLogClean['SemanticTypeName'] = ""


# --- Bibliographic Entity ---
# Assign ALL queries over 20 char to 'Bibliographic Entity' (often citations, search strategies, pub titles...)
searchLogClean.loc[(searchLogClean['adjustedQueryCase'].str.len() > 20), 'preferredTerm'] = 'Bibliographic Entity'

# searchLogClean.loc[(searchLogClean['adjustedQueryCase'].str.len() > 25) & (~searchLogClean['preferredTerm'].str.contains('pmresources.html', na=False)), 'preferredTerm'] = 'Bibliographic Entity'

# Search strategies might also be in the form "clinical trial" and "phase 0"
searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('[a-z]{3,}" and "[a-z]{3,}', na=False), 'preferredTerm'] = 'Bibliographic Entity'

# Search strategies might also be in the form "clinical trial" and "phase 0"
searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('[a-z]{3,}" and "[a-z]{3,}', na=False), 'preferredTerm'] = 'Bibliographic Entity'

# Queries about specific journal titles
searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('^journal of', na=False), 'preferredTerm'] = 'Bibliographic Entity'
searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('^international journal of', na=False), 'preferredTerm'] = 'Bibliographic Entity'

# Add SemanticTypeName
searchLogClean.loc[searchLogClean['preferredTerm'].str.contains('Bibliographic Entity', na=False), 'SemanticTypeName'] = 'Bibliographic Entity' # 'Intellectual Product'


# --- Numeric Entity ---
# Assign entries starting with 3 digits
# FIXME - Clarify and grab the below, PMID, ISSN, ISBN 0-8016-5253-7), etc.
# searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('^[0-9]{3,}', na=False), 'preferredTerm'] = 'Numeric ID'
searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('[0-9]{5,}', na=False), 'preferredTerm'] = 'Numeric ID'
searchLogClean.loc[searchLogClean['adjustedQueryCase'].str.contains('[0-9]{4,}-[0-9]{4,}', na=False), 'preferredTerm'] = 'Numeric ID'

# Add SemanticTypeName
searchLogClean.loc[searchLogClean['preferredTerm'].str.contains('Numeric ID', na=False), 'SemanticTypeName'] = 'Numeric ID'

print("Assignments to preferredTerm\n{}".format(searchLogClean['preferredTerm'].value_counts()))

# Useful to write out the cleaned up version; if you do re-processing, you can skip a bunch of work.
writer = pd.ExcelWriter(localDir + 'searchLogClean.xlsx')
searchLogClean.to_excel(writer,'searchLogClean')
# df2.to_excel(writer,'Sheet2')
writer.save()


# -------------
# How we doin?
# -------------

TotQueries = len(searchLogClean)
Assigned = searchLogClean['preferredTerm'].notnull().sum()
Unassigned = searchLogClean['preferredTerm'].isnull().sum()
PercentUnassigned = (Unassigned / TotQueries) * 100

print("\nTotal queries in searchLogClean: {}".format(TotQueries))
print("\nPre-processing assignments:\n{}".format(searchLogClean['preferredTerm'].value_counts()))
print("\nAssigned: {}".format(Assigned))
print("Unassigned: {}".format(Unassigned))
print("\nPercent of queries to resolve: {}%".format(round(PercentUnassigned)))


#%%
# ===========================================================================================
# 7. Create logAfterGoldStandard - Match to the "gold standard" file of historical matches
# ===========================================================================================
'''
Attempt exact matches to previously assigned UMLS data. Over time this will 
lighten your overall workload significantly. You should edit the "Gold 
Standard" once in a while so it remains accurate. 
'''

# Bring in historical file
GoldStandard = pd.read_excel(localDir + 'GoldStandard_master.xlsx')

# FIXME - see notes below, problem here
logAfterGoldStandard = pd.merge(searchLogClean, GoldStandard, left_on='adjustedQueryCase', right_on='adjustedQueryCase', how='left')

logAfterGoldStandard.head()
logAfterGoldStandard.columns

# Future: Look for a better way to do the above - MERGE WITH CONDITIONAL OVERWRITE. Temporary fix:
logAfterGoldStandard['preferredTerm2'] = logAfterGoldStandard['preferredTerm_x'].where(logAfterGoldStandard['preferredTerm_x'].notnull(), logAfterGoldStandard['preferredTerm_y'])
logAfterGoldStandard['SemanticTypeName2'] = logAfterGoldStandard['SemanticTypeName_x'].where(logAfterGoldStandard['SemanticTypeName_x'].notnull())
logAfterGoldStandard['SemanticTypeName2'] = logAfterGoldStandard['SemanticTypeName_y'].where(logAfterGoldStandard['SemanticTypeName_y'].notnull())

logAfterGoldStandard.drop(['preferredTerm_x', 'preferredTerm_y', 'SemanticTypeName_x', 'SemanticTypeName_y'], axis=1, inplace=True)
logAfterGoldStandard.rename(columns={'preferredTerm2': 'preferredTerm',
                                     'SemanticTypeName2': 'SemanticTypeName'}, inplace=True)


#%%
# ===============================================
# 8. Apply matches in HighConfidenceGuesses.xlsx
# ===============================================
'''
This data comes from fuzzy matching later on; items in here can be proper names,
misspellings, foreign terms, that Python FuzzyWuzzy scored at 90% or higher - 
just a few characters off from what the UMLS API is able to match or what can
be read from the web site spidering that made it into the GoldStandard. You 
should edit this file a bit more frequently than you edit the GoldStandard 
file; these are automatically assigned.
'''

# Bring in historical file of lightly edited matches
HighConfidenceGuesses = pd.read_excel(localDir + 'HighConfidenceGuesses.xlsx')

logAfterGoldStandard = pd.merge(searchLogClean, GoldStandard, left_on='adjustedQueryCase', right_on='adjustedQueryCase', how='left')


logAfterGoldStandard.head(30)

# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'logAfterGoldStandard.xlsx')
logAfterGoldStandard.to_excel(writer,'logAfterGoldStandard')
# df2.to_excel(writer,'Sheet2')
writer.save()


# -----------------
# Visualize results
# -----------------

# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logAfterGoldStandard)
unassigned = logAfterGoldStandard['preferredTerm'].isnull().sum()
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=False, startangle=100)
plt.axis('equal')
plt.title("Status after 'GoldStandard' processing - \n{} queries with {} unassigned".format(totCount, unassigned))
plt.show()


'''
Top 20 SemanticTypeName assigned. Later this will be on SemanticGroup, but here, 
that has not been assigned yet.
'''


# Bar of SemanticTypeName categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterGoldStandard['SemanticTypeName'].value_counts()[:20].plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Top 20 semantic types assigned after 'GoldStandard' processing with {} of {} unassigned".format(unassigned, totCount), fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top 
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)

# Remove searchLogClean


#%%
# ===========================================================================================
# 9. Create 'uniques' dataframe/file for APIs
# ===========================================================================================
'''
Prepare a list of unique terms to process with API.

Re-starting?
logAfterGoldStandard = pd.read_excel(localDir + 'logAfterGoldStandard.xlsx')
'''

# Unique unassigned terms and frequency of occurrence
listOfUniqueUnassignedAfterGS = logAfterGoldStandard[pd.isnull(logAfterGoldStandard['preferredTerm'])] # was SemanticGroup
listOfUniqueUnassignedAfterGS = listOfUniqueUnassignedAfterGS.groupby('adjustedQueryCase').size()
listOfUniqueUnassignedAfterGS = pd.DataFrame({'timesSearched':listOfUniqueUnassignedAfterGS})
listOfUniqueUnassignedAfterGS = listOfUniqueUnassignedAfterGS.sort_values(by='timesSearched', ascending=False)
listOfUniqueUnassignedAfterGS = listOfUniqueUnassignedAfterGS.reset_index()


# ---------------------------------------------------------------
# Eyeball for fixes - Don't give the API things it can't resolve
# ---------------------------------------------------------------
'''
Act based on what the dataframes say; drop, modify, etc.
'''

# Save to file so you can open in future sessions
writer = pd.ExcelWriter(localDir + 'listOfUniqueUnassignedAfterGS.xlsx')
listOfUniqueUnassignedAfterGS.to_excel(writer,'listOfUniqueUnassignedAfterGS')
# df2.to_excel(writer,'Sheet2')
writer.save()

