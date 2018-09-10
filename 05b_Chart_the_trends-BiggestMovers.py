
# coding: utf-8

# # 05b Chart the trends - "Biggest movers" May-June
# App to analyze web-site search logs (internal search)<br>
# **This script:** May-June analysis, fuller than the 05 file. Biggest Movers / Percent change charts<br>
# Authors: dan.wendling@nih.gov, <br>
# Last modified: 2018-09-09
# 
# 
# ## Script contents
# 
# 1. Start-up / What to put into place, where
# 2. Unite search log data into single dataframe; globally update columns and rows
# 3. Separate out the queries with non-English characters
# 4. Run STAFF stats
# 5. Run PUBLIC (off-LAN) stats
# 6. Add result to MySQL, process at http://localhost:5000/searchsum
# 
# 
# ## FIXMEs
# 
# Things Dan wrote for Dan; modify as needed. There are more FIXMEs in context.
# 
# * [ ] 

# In[ ]:


# 1. Start-up / What to put into place, where
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import numpy as np
import os
import string

# Set working directory
os.chdir('/Users/wendlingd/Projects/webDS/_util')

localDir = '05_Chart_the_trends_files/'


# In[ ]:


# 2. Unite search log data into single dataframe; globally update columns and rows
# =================================================================================
# What is your new log file named?

newSearchLogFile = '00_Source_files/FY18-q3.xlsx'

x1 = pd.read_excel(newSearchLogFile, 'Page1_1', skiprows=2)
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

# Drop ID column, not needed
# searchLog.drop(['ID'], axis=1, inplace=True)
            
# Until Cognos report is fixed, problem of blank columns, multi-word col name
# Update col name
searchLog = searchLog.rename(columns={'Search Timestamp': 'Timestamp', 
                                      'NLM IP Y/N':'StaffYN',
                                      'IP':'SessionID'})

# Remove https:// to become joinable with traffic data
searchLog['Referrer'] = searchLog['Referrer'].str.replace('https://', '')

# Dupe off the Query column into a lower-cased 'adjustedQueryCase', which 
# will be the column you match against
searchLog['adjustedQueryCase'] = searchLog['Query'].str.lower()

# Remove incomplete rows, which can cause errors later
searchLog = searchLog[~pd.isnull(searchLog['Referrer'])]
searchLog = searchLog[~pd.isnull(searchLog['Query'])]

# Limit to NLM Home
searchfor = ['www.nlm.nih.gov$', 'www.nlm.nih.gov/$']
HmPgLog = searchLog[searchLog.Referrer.str.contains('|'.join(searchfor))]

timeBoundHmPgLog = HmPgLog

# Limit to May and June and assign month name
timeBoundHmPgLog.loc[(timeBoundHmPgLog['Timestamp'] > '2018-05-01 00:00:00') & (timeBoundHmPgLog['Timestamp'] < '2018-06-01 00:00:00'), 'Month'] = 'May'
timeBoundHmPgLog.loc[(timeBoundHmPgLog['Timestamp'] > '2018-06-01 00:00:00') & (timeBoundHmPgLog['Timestamp'] < '2018-07-01 00:00:00'), 'Month'] = 'June'
timeBoundHmPgLog = timeBoundHmPgLog.loc[(timeBoundHmPgLog['Month'] != "")]
# or drop nan
timeBoundHmPgLog.dropna(subset=['Month'], inplace=True) 


# Useful to write out the cleaned up version; if you do re-processing, you can skip a bunch of work.
writer = pd.ExcelWriter(localDir + 'timeBoundHmPgLog.xlsx')
timeBoundHmPgLog.to_excel(writer,'timeBoundHmPgLog')
# df2.to_excel(writer,'Sheet2')
writer.save()

# Remove x1., etc., searchLog, HmPgLog


# In[ ]:


# 3. Separate out the queries with non-English characters
# ========================================================
'''
# FIXME - STOP THIS FROM CHANGING NORMAL ROWS.
See comment in function. Trying things from:
https://stackoverflow.com/questions/36340627/removing-non-ascii-characters-and-replacing-with-spaces-from-pandas-data-frame
https://stackoverflow.com/questions/27084617/detect-strings-with-non-english-characters-in-python
https://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
https://stackoverflow.com/questions/16353729/how-do-i-use-pandas-apply-function-to-multiple-columns
And other places

For testing
searchLogClean = pd.read_excel(localDir + 'searchLogClean.xlsx')
searchLogClean = searchLogClean.iloc[12000:13000]
searchLogClean['preferredTerm'] = searchLogClean['preferredTerm'].str.replace(None, '')

Future: Break out languages better; assign language name, find translation API, etc.

Re-start
MayJuneHmPg = pd.read_excel(localDir + 'searchLog-MayJune-HmPg.xlsx')
timeBoundHmPgLog = MayJuneHmPg
'''


# When it hangs... checkTrouble = searchLog.iloc[156422:156427]


timeBoundHmPgLog['preferredTerm'] = ""

def foreignCharTest(row):
    try: 
        row['Query'].encode('ascii'); 
        pass # Intention is, don't alter row at all; but returns None.
    except UnicodeEncodeError: 
        return 'NON-ENGLISH CHARACTERS'

timeBoundHmPgLog['preferredTerm'] = timeBoundHmPgLog.apply(foreignCharTest, axis=1)

# FIXME - Find a way to restore preferredTerm
# searchLog['preferredTerm'].replace('', np.nan, inplace=True)


# In[ ]:


# 4. Run STAFF stats
# ==============================
'''
On-LAN stats
FIXME - Check whether Cognos separation of Sfaff-YN can exclude reading room?
But, how many of the people in the reading room are on www.nlm.nih.gov at all?
'''
# Restrict to staff
staffStats = timeBoundHmPgLog.loc[timeBoundHmPgLog['StaffYN'].str.contains('Y') == True]

# Staff search count
totSearchesStaff = staffStats.groupby('Month')['ID'].nunique()
print("\nTotal STAFF SEARCHES in raw log file:\n{}".format(totSearchesStaff))

# Staff unique queries
uniqueSearchesStaff = staffStats['Query'].nunique()
uniqueSearchesStaff

uniqueSearchesStaffByMonth = staffStats.groupby('Month')['Query'].nunique()
uniqueSearchesStaffByMonth




# Staff session count
totSessionsStaff = staffStats.groupby('Month')['SessionID'].nunique()
print("\nTotal STAFF SESSIONS in raw log file:\n{}".format(totSessionsStaff))

'''
Bar chart - by number of searches per session

Average searches per session
Median searches per session
Average searches per day (@ 22d/mo.)
Median searches per day  (@ 22d/mo.)
Average sessions per day
Median sessions per day
Highest search count in one session

'''


# Top 40 queries from NLM LAN, from NLM Home (not normalized)
searchLogLanYesHmPg = staffStats.loc[staffStats['StaffYN'].str.contains('Y') == True]
searchfor = ['www.nlm.nih.gov$', 'www.nlm.nih.gov/$']
searchLogLanYesHmPg = searchLogLanYesHmPg[searchLogLanYesHmPg.Referrer.str.contains('|'.join(searchfor))]
searchLogLanYesHmPgQueryCounts = searchLogLanYesHmPg['Query'].value_counts()
searchLogLanYesHmPgQueryCounts = searchLogLanYesHmPgQueryCounts.reset_index()
searchLogLanYesHmPgQueryCounts = searchLogLanYesHmPgQueryCounts.rename(columns={'index': 'Top queries from NLM LAN, from Home, as entered', 'Query': 'Count'})
searchLogLanYesHmPgQueryCounts.head(n=25)


# In[ ]:


# 5. Run PUBLIC (off-LAN) stats
# ==============================


visitorStats = timeBoundHmPgLog.loc[timeBoundHmPgLog['StaffYN'].str.contains('N') == True]

