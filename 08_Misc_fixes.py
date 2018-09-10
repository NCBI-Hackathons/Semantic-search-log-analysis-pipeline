
# coding: utf-8

# # Part 8. Misc fixes
# App to analyze web-site search logs (internal search)<br>
# **This script:** Re-usable code that doesn't belong anywhere in particular<br>
# Authors: dan.wendling@nih.gov, <br>
# Last modified: 2018-09-09
# 
# ## Script contents
# 
# 
# ## FIXMEs
# 
# Things Dan wrote for Dan; modify as needed. There are more FIXMEs in context.
# 
# * [ ] 
# 
# 
# Found this useful: https://stackoverflow.com/questions/tagged/matplotlib
# 
# ## 1. Start-up / What to put into place, where
# 

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import os

# Set working directory
os.chdir('/Users/wendlingd/Projects/webDS/_util')

localDir = '08_Misc_fixes/' # Different than others, see about changing


# In[ ]:


# 2. Load and clean logAfterUmlsApi1
# ===================================

logAfterUmlsApi1 = pd.read_excel('02_Run_APIs_files/logAfterUmlsApi1.xlsx')

logAfterUmlsApi1.loc[logAfterUmlsApi1['preferredTerm'].str.contains('^BLAST (physical force)', na=False), 'preferredTerm'] = 'Bibliographic Entity'


logAfterUmlsApi1['preferredTerm'] = logAfterUmlsApi1['preferredTerm'].str.replace("^BLAST \(physical force\)", "^BLAST$", regex=True)

logAfterUmlsApi1['preferredTerm'] = logAfterUmlsApi1['preferredTerm'].str.replace("BLAST Link", "BLAST", regex=False)

huh = logAfterUmlsApi1[logAfterUmlsApi1.adjustedQueryCase.str.startswith("blast") == True] # retrieve records to eyeball
huh = huh.groupby('preferredTerm').size()

logAfterUmlsApi1['preferredTerm'] = logAfterUmlsApi1['preferredTerm'].str.replace('Bibliographic Reference', 'Bibliographic Entity')

logAfterUmlsApi1['preferredTerm'] = logAfterUmlsApi1['preferredTerm'].str.replace('Mesh surgical material', 'MeSH')

# Write out the fixed file
writer = pd.ExcelWriter('02_Run_APIs_files/logAfterUmlsApi1.xlsx')
logAfterUmlsApi1.to_excel(writer,'logAfterUmlsApi1')
# df2.to_excel(writer,'Sheet2')
writer.save()


# In[ ]:


# VIEW PREVIOUS ASSIGNMENTS IN GoldStandard_master


from matplotlib.pyplot import pie, axis, show
import numpy as np
import os
import string


# Bring in historical file of (somewhat edited) matches
GoldStandard = localDir + 'GoldStandard_Master.xlsx'
GoldStandard = pd.read_excel(GoldStandard)

GoldStandard = GoldStandard[pd.notnull(GoldStandard['SemanticGroup'])]

'''
SELECT * FROM `manual_assignments` 
WHERE preferredTerm IS NULL
ORDER BY NewSemanticTypeName` DESC


preferredTerm, SemanticTypeName, SemanticGroup
'''

df2 = GoldStandard[GoldStandard.preferredTerm.str.contains("photo") == True]
df2 = GoldStandard[GoldStandard.SemanticTypeName.str.contains("foreign") == True]
df2 = GoldStandard[GoldStandard.SemanticGroup.str.contains("foreign") == True]




df = df.groupby('adjustedQueryCase').size()
df = pd.DataFrame({'timesSearched':df})


GoldStandard = GoldStandard.sort_values(by='timesSearched', ascending=False)
GoldStandard = GoldStandard.reset_index()


sum1 = logAfterUmlsApi1.groupby('SemanticTypeName').size()


# In[ ]:



# READ FROM SQL TO DATAFRAME


from sqlalchemy import create_engine

dbconn = create_engine('mysql+mysqlconnector://wendlingd:DataSciPwr17@localhost/ia')


# Extract from MySQL to df
mayJuneLog = pd.read_sql('SELECT * FROM timeboundhmpglog', con=dbconn)



# Write this to file (assuming multiple cycles)
writer = pd.ExcelWriter(localDir + 'mayJuneLog.xlsx')
mayJuneLog.to_excel(writer,'timeboundhmpglog')
writer.save()


