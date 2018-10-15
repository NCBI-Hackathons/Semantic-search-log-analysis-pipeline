#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 10:44:31 2018

@authors: dan.wendling@nih.gov, 

Last modified: 2018-10-15

** Site-search log file analyzer, Part 3 **

CODE IS INCOMPLETE for the manual matching UI

This script: Automatically update "high-confidence guesses," then use 
Django UI to build the "training data" for machine learning by making
selections manually.

Matches such as proper names, acronyms, etc., will not be in UMLS, but 
can be fed into the 01 files over time. This step helps the system
get better over time; high-confidence corrections are automatic, but should
be checked occasionally, and lower-confidence matches need to be manually
inspected. Two Django pages and a sqlite database assist with this.

Python's FuzzyWuzzy was written for single inputs to a web form; I, however, 
am using it to compare one dataframe column to another dataframe's column. 
Takes a lot to match the tokenized function output back 
to the original untokenized term, which is necessary for this work.

Fuzzy match can be applied to an entire column of dataset_1 to return the 
best score against the column of dataset_2.

For more options see temp_FuzzyWuzzyHowTo.py.


----------------
SCRIPT CONTENTS
----------------

1. Start-up / What to put into place, where
2. FuzzyAutoAdd - When phrase-match score is 90 or higher, assign without checking
3. FuzzyWuzzyListToCheck - Set up manual matching UI
4. Add result to SQLite, process at http://localhost:5000/fuzzy/
   (Use browser to update SQLite table)
5. Bring data from manual_assignments back into Pandas
6. Update log and GoldStandard with new matches from MySQL
7. Create new 'uniques' dataframe/file for ML
8. Next steps
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
from fuzzywuzzy import fuzz, process

# Set working directory
os.chdir('/Users/user/Projects/webDS/_util')

localDir = '03_Fuzzy_match_files/'
dbDir = '_django/loganalysis/'

# Bring in historical file of (somewhat edited) matches
GoldStandard = pd.read_excel('01_Import-transform_files/GoldStandard_master.xlsx')


#%%
# ===========================================================
# 2. FuzzyAutoAdd - When phrase-match score is 90 or higher, 
#    assign without manual checking
# ===========================================================
'''
Isolate terms that might be a minor misspelling or might be a foreign version 
of the term. Some of these matches will be wrong, but overall, it's a good use 
of time to assign to what they look very similar to. Here we set the scorer to 
match whole terms/phrases, and the fuzzy matching score must be 90 or higher.

# Quick test, if you want - punctuation difference
fuzz.ratio('Testing FuzzyWuzzy', 'Testing FuzzyWuzzy!!')

FuzzyWuzzyResults - What the results of this function mean:
('hippocratic oath', 100, 2987)
('Best match string from dataset_2' (GoldStandard), 'Score of best match', 'Index of best match string in GoldStandard')

Re-start:
listOfUniqueUnassignedAfterUmls11 = pd.read_excel('02_Run_APIs_files/listOfUniqueUnassignedAfterUmls11.xlsx')
GoldStandard = pd.read_excel('01_Import-transform_files/GoldStandard_master.xlsx')

-----------
REFERENCES
-----------
- https://pypi.org/project/fuzzywuzzy/
- https://www.neudesic.com/blog/fuzzywuzzy-using-python/
- http://jonathansoma.com/lede/algorithms-2017/classes/fuzziness-matplotlib/fuzzing-matching-in-pandas-with-fuzzywuzzy/
'''

listOfUniqueUnassignedAfterUmls = pd.read_excel('02_Run_APIs_files/listOfUniqueUnassignedAfterUmls.xlsx')

fuzzySourceZ = listOfUniqueUnassignedAfterUmls

# Or,
# Recommendation: Test first
# fuzzySourceZ = listOfUniqueUnassignedAfterGS.iloc[0:25]

# 2018-07-08: Created FuzzyWuzzyProcResult1, 3,000 records, in 24 minutes
# 2018-07-09: 5,000 in 39 minutes
# 2018-07-09: 4,000 in 32 minutes
fuzzySourceZ = listOfUniqueUnassignedAfterUmls.iloc[0:500]