# Count rows with foreign chars
foreignCount = visitorStats.loc[visitorStats['preferredTerm'].str.contains('NON-ENGLISH CHARACTERS') == True]
foreignCount.count()

# Drop rows with foreign chars
visitorStats = visitorStats[visitorStats.preferredTerm != 'NON-ENGLISH CHARACTERS']

# Visitor search count
totSearchesVisitors = visitorStats.groupby('Month')['ID'].nunique()
print("\nTotal VISITOR SEARCHES in raw log file:\n{}".format(totSearches))

# Visitor unique queries
uniqueSearchesVisitors = visitorStats['Query'].nunique()
uniqueSearchesVisitors

uniqueSearchesVisitorsByMonth = visitorStats.groupby('Month')['Query'].nunique()
uniqueSearchesVisitorsByMonth


# Visitor session count
totSessionsVisitors = visitorStats.groupby('Month')['SessionID'].nunique()
print("\nTotal VISITOR SESSIONS in raw log file:\n{}".format(totSessions))



'''
Bar chart - by number of searches per session

Average searches per session
Median searches per session
Average searches per day (@ 22d/mo.)
Median searches per day  (@ 22d/mo.)
Average sessions per day
Median sessions per day
Highest search count in one session

'''


# Highest session search count
SessionCounts = visitorStats['SessionID'].value_counts()
SessionCounts = pd.DataFrame({'TypeCount':SessionCounts})
SessionCounts.sort_values("TypeCount", ascending=True, inplace=True)
SessionCounts = SessionCounts.reset_index()

# test = searchLog.loc[searchLog['SessionID'].str.contains('47C9DEE89B48E22FB53E2BE2DB107763') == True]


# Top queries outside NLM LAN, from NLM Home (not normalized)
# May-June
df3LanNoHmPgQueryCounts = visitorStats['Query'].value_counts()
df3LanNoHmPgQueryCounts = df3LanNoHmPgQueryCounts.reset_index()
df3LanNoHmPgQueryCounts = df3LanNoHmPgQueryCounts.rename(columns={'index': 'Top queries off of LAN, from Home, as entered', 'Query': 'Count'})
df3LanNoHmPgQueryCounts.head(n=25)

# May top 25
MayVisitorTop25 = visitorStats.loc[visitorStats['Month'].str.contains('May') == True]
MayVisitorTop25 = MayVisitorTop25['Query'].value_counts()
MayVisitorTop25 = MayVisitorTop25.reset_index()
MayVisitorTop25 = MayVisitorTop25.rename(columns={'index': 'Top VISITOR queries from NLM Home page, as entered', 'Query': 'Count'})
MayVisitorTop25.head(n=25)

# June top 25
JuneVisitorTop25 = visitorStats.loc[visitorStats['Month'].str.contains('June') == True]
JuneVisitorTop25 = JuneVisitorTop25['Query'].value_counts()
JuneVisitorTop25 = JuneVisitorTop25.reset_index()
JuneVisitorTop25 = JuneVisitorTop25.rename(columns={'index': 'Top VISITOR queries from NLM Home page, as entered', 'Query': 'Count'})
JuneVisitorTop25.head(n=25)


# In[ ]:


# logAfterFuzzyMatch

EffectOfLight = logAfterFuzzyMatch.loc[logAfterFuzzyMatch['Query'].str.contains('effect of light') == True]

# Useful to write out the cleaned up version; if you do re-processing, you can skip a bunch of work.
writer = pd.ExcelWriter(localDir + 'EffectOfLight.xlsx')
EffectOfLight.to_excel(writer,'EffectOfLight')
# df2.to_excel(writer,'Sheet2')
writer.save()



dobby = logAfterFuzzyMatch.loc[logAfterFuzzyMatch['preferredTerm'].str.startswith('Samples of Formatted') == True]

# Samples of Formatted References for Authors of Journal Articles


# In[ ]:


# 6. Add result to MySQL, process at http://localhost:5000/searchsum
# ========================================================================
'''
timeBoundHmPgLog.columns

In phpMyAdmin:

DROP TABLE IF EXISTS `timeboundhmpglog`;
CREATE TABLE `timeboundhmpglog` (
  `Timestamp` datetime DEFAULT NULL,
  `preferredTerm` text,
  `SemanticTypeName` text,
  `SemanticTypeCode` int(11) DEFAULT NULL,
  `SemanticGroup` text,
  `SemanticGroupCode` int(11) DEFAULT NULL,
  `Month` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    
        
writer = pd.ExcelWriter(localDir + 'timeBoundHmPgLog.xlsx')
timeBoundHmPgLog.to_excel(writer,'timeBoundHmPgLog')
# df2.to_excel(writer,'Sheet2')
writer.save()


Re-start
MayJuneHmPg = pd.read_excel(localDir + 'searchLog-MayJune-HmPg.xlsx')
timeBoundHmPgLog = MayJuneHmPg
'''

logAfterFuzzyMatch = pd.read_excel('03_Fuzzy_match_files/logAfterFuzzyMatch.xlsx')

# Remove nans from Month
logAfterFuzzyMatch = logAfterFuzzyMatch.dropna(subset=['Month'])

logAfterFuzzyMatch.columns

# Reduce size for test
test = logAfterFuzzyMatch.iloc[0:49]


# Add dataframe to MySQL

import mysql.connector
from pandas.io import sql
from sqlalchemy import create_engine

dbconn = create_engine('mysql+mysqlconnector://wendlingd:DataSciPwr17@localhost/ia')

logAfterFuzzyMatch.to_sql(name='timeboundhmpglog', con=dbconn, if_exists = 'replace', index=False) # or if_exists='append'
   


# In[ ]:



'''

test = df3

df3.set_index('SessionID', inplace=True)
test = df3.groupby(['col2','col3'], as_index=False).count()



test = df3.groupby(['Month','StaffYN'], as_index=False)['SessionID'].count()
test

test = df3.groupby(['Month','StaffYN'], as_index=False)['SearchID'].count()
test


test = df3['ID'].groupby([df3['Month'], df3['StaffYN']]).size()
test


df3['SearchID'].count()

test = df3.groupby(['Month', 'StaffYN'])['Referrer'].size()
test

totSearches = df3.groupby(['Month', 'StaffYN'])['SearchID'].count()
print("\nTotal SEARCHES in raw log file:\n{}".format(totSearches))

totSessions = df3.groupby(['Month', 'StaffYN']).size()
print("\nTotal SESSIONS in raw log file:\n{}".format(totSessions))


# pd.crosstab(df3.ID, df3.SessionID, margins=True)


# df3 = df3.rename(columns={'ID': 'SearchID'})
'''



# Total SEARCHES in raw log file
totSearches = df3['SearchID'].groupby([df3['Month'], df3['StaffYN']]).count()
print("\nTotal SEARCHES in raw log file:\n{}".format(totSearches))

# Total SESSIONS in raw log file
totSessions = df3['SessionID'].groupby([df3['Month'], df3['StaffYN']]).count()
print("\nTotal SESSIONS in raw log file:\n{}".format(totSessions))



print("Total searches in raw log file: {}".format(len(df3)))

# totals
print("\nTotal SEARCH QUERIES, on NLM LAN or not\n{}".format(df3['StaffYN'].value_counts()))

print("\nTotal SESSIONS, on NLM LAN or not\n{}".format(df3.groupby('StaffYN')['SessionID'].nunique()))




test = df3['SearchID'].groupby(df3['Month'])
test.count()

# If you see digits in text col, perhaps these are partial log entries - eyeball for removal
# df3.drop(76080, inplace=True)


test = df3['StaffYN'].groupby(df3['Month'])
test.count()



# Total SEARCHES containing 'Non-English characters'
print("Total SEARCHES with non-English characters\n{}".format(df3['preferredTerm'].value_counts()))

# Total SESSIONS containing 'Non-English characters'
# Future




