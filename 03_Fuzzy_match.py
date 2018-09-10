
# coding: utf-8

# # Part 3. Fuzzy match
# App to analyze web-site search logs (internal search)<br>
# **This script:** For training ML algorithms: Post fuzzy match candidates to browser so user can select manually<br>
# Authors: dan.wendling@nih.gov, <br>
# Last modified: 2018-09-09
# 
# 
# ## Script contents
# 
# 1. Start-up / What to put into place, where
# 2. FuzzyWuzzyListToAdd - FuzzyWuzzy matching
# 3. Add result to MySQL, process at http://localhost:5000/fuzzy/
#    (Use browser to update MySQL table)
# 4. Bring data from manual_assignments back into Pandas
# 5. Update log and GoldStandard with new matches from MySQL
# 6. Create new 'uniques' dataframe/file for ML
# 7. Next steps
# 

# In[ ]:


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
os.chdir('/Users/wendlingd/Projects/webDS/_util')

localDir = '03_Fuzzy_match_files/'



# Bring in historical file of (somewhat edited) matches
GoldStandard = '01_Text_wrangling_files/GoldStandard_master.xlsx'
GoldStandard = pd.read_excel(GoldStandard)


# ## 2. FuzzyWuzzyListToAdd - FuzzyWuzzy matching
# 5,000 in ~25 minutes; ~10,000 in ~50 minutes (at score_cutoff=85)
# 
# Fuzzy match can be applied to an entire column of dataset_1 to return the 
# best score against the column of dataset_2. Here we set the scorer to 
# ‘token_set_ratio’ with score_cutoff of (originally) 90.
# 
# FuzzyWuzzy was written for single inputs to a web form; I, however, 
# am using it to compare one dataframe column to another dataframe's column,
# which outside https://www.neudesic.com/blog/fuzzywuzzy-using-python/ is 
# poorly documented. Takes a lot to match the tokenized function output back 
# to the original untokenized term, which is necessary for this work.
# 
# For more options see temp_FuzzyWuzzyHowTo.py
# 
# Browser page looks like: 
# 
# <img src="03_Fuzzy_match_files/fuzzyMatch-Browser.png" />
# 
# 
# # Quick test, if you want - punctuation difference
# fuzz.ratio('Testing FuzzyWuzzy', 'Testing FuzzyWuzzy!!')
# 
# FuzzyWuzzyResults - What the results of this function mean:
# ('hippocratic oath', 100, 2987)
# ('Best match string from dataset_2' (GoldStandard), 'Score of best match', 'Index of best match string in GoldStandard')
# 
# Re-start:
# listOfUniqueUnassignedAfterUmls11 = pd.read_excel('02_Run_APIs_files/listOfUniqueUnassignedAfterUmls11.xlsx')
# GoldStandard = pd.read_excel('01_Text_wrangling_files/GoldStandard_master.xlsx')

# In[ ]:


from fuzzywuzzy import fuzz, process

# Recommendation: Test first
# fuzzySourceZ = listOfUniqueUnassignedAfterGS.iloc[0:25]

# 2018-07-08: Created FuzzyWuzzyProcResult1, 3,000 records, in 24 minutes
# 2018-07-09: 5,000 in 39 minutes
# 2018-07-09: 4,000 in 32 minutes
fuzzySourceZ = listOfUniqueUnassignedAfterUmls2.iloc[0:4000]

'''
fuzzySource1 = listOfUniqueUnassignedAfterGS.iloc[0:5000]
fuzzySource2 = listOfUniqueUnassignedAfterGS.iloc[5001:10678]
'''

def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(
        x, choices=choices, scorer=scorer, score_cutoff=cutoff
    )