'''
fuzzySource1 = listOfUniqueUnassignedAfterGS.iloc[0:5000]
fuzzySource2 = listOfUniqueUnassignedAfterGS.iloc[5001:10678]
'''

def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(
        x, choices=choices, scorer=scorer, score_cutoff=cutoff
    )

# Create series FuzzyWuzzyResults
FuzzyAutoAdd1 = fuzzySourceZ.loc[:, 'adjustedQueryCase'].apply(
        fuzzy_match,
    args=( GoldStandard.loc[:, 'adjustedQueryCase'],
            fuzz.ratio, # also fuzz.token_set_ratio
            90
        )
)

# Convert FuzzyWuzzyResults Series to df
FuzzyAutoAdd2 = pd.DataFrame(FuzzyAutoAdd1)

# Move Index (IDs) into 'FuzzyIndex' col because Index values will be discarded
FuzzyAutoAdd2 = FuzzyAutoAdd2.reset_index()
FuzzyAutoAdd2 = FuzzyAutoAdd2.rename(columns={'index': 'FuzzyIndex'})

# Remove nulls
FuzzyAutoAdd2 = FuzzyAutoAdd2[FuzzyAutoAdd2.adjustedQueryCase.notnull() == True] # remove nulls

# Move tuple output into 3 cols
FuzzyAutoAdd2[['ProbablyMeantGSTerm', 'FuzzyScore', 'GoldStandardIndex']] = FuzzyAutoAdd2['adjustedQueryCase'].apply(pd.Series)
FuzzyAutoAdd2.drop(['adjustedQueryCase'], axis=1, inplace=True) # drop tuples

# Merge result to the orig source list cols
FuzzyAutoAdd3 = pd.merge(FuzzyAutoAdd2, fuzzySourceZ, how='left', left_index=True, right_index=True)
FuzzyAutoAdd3.columns
# 'FuzzyIndex', 'GSPrefTerm', 'FuzzyScore', 'GoldStandardIndex', 'adjustedQueryCase', 'timesSearched'
       
# Change col order for browsability if you want to analyze this by itself
FuzzyAutoAdd3 = FuzzyAutoAdd3[['adjustedQueryCase', 'ProbablyMeantGSTerm', 'FuzzyScore', 'timesSearched', 'FuzzyIndex', 'GoldStandardIndex']]

# Merge result to GoldStandard supplemental info
# Don't have a second person altering GoldStandard during your work...

FuzzyAutoAdd4 = pd.merge(FuzzyAutoAdd3, GoldStandard, how='left', left_on='ProbablyMeantGSTerm', right_on='adjustedQueryCase')
FuzzyAutoAdd4.columns
'''
Formerly used GoldStandardIndex, but GoldStandard can have multiple rows per item
and GoldStandardIndex was only getting one row.

'adjustedQueryCase_x', 'ProbablyMeantGSTerm', 'FuzzyScore',
       'timesSearched', 'FuzzyIndex', 'GoldStandardIndex', 'SemanticTypeName',
       'adjustedQueryCase_y', 'preferredTerm'
'''

# Reduce and rename
FuzzyAutoAdd4 = FuzzyAutoAdd4[['adjustedQueryCase_x', 'ProbablyMeantGSTerm', 'preferredTerm', 'SemanticTypeName']]
FuzzyAutoAdd4 = FuzzyAutoAdd4.rename(columns={'adjustedQueryCase_x': 'adjustedQueryCase'})


# --------------------------------------
# Add new entries to HighQualityGuesses
# --------------------------------------

# Open file from phase 1
HighQualityGuesses = pd.read_excel('01_Import-transform_files/HighConfidenceGuesses.xlsx')

# Append new data
HighQualityGuesses = HighQualityGuesses.append('FuzzyAutoAdd4', sort=True)

# Write out for future phase 1's
writer = pd.ExcelWriter('01_Import-transform_files/HighConfidenceGuesses.xlsx')
FuzzyAutoAdd4.to_excel(writer,'logAfterUmlsApi')
# df2.to_excel(writer,'Sheet2')
writer.save()


# --------------------------------------
# Add new entries to search log
# --------------------------------------