# How to set a date range
AprMay = logAfterUmlsApi1[(logAfterUmlsApi1['Timestamp'] > '2018-04-01 01:00:00') & (logAfterUmlsApi1['Timestamp'] < '2018-06-01 00:00:00')]





# Top queries from LAN (not normalized)
df3LanYes = df3.loc[df3['StaffYN'].str.contains('Y') == True]
df3LanYesQueryCounts = df3LanYes['Query'].value_counts()
df3LanYesQueryCounts = df3LanYesQueryCounts.reset_index()
df3LanYesQueryCounts = df3LanYesQueryCounts.rename(columns={'index': 'Top staff queries as entered', 'Query': 'Count'})
df3LanYesQueryCounts.head(n=30)

# Top queries from NLM LAN, from NLM Home (not normalized)
df3LanYesHmPg = df3.loc[df3['StaffYN'].str.contains('Y') == True]
searchfor = ['www.nlm.nih.gov$', 'www.nlm.nih.gov/$']
df3LanYesHmPg = df3LanYesHmPg[df3LanYesHmPg.Referrer.str.contains('|'.join(searchfor))]
df3LanYesHmPgQueryCounts = df3LanYesHmPg['Query'].value_counts()
df3LanYesHmPgQueryCounts = df3LanYesHmPgQueryCounts.reset_index()
df3LanYesHmPgQueryCounts = df3LanYesHmPgQueryCounts.rename(columns={'index': 'Top queries from NLM LAN, from Home, as entered', 'Query': 'Count'})
df3LanYesHmPgQueryCounts.head(n=25)


# Top queries outside NLM LAN (not normalized)
df3LanNo = df3.loc[df3['StaffYN'].str.contains('N') == True]
df3LanNoQueryCounts = df3LanNo['Query'].value_counts()
df3LanNoQueryCounts = df3LanNoQueryCounts.reset_index()
df3LanNoQueryCounts = df3LanNoQueryCounts.rename(columns={'index': 'Top queries off of LAN, as entered', 'Query': 'Count'})
df3LanNoQueryCounts.head(n=25)



# Top home page queries, staff or public
searchfor = ['www.nlm.nih.gov$', 'www.nlm.nih.gov/$']
df3AllHmPgQueryCounts = df3[df3.Referrer.str.contains('|'.join(searchfor))]
df3AllHmPgQueryCounts = df3AllHmPgQueryCounts['Query'].value_counts()
df3AllHmPgQueryCounts = df3AllHmPgQueryCounts.reset_index()
df3AllHmPgQueryCounts = df3AllHmPgQueryCounts.rename(columns={'index': 'Top home page queries, staff or public, as entered', 'Query': 'Count'})
df3AllHmPgQueryCounts.head(n=25)


# FIXME - Add table, Percentage of staff, public searches done within pages, within search results


# FIXME - Add table for Top queries with columns/counts On LAN, Off LAN, Total






# Remove the searches run from within search results screens, vsearch.nlm.nih.gov/vivisimo/
# I'm not looking at these now; you might be.
df3 = df3[df3.Referrer.str.startswith("www.nlm.nih.gov") == True]

# Not sure what these are, www.nlm.nih.gov/?_ga=2.95055260.1623044406.1513044719-1901803437.1513044719
df3 = df3[df3.Referrer.str.startswith("www.nlm.nih.gov/?_ga=") == False]


# FIXME - VARIABLE EXPLORER: After saving the stats, remove unneeded 'Type=DataFrame' items
'''
Remove manually for now.
Not finding an equiv to R's rm; cf https://stackoverflow.com/questions/32247643/how-to-delete-multiple-pandas-python-dataframes-from-memory-to-save-ram?rq=1
pd.x1(), pd.x2(), # pd.x3(), pd.x4(), pd.x5(), pd.x6(), pd.x7(), 
              pd.searchLogLanYes(), pd.searchLogLanYesHmPg(), 
              pd.searchLogLanNo(), pd.searchLogLanNoHmPg(),
              pd.searchLogAllHmPg()
'''