# Create series FuzzyWuzzyResults
FuzzyWuzzyProcResult1 = fuzzySourceZ.loc[:, 'adjustedQueryCase'].apply(
        fuzzy_match,
    args=( GoldStandard.loc[:, 'adjustedQueryCase'],
            fuzz.token_set_ratio,
            95
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
FuzzyWuzzyProcResult2[['FuzzyToken', 'FuzzyScore', 'GoldStandardIndex']] = FuzzyWuzzyProcResult2['adjustedQueryCase'].apply(pd.Series)
FuzzyWuzzyProcResult2.drop(['adjustedQueryCase'], axis=1, inplace=True) # drop tuples

# Merge result to the orig source list cols
FuzzyWuzzyProcResult3 = pd.merge(FuzzyWuzzyProcResult2, fuzzySourceZ, how='left', left_index=True, right_index=True)

# Change col order for browsability if you want to analyze this by itself
FuzzyWuzzyProcResult3 = FuzzyWuzzyProcResult3[['adjustedQueryCase', 'FuzzyToken', 'FuzzyScore', 'timesSearched', 'FuzzyIndex', 'GoldStandardIndex']]

# Merge result to GoldStandard supplemental info
# Don't have a second person altering GoldStandard during your work...
FuzzyWuzzyProcResult4 = pd.merge(FuzzyWuzzyProcResult3, GoldStandard, how='left', left_on='GoldStandardIndex', right_index=True)

# Reduce and rename
FuzzyWuzzyProcResult4 = FuzzyWuzzyProcResult4[['adjustedQueryCase_x', 'preferredTerm', 'FuzzyToken', 'SemanticTypeName', 'SemanticGroup', 'timesSearched', 'FuzzyScore']]
FuzzyWuzzyProcResult4 = FuzzyWuzzyProcResult4.rename(columns={'adjustedQueryCase_x': 'adjustedQueryCase'})

# Change name to be sensical inside other procedures
FuzzyWuzzyRawRecommendations = FuzzyWuzzyProcResult4


# Save to file so you can open in future sessions, if needed
writer = pd.ExcelWriter(localDir + 'FuzzyWuzzyRawRecommendations.xlsx')
FuzzyWuzzyRawRecommendations.to_excel(writer,'FuzzyWuzzyRawRecommendations')
# df2.to_excel(writer,'Sheet2')
writer.save()


# Future: chart for precent of total that were assigned something...

# Remove fuzzySource1, etc., FuzzyWuzzyProcResult1, FuzzyWuzzyProcResult2, etc.


# In[ ]:


# 3. Add result to MySQL, process at http://localhost:5000/fuzzy/
# ========================================================================

# Requires manual_assignments table, see 06_Load_database.

# Add dataframe to MySQL

import pandas as pd
import mysql.connector
from pandas.io import sql
from sqlalchemy import create_engine

dbconn = create_engine('mysql+mysqlconnector://wendlingd:pwd@localhost/ia')

FuzzyWuzzyRawRecommendations.to_sql(name='manual_assignments', con=dbconn, if_exists = 'replace', index=False) # or if_exists='append'
    

'''
From MySQL command line:
LOAD DATA LOCAL INFILE '/Users/wendlingd/Downloads/FuzzyWuzzyRawRecommendations.csv' INTO TABLE manual_assignments FIELDS TERMINATED BY ',' (adjustedQueryCase, preferredTerm, FuzzyToken, SemanticTypeName, SemanticGroup, timesSearched, FuzzyScore);

ALTER TABLE `manual_assignments` ADD `NewSemanticTypeName` VARCHAR(100) NULL AFTER `adjustedQueryCase`;

Re-start:
FuzzyWuzzyRawRecommendations = pd.read_excel(localDir + 'FuzzyWuzzyRawRecommendations')


select NewSemanticTypeName, count(*) as cnt
from manual_assignments
group by NewSemanticTypeName
order by cnt DESC;

select count(*) cnt
from manual_assignments
WHERE NewSemanticTypeName IS NOT NULL



FuzzyWuzzyRawRecommendations = pd.read_excel(localDir + 'FuzzyWuzzyRawRecommendations.xlsx')

FuzzyWuzzyRawRecommendations.to_csv(localDir + 'FuzzyWuzzyRawRecommendations.csv', index=False, header=None)

'''


# In[ ]:


'''
Resolve null column issues...
- No nulls
- Look right? Consistent, etc. 

Get SemanticTypeName for terms with new preferredTerm

SELECT preferredTerm, NewSemanticTypeName, SemanticGroup
FROM manual_assignments
WHERE NewSemanticTypeName IS NULL
ORDER BY preferredTerm


When NewSemanticTypeName is null

UPDATE manual_assignments
SET NewSemanticTypeName = SemanticTypeName
WHERE NewSemanticTypeName IS NULL


'''


# In[ ]:


# 4. Bring data from manual_assignments back into Pandas
# ========================================================================
'''
Assign SemanticGroup from GoldStandard or other.

'''


from sqlalchemy import create_engine

dbconn = create_engine('mysql+mysqlconnector://wendlingd:DataSciPwr17@localhost/ia')


# Extract from MySQL to df
FuzAssigned = pd.read_sql('SELECT adjustedQueryCase, preferredTerm, NewSemanticTypeName FROM manual_assignments WHERE NewSemanticTypeName IS NOT NULL AND NewSemanticTypeName NOT LIKE "Ignore"', con=dbconn)



# Write this to file (assuming multiple cycles)
writer = pd.ExcelWriter(localDir + 'FuzAssigned_BackFromMysql.xlsx')
FuzAssigned.to_excel(writer,'FuzAssigned')
writer.save()


# update SemanticGroup from GoldStandard_master

gsUnique = GoldStandard[['preferredTerm', 'SemanticTypeName', 'SemanticGroup', 'SemanticGroupCode', 'BranchPosition', 'CustomTreeNumber']]

gsUnique = gsUnique.drop_duplicates()
FuzAssigned2 = pd.merge(FuzAssigned, gsUnique, how='inner', on='preferredTerm')

# Not sure why NewSemanticTypeName and SemanticTypeName are the same.
FuzAssigned2.drop(['NewSemanticTypeName'], axis=1, inplace=True)

# Append to GoldStandard_master
GoldStandard = GoldStandard.append(FuzAssigned2, sort=True)

# Write new GoldStandard
writer = pd.ExcelWriter('01_Text_wrangling_files/GoldStandard_master.xlsx')
GoldStandard.to_excel(writer,'GoldStandard')
# df2.to_excel(writer,'Sheet2')
writer.save()


# In[ ]:


# 5. Update log and GoldStandard with new matches from MySQL
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
        autopct='%1.f%%', shadow=True, startangle=100)
plt.axis('equal')
plt.title("Status after 'fuzzy match' processing")
plt.show()


# Bar of SemanticGroup categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logAfterFuzzyMatch['SemanticGroup'].value_counts().plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Categories assigned after 'fuzzy match' processing", fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31,             str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top 
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)