# Open file from phase 2
logAfterUmlsApi1 = pd.read_excel('02_Run_APIs_files/logAfterUmlsApi1.xlsx')

# Join new UMLS API adds to the current search log master
# This should update some rows and add some new rows for second/third semantic types
logAfterFuzzy1 = pd.merge(logAfterUmlsApi1, FuzzyAutoAdd4, how='left', on='adjustedQueryCase')

logAfterFuzzy1.columns
'''
'Referrer', 'Query', 'Timestamp', 'adjustedQueryCase',
       'preferredTerm_x', 'SemanticTypeName_x', 'ProbablyMeantGSTerm',
       'preferredTerm_y', 'SemanticTypeName_y'
'''

# Future: Look for a better way to do the above - MERGE WITH CONDITIONAL OVERWRITE. Temporary fix:
logAfterFuzzy1['preferredTerm2'] = logAfterFuzzy1['preferredTerm_x'].where(logAfterFuzzy1['preferredTerm_x'].notnull(), logAfterFuzzy1['preferredTerm_y'])
logAfterFuzzy1['SemanticTypeName2'] = logAfterFuzzy1['SemanticTypeName_x'].where(logAfterFuzzy1['SemanticTypeName_x'].notnull(), logAfterFuzzy1['SemanticTypeName_y'])
logAfterFuzzy1.drop(['preferredTerm_x', 'preferredTerm_y',
                          'SemanticTypeName_x', 'SemanticTypeName_y', 'ProbablyMeantGSTerm'], axis=1, inplace=True)
logAfterFuzzy1.rename(columns={'preferredTerm2': 'preferredTerm',
                                    'SemanticTypeName2': 'SemanticTypeName'}, inplace=True)


# Re-sort full file
logAfterFuzzy1 = logAfterFuzzy1.sort_values(by='adjustedQueryCase', ascending=True)
logAfterFuzzy1 = logAfterFuzzy1.reset_index()
logAfterFuzzy1.drop(['index'], axis=1, inplace=True)


# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'logAfterFuzzy1.xlsx')
logAfterFuzzy1.to_excel(writer,'logAfterFuzzy1')
# df2.to_excel(writer,'Sheet2')
writer.save()


# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'FuzzyAutoAdd.xlsx')
FuzzyAutoAdd4.to_excel(writer,'FuzzyAutoAdd')
# df2.to_excel(writer,'Sheet2')
writer.save()




# -----------------
# Visualize results
# -----------------
# logAfterFuzzy1 = pd.read_excel('03_Fuzzy_match_files/logAfterFuzzy1.xlsx')


# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logAfterFuzzy1)
unassigned = logAfterFuzzy1['preferredTerm'].isnull().sum()
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=False, startangle=100)
plt.axis('equal')
plt.title("Status after 'Fuzzy1' processing - \n{} queries with {} unassigned".format(totCount, unassigned))
plt.show()


'''
Top 20 SemanticTypeName assigned. Later this will be on SemanticGroup, but here, 
that has not been assigned yet.
'''


# Bar of SemanticTypeName categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterFuzzy1['SemanticTypeName'].value_counts()[:20].plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Top 20 semantic types assigned after 'Fuzzy1' processing \nwith {} of {} unassigned".format(unassigned, totCount), fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top 
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)


# Remove df's fuzzyAutoAdd1, etc., FuzzyWuzzyProcResult1, etc., fuzzySourceZ, etc., GoldStandard, others