# In[ ]:



# UPDATE SEMANTIC NETWORK table IN MYSQL
'''
DROP TABLE IF EXISTS `semantic_network`;
CREATE TABLE `semantic_network` (
    `semnet_id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `SemanticGroupCode`  int(11) NOT NULL,
    `SemanticGroup` varchar(60) NOT NULL,
    `SemanticGroupAbr` varchar(10) NOT NULL,
    `CustomTreeNumber`  int(11) NOT NULL,
    `SemanticTypeName` varchar(100) NOT NULL,
    `BranchPosition`  int(11) NOT NULL,
    `Definition` varchar(200) NOT NULL,
    `Examples` varchar(100) NOT NULL,
    `RelationName` varchar(60) NOT NULL,
    `SemTypeTreeNo` varchar(60) NOT NULL,
    `UsageNote` varchar(60) NOT NULL,
    `Abbreviation` varchar(60) NOT NULL,
    `UniqueID` int(11) NOT NULL,
    `NonHumanFlag` varchar(60) NOT NULL,
    `RecordType` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

SemanticNetworkReference = pd.read_excel('01_Text_wrangling_files/SemanticNetworkReference.xlsx')

SemanticNetworkReference.columns


# Add dataframe to MySQL

import mysql.connector
from pandas.io import sql
from sqlalchemy import create_engine

dbconn = create_engine('mysql+mysqlconnector://wendlingd:DataSciPwr17@localhost/ia')

SemanticNetworkReference.to_sql(name='semantic_network', con=dbconn, if_exists = 'replace', index=False) # or if_exists='append'

# Reduce to needed columns
listCol = SemanticNetworkReference[['SemanticGroupCode', 'SemanticGroup']]

listCol = listCol.drop_duplicates('SemanticGroup')


# In[ ]:


# RE-NAME categories

'''
SemanticGroup
    Citation, PubMed strategy, complex, unclear, etc.

logAfterFuzzyMatch

'''


logAfterFuzzyMatch['preferredTerm'] = logAfterFuzzyMatch['preferredTerm'].str.replace('Bibliographic Entity', 'PubMed strategy, citation, unclear, etc.')

logAfterFuzzyMatch.loc[logAfterFuzzyMatch['preferredTerm'].str.startswith('Bibliographic Entity', na=False), 'SemanticGroup'] = 'Unparsed'
logAfterFuzzyMatch.loc[logAfterFuzzyMatch['preferredTerm'].str.startswith('Bibliographic Entity', na=False), 'SemanticTypeName'] = 'Unparsed'


logAfterFuzzyMatch.loc[logAfterFuzzyMatch['preferredTerm'].str.contains('Numeric Entity', na=False), 'SemanticGroup'] = 'Accession Number'
logAfterFuzzyMatch.loc[logAfterFuzzyMatch['preferredTerm'].str.contains('Numeric Entity', na=False), 'SemanticTypeName'] = 'Accession Number'


writer = pd.ExcelWriter('03_Fuzzy_match_files/logAfterFuzzyMatch.xlsx')
logAfterFuzzyMatch.to_excel(writer,'logAfterFuzzyMatch')
# df2.to_excel(writer,'Sheet2')
writer.save()



logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^benefits of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^cause of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^cause for ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^causes for ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^causes of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^definition for ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^definition of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^effect of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^etiology of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^symptoms of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^treating ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^treatment for ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^treatments for ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^treatment of ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^what are ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^what causes ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^what is a ', '')
logAfterFuzzyMatch['adjustedQueryCase'] = logAfterFuzzyMatch['adjustedQueryCase'].str.replace('^what is ', '')


writer = pd.ExcelWriter('03_Fuzzy_match_files/logAfterFuzzyMatch.xlsx')
logAfterFuzzyMatch.to_excel(writer,'logAfterFuzzyMatch')
# df2.to_excel(writer,'Sheet2')
writer.save()


# In[ ]:



logAfterFuzzyMatch = logAfterFuzzyMatch.replace(np.nan, 'Unparsed', regex=True)

logAfterFuzzyMatch['preferredTerm'] = logAfterFuzzyMatch['preferredTerm'].str.replace('National Center for Biotechnology Information', 'NCBI')

logAfterFuzzyMatch['preferredTerm'] = logAfterFuzzyMatch['preferredTerm'].str.replace('Formatted References for Authors of Journal Articles', 'Refs for J Article Authors')