'''
# Unite data, if there are multiple output files
f1 = pd.read_excel(localDir + 'FuzAssigned_Dan1.xlsx')
f2 = pd.read_excel(localDir + 'FuzAssigned_Dan2.xlsx')
f3 = pd.read_excel(localDir + 'FuzAssigned_Dan3.xlsx')

# Concat
fmAdd1 = pd.concat([f1, f2, f3], ignore_index=True, sort=True)

# drop SemanticTypeName (if present)
fmAdd1.drop(['SemanticTypeName'], axis=1, inplace=True)

# Rename SemanticTypeName
fmAdd1 = fmAdd1.rename(columns={'NewSemanticTypeName': 'SemanticTypeName'})


# De-dupe. Future? July run, need to eyeball before deleting
# fmAdd1.drop_duplicates(subset=['A', 'C'], keep=False)

searchLog.head(n=5)
searchLog.shape
searchLog.info()
searchLog.columns

# Remove f1, etc.
'''


# In[ ]:


# 5. Create new 'uniques' dataframe/file for ML
# =========================================================================
'''
Won't require Excel file if you run the df from here. File will have 
updated entries from this session, by pulling back GoldStandard. Also will
make sure that previously found preferredTerm will be available as if they 
were queries. To get maximum utility from the API.

Training file: ApiAssignedSearches.xlsx (successful matches)
Unmatched terms we want to predict for: search-seed_the_ML.xlsx

GoldStandard = pd.read_excel('01_Text_wrangling_files/GoldStandard_master.xlsx')
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


# In[ ]:


# 7. Next steps
# ==============
'''
Open 03_ML-classification.py, run the machine learning routines. You will use
these Excel files or dataframes

- ApiAssignedSearches
- unassignedAfterUmls1 or unassignedAfterUmls2

'''