#%%
# ==================================================================
# 3. FuzzyWuzzyListToCheck - Set up manual matching UI
# ==================================================================
'''
Now that the safe bets have been taken out, let's allow more liberal matching
and finish some assignments using human review.

Over time you can change the parameters to match your time and desired level
of effort. You can reduce the list, change the type of match (full phrase or 
any word), and change the score, to change the number of candidates to 
match how much time you want to spend in the browser. When starting with a
new site you should probably spend a good deal of time here, to make connections
the other steps can't make. Decisions you make here will provide training 
data that the machine learning component can use.

Some options described at https://www.neudesic.com/blog/fuzzywuzzy-using-python/.
See for example fuzz.ratio (conservative) vs. fuzz.partial_ratio (medium) vs.
fuzz.token_set_ratio (any single word in the phrases, very liberal). The more
liberal you get here, the more you will see multiple-concept searches, which
you don't need to see at this point. This is not a good time to solve those.

5,000 in ~25 minutes; ~10,000 in ~50 minutes (at score_cutoff=85)

# Quick test, if you want - punctuation difference
fuzz.ratio('Testing FuzzyWuzzy', 'Testing FuzzyWuzzy!!')

FuzzyWuzzyResults - What the results of this function mean:
('hippocratic oath', 100, 2987)
('Best match string from dataset_2' (GoldStandard), 'Score of best match', 'Index of best match string in GoldStandard')

Re-start:
logAfterFuzzy1 = pd.read_excel(localDir + 'listOfUniqueUnassignedAfterFuzzy1.xlsx')
'''

# Unique unassigned terms and frequency of occurrence
listOfUniqueUnassignedAfterFuzzy1 = logAfterFuzzy1[pd.isnull(logAfterFuzzy1['preferredTerm'])] # was SemanticGroup
listOfUniqueUnassignedAfterFuzzy1 = listOfUniqueUnassignedAfterFuzzy1.groupby('adjustedQueryCase').size()
listOfUniqueUnassignedAfterFuzzy1 = pd.DataFrame({'timesSearched':listOfUniqueUnassignedAfterFuzzy1})
listOfUniqueUnassignedAfterFuzzy1 = listOfUniqueUnassignedAfterFuzzy1.sort_values(by='timesSearched', ascending=False)
listOfUniqueUnassignedAfterFuzzy1 = listOfUniqueUnassignedAfterFuzzy1.reset_index()


fuzzySourceZ = listOfUniqueUnassignedAfterFuzzy1

# Recommendation: Do a test
# fuzzySourceZ = listOfUniqueUnassignedAfterFuzzy1.iloc[0:25]

# 2018-07-08: Created FuzzyWuzzyProcResult1, 3,000 records, in 24 minutes
# 2018-07-09: 5,000 in 39 minutes
# 2018-07-09: 4,000 in 32 minutes

'''
The list is sorted so more-frequent searches are near the top. These are more
likely to be real things, such as terms from web site pages. Items searched
only once or twice may not have enough information for classification. 
Real examples: accident room; achieve; advertise purch;


'''

# fuzzySourceZ = listOfUniqueUnassignedAfterFuzzy1.iloc[0:500]

'''
Large datasets, you may want to break up...
fuzzySource1 = listOfUniqueUnassignedAfterFuzzy1.iloc[0:5000]
fuzzySource2 = listOfUniqueUnassignedAfterFuzzy1.iloc[5001:10678]
'''

def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(
        x, choices=choices, scorer=scorer, score_cutoff=cutoff
    )

# Create series FuzzyWuzzyResults
FuzzyWuzzyProcResult1 = fuzzySourceZ.loc[:, 'adjustedQueryCase'].apply(
        fuzzy_match,
    args=( GoldStandard.loc[:, 'adjustedQueryCase'],
            fuzz.ratio,
            75 # Items must have this score or higher to appear in the results
        )
)


# Convert FuzzyWuzzyResults Series to df
FuzzyWuzzyProcResult2 = pd.DataFrame(FuzzyWuzzyProcResult1)

# Move Index (IDs) into 'FuzzyIndex' col because Index values will be discarded
FuzzyWuzzyProcResult2 = FuzzyWuzzyProcResult2.reset_index()
FuzzyWuzzyProcResult2 = FuzzyWuzzyProcResult2.rename(columns={'index': 'FuzzyIndex'})

# Remove nulls
FuzzyWuzzyProcResult2 = FuzzyWuzzyProcResult2[FuzzyWuzzyProcResult2.adjustedQueryCase.notnull() == True] # remove nulls

# Move tuple output into 3 cols
FuzzyWuzzyProcResult2[['ProbablyMeantGSTerm', 'FuzzyScore', 'GoldStandardIndex']] = FuzzyWuzzyProcResult2['adjustedQueryCase'].apply(pd.Series)
FuzzyWuzzyProcResult2.drop(['adjustedQueryCase'], axis=1, inplace=True) # drop tuples

# Merge result to the orig source list cols
FuzzyWuzzyProcResult3 = pd.merge(FuzzyWuzzyProcResult2, fuzzySourceZ, how='left', left_index=True, right_index=True)
FuzzyWuzzyProcResult3.columns
# 'FuzzyIndex', 'GSPrefTerm', 'FuzzyScore', 'GoldStandardIndex', 'adjustedQueryCase', 'timesSearched'
       
# Change col order for browsability if you want to analyze this by itself
FuzzyWuzzyProcResult3 = FuzzyWuzzyProcResult3[['adjustedQueryCase', 'ProbablyMeantGSTerm', 'FuzzyScore', 'timesSearched', 'FuzzyIndex', 'GoldStandardIndex']]

# Merge result to GoldStandard supplemental info
# Don't have a second person altering GoldStandard during your work...

FuzzyWuzzyProcResult4 = pd.merge(FuzzyWuzzyProcResult3, GoldStandard, how='left', left_on='ProbablyMeantGSTerm', right_on='adjustedQueryCase')
FuzzyWuzzyProcResult4.columns
'''
'adjustedQueryCase_x', 'ProbablyMeantGSTerm', 'FuzzyScore',
       'timesSearched', 'FuzzyIndex', 'GoldStandardIndex', 'SemanticTypeName',
       'adjustedQueryCase_y', 'preferredTerm'
'''

# Reduce and rename
FuzzyWuzzyProcResult4 = FuzzyWuzzyProcResult4[['adjustedQueryCase_x', 'preferredTerm', 'ProbablyMeantGSTerm', 'SemanticTypeName', 'timesSearched', 'FuzzyScore']]
FuzzyWuzzyProcResult4 = FuzzyWuzzyProcResult4.rename(columns={'adjustedQueryCase_x': 'adjustedQueryCase'})
# FYI adjustedQueryCase_y is now redundant; okay to drop

# Write to the folder containing sqlite database
writer = pd.ExcelWriter(dbDir + 'importManualAssignments.xlsx')
FuzzyWuzzyProcResult4.to_excel(writer,'manual')
# df2.to_excel(writer,'Sheet2')
writer.save()

# '_django/loganalysis/FuzzyWuzzyRawRecommendations.xlsx'

# Remove fuzzySource1, etc., FuzzyWuzzyProcResult1, etc.


#%%
# =================================================================
# 4. Add result to SQLite, process at http://localhost:5000/fuzzy/
# =================================================================
'''
https://docs.python.org/2/library/sqlite3.html

http://www.sqlitetutorial.net/sqlite-python/creating-database/

Database: /Users/user/Projects/webDS/_util/_django/loganalysis/db.sqlite3

CREATE TABLE "manual_assignments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "adjustedQueryCase" varchar(200) NULL, "NewSemanticTypeName" varchar(100) NULL, "preferredTerm" varchar(200) NULL, "FuzzyToken" varchar(50) NULL, "SemanticTypeName" varchar(100) NULL, "SemanticGroup" varchar(50) NULL, "timesSearched" integer NULL, "FuzzyScore" integer NULL, "Modified" integer NULL)

MySQL version was:
CREATE TABLE `manual_assignments` (
  `assignment_id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `adjustedQueryCase` varchar(200) NULL,
  `NewSemanticTypeName` varchar(100) NULL,
  `preferredTerm` varchar(200) NULL,
  `FuzzyToken` varchar(50) NULL,
  `SemanticTypeName` varchar(100) NULL,
  `SemanticGroup` varchar(50) NULL,
  `timesSearched` int(11) NULL,
  `FuzzyScore` int(11) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-----------
REFERENCES
-----------
- https://docs.python.org/2/library/sqlite3.html
- http://www.sqlitetutorial.net/sqlite-python/
    - http://www.sqlitetutorial.net/sqlite-python/creating-database/
    - http://www.sqlitetutorial.net/sqlite-replace-statement/
    - http://www.sqlitetutorial.net/sqlite-python/update/
- Python-SQLite code below, but DB Browser for SQLite was also used - http://sqlitebrowser.org/

Re-start?
FuzzyWuzzyProcResult4 = pd.read_excel('importManualAssignments.xlsx')

'''

# import pandas as pd
import sqlite3
from pandas.io import sql
from sqlite3 import Error
from pandas.io import sql
from sqlalchemy import create_engine
# import mysql.connector

# Set working directory
os.chdir('/Users/user/Projects/webDS/_util/_django/loganalysis')


# ----------------------------------------------------
# Get SQLite database going
# ----------------------------------------------------
'''
Recommendation: If you're using both DB Browser for SQLite and this at the 
same time, close DB Browser if you get "OperationalError: database is locked"
Or try using conn.close() here.
'''

# Open or re-open the database connection
conn = sqlite3.connect("db.sqlite3") # opens sqlite and a database file
myCursor = conn.cursor() # provides a connection to the database

# Test the connection
myCursor.execute("SELECT adjustedQueryCase, timesSearched FROM `manual_assignments` limit 10;", conn)
top10 = myCursor.fetchall()
print("\n\nTop 10 by timesSearched:\n {}".format(top10))

'''
CREATE statement from DB Browser from SQLite:
    CREATE TABLE "manual_assignments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "adjustedQueryCase" varchar(200) NULL, "NewSemanticTypeName" varchar(100) NULL, "preferredTerm" varchar(200) NULL, "FuzzyToken" varchar(50) NULL, "SemanticTypeName" varchar(100) NULL, "SemanticGroup" varchar(50) NULL, "timesSearched" integer NULL, "FuzzyScore" integer NULL, "Modified" integer NULL)
    
# To create a table from scratch; may not work.
http://www.sqlitetutorial.net/sqlite-create-table/
myCursor.execute("CREATE TABLE "manual_assignments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "adjustedQueryCase" varchar(200) NULL, "NewSemanticTypeName" varchar(100) NULL, "preferredTerm" varchar(200) NULL, "FuzzyToken" varchar(50) NULL, "SemanticTypeName" varchar(100) NULL, "SemanticGroup" varchar(50) NULL, "timesSearched" integer NULL, "FuzzyScore" integer NULL, "Modified" integer NULL)")
'''

FuzzyWuzzyProcResult4.columns
'''
'adjustedQueryCase', 'preferredTerm', 'ProbablyMeantGSTerm',
       'SemanticTypeName', 'timesSearched', 'FuzzyScore'
       ProbablyMeantGSTerm = FuzzyToken
'''

# FIXME - Problem with Django; fix there and remove this workaround
# FIXME - Reset index and name column assignment_id.;
FuzzyWuzzyProcResult4.rename(columns={'ProbablyMeantGSTerm': 'FuzzyToken'}, inplace=True)
FuzzyWuzzyProcResult4 = FuzzyWuzzyProcResult4.reset_index()
FuzzyWuzzyProcResult4.rename(columns={'index': 'id'}, inplace=True)


'''
FIXME - Ended up running these 3 commands in DB Browser for SQLite; something wrong.

DROP TABLE IF EXISTS manual_assignments;
VACUUM;
CREATE TABLE `manual_assignments` (`id` integer NOT NULL PRIMARY KEY AUTOINCREMENT, `adjustedQueryCase` TEXT, `preferredTerm` TEXT, `FuzzyToken` TEXT, `SemanticTypeName` TEXT, `timesSearched` INTEGER, `FuzzyScore` INTEGER, `NewSemanticTypeName` TEXT, `SemanticGroup` TEXT, `Modified` INTEGER);
'''

myCursor.execute("DROP TABLE IF EXISTS manual_assignments;")
conn.commit()

myCursor.execute("VACUUM;")
conn.commit()

myCursor.execute("CREATE TABLE `manual_assignments` (`id` integer NOT NULL PRIMARY KEY AUTOINCREMENT, `adjustedQueryCase` TEXT, `preferredTerm` TEXT, `FuzzyToken` TEXT, `SemanticTypeName` TEXT, `timesSearched` INTEGER, `FuzzyScore` INTEGER, `NewSemanticTypeName` TEXT, `SemanticGroup` TEXT, `Modified` INTEGER);")
conn.commit()


# ---------------------------------------------
# Move df FuzzyWuzzyProcResult4 df into SQLite
# ---------------------------------------------

# Add additional cols or SQLite will change schema
FuzzyWuzzyProcResult4['NewSemanticTypeName'] = ""
FuzzyWuzzyProcResult4['SemanticGroup'] = ""
FuzzyWuzzyProcResult4['Modified'] = ""

# Replace old data with new
FuzzyWuzzyProcResult4.to_sql("manual_assignments", conn, if_exists="replace")

# Did it work?
myCursor.execute("SELECT adjustedQueryCase, timesSearched FROM `manual_assignments` limit 10;")
top10 = myCursor.fetchall()
print("\n\nTop 10 by timesSearched:\n {}".format(top10))

'''
Alternatives...

myCursor.execute('SELECT adjustedQueryCase, timesSearched FROM `manual_assignments` limit 10;')
top10 = myCursor.fetchall()
print("\n\nTop 10 by timesSearched:\n {}".format(top10))


for arow in FuzzyWuzzyProcResult4:
    if arow[0].value == "code": continue
    theValues = (int(arow[0].value),arow[1].value)
    myCursor.execute("INSERT INTO 'accident_severity' VALUES (?,?) ",theValues)
'''


# To close the connection. I open and close this when switching between Python
# and DB Browser for SQLite.
conn.close()


#%%




# FIXME - the rest of the app requires work!






#%%
# ========================================================================
# 5. Bring data from manual_assignments back into Pandas
# ========================================================================
'''
Assign SemanticGroup from GoldStandard or other.

'''



#%%
# ========================================================================
# 6. Update log and GoldStandard with new matches from MySQL
# ========================================================================
'''
Move clean-up work into browser.

delete from manual_assignments
where NewSemanticTypeName like 'Ignore'

Re-start:
logAfterUmlsApi1 = pd.read_excel('02_Run_APIs_files/logAfterUmlsApi1.xlsx')
'''

logAfterUmlsApi1 = pd.read_excel('02_Run_APIs_files/logAfterUmlsApi1.xlsx')


# Apply to log file
logAfterFuzzyMatch = pd.merge(logAfterUmlsApi1, FuzAssigned2, how='left', on='adjustedQueryCase')

# Future: Look for a better way to do the above - MERGE WITH CONDITIONAL OVERWRITE. Temporary fix:
logAfterFuzzyMatch['preferredTerm2'] = logAfterFuzzyMatch['preferredTerm_x'].where(logAfterFuzzyMatch['preferredTerm_x'].notnull(), logAfterFuzzyMatch['preferredTerm_y'])
logAfterFuzzyMatch['SemanticTypeName2'] = logAfterFuzzyMatch['SemanticTypeName_x'].where(logAfterFuzzyMatch['SemanticTypeName_x'].notnull(), logAfterFuzzyMatch['SemanticTypeName_y'])
logAfterFuzzyMatch['SemanticGroupCode2'] = logAfterFuzzyMatch['SemanticGroupCode_x'].where(logAfterFuzzyMatch['SemanticGroupCode_x'].notnull(), logAfterFuzzyMatch['SemanticGroupCode_y'])
logAfterFuzzyMatch['SemanticGroup2'] = logAfterFuzzyMatch['SemanticGroup_x'].where(logAfterFuzzyMatch['SemanticGroup_x'].notnull(), logAfterFuzzyMatch['SemanticGroup_y'])
logAfterFuzzyMatch['BranchPosition2'] = logAfterFuzzyMatch['BranchPosition_x'].where(logAfterFuzzyMatch['BranchPosition_x'].notnull(), logAfterFuzzyMatch['BranchPosition_y'])
logAfterFuzzyMatch['CustomTreeNumber2'] = logAfterFuzzyMatch['CustomTreeNumber_x'].where(logAfterFuzzyMatch['CustomTreeNumber_x'].notnull(), logAfterFuzzyMatch['CustomTreeNumber_y'])
logAfterFuzzyMatch.drop(['preferredTerm_x', 'preferredTerm_y',
                          'SemanticTypeName_x', 'SemanticTypeName_y',
                          'SemanticGroup_x', 'SemanticGroup_y',
                          'SemanticGroupCode_x', 'SemanticGroupCode_y',
                          'BranchPosition_x', 'BranchPosition_y', 
                          'CustomTreeNumber_x', 'CustomTreeNumber_y'], axis=1, inplace=True)
logAfterFuzzyMatch.rename(columns={'preferredTerm2': 'preferredTerm',
                                    'SemanticTypeName2': 'SemanticTypeName',
                                    'SemanticGroup2': 'SemanticGroup',
                                    'SemanticGroupCode2': 'SemanticGroupCode',
                                    'BranchPosition2': 'BranchPosition',
                                    'CustomTreeNumber2': 'CustomTreeNumber'
                                    }, inplace=True)


# FIXME - Why are duplicate rows introduced?
logAfterFuzzyMatch = logAfterFuzzyMatch.drop_duplicates()


# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'logAfterFuzzyMatch.xlsx')
logAfterFuzzyMatch.to_excel(writer,'logAfterFuzzyMatch')
# df2.to_excel(writer,'Sheet2')
writer.save()



# ---------------------------------------
# Visualize results - logAfterFuzzyMatch
# ---------------------------------------
    
# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logAfterFuzzyMatch)
unassigned = logAfterFuzzyMatch['SemanticGroup'].isnull().sum()
# unassigned = logAfterFuzzyMatch.loc[logAfterFuzzyMatch['preferredTerm'].str.contains('Unparsed') == True]
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=False, startangle=100)
plt.axis('equal')
plt.title("Status after 'fuzzy match' processing - \n{} queries with {} unassigned".format(totCount, unassigned))
plt.show()


# Bar of SemanticGroup categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterFuzzyMatch['SemanticGroup'].value_counts().plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Categories assigned after 'fuzzy match' processing with {} of {} unassigned".format(unassigned, totCount), fontsize=14)
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
# =========================================================================
# 7. Create new 'uniques' dataframe/file for ML
# =========================================================================
'''
Won't require Excel file if you run the df from here. File will have 
updated entries from this session, by pulling back GoldStandard. Also will
make sure that previously found preferredTerm will be available as if they 
were queries. To get maximum utility from the API.

Training file: ApiAssignedSearches.xlsx (successful matches)
Unmatched terms we want to predict for: search-seed_the_ML.xlsx

GoldStandard = pd.read_excel('01_Import-transform_files/GoldStandard_master.xlsx')
'''


# Base on UPDATED (above) GoldStandard
ApiAssignedSearches = GoldStandard

col = ['adjustedQueryCase', 'preferredTerm', 'SemanticTypeName']
ApiAssignedSearches = ApiAssignedSearches[col]

'''
get all preferredTerm items, dupe this into adjustedQueryCase column (so both 
columns are the same, i.e, preferredTerm is also available as if it were 
raw input; append to df, de-dedupe rows.
'''

prefGrabber = ApiAssignedSearches.drop(['adjustedQueryCase'], axis=1) # drop col
prefGrabber.drop_duplicates(inplace=True) # de-dupe rows
prefGrabber['adjustedQueryCase'] = prefGrabber['preferredTerm'].str.lower()  # dupe and lc

ApiAssignedSearches = ApiAssignedSearches.append(prefGrabber, sort=True) # append to orig
ApiAssignedSearches.drop_duplicates(inplace=True) # de-dupe rows after append

# FIXME - Some adjustedQueryCase = nan
ApiAssignedSearches.adjustedQueryCase.fillna(ApiAssignedSearches.preferredTerm, inplace=True)
ApiAssignedSearches['adjustedQueryCase'].str.lower() # str.lower the nan fixes

# Write this to file
writer = pd.ExcelWriter(localDir + 'ApiAssignedSearches.xlsx')
ApiAssignedSearches.to_excel(writer,'ApiAssignedSearches')
writer.save()


# REMOVE
# Most variables but NOT ApiAssignedSearches
