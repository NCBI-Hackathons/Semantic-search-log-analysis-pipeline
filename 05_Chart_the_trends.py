
# coding: utf-8

# # Part 5. Chart the trends
# App to analyze web-site search logs (internal search)<br>
# **This script:** Biggest Movers / Percent change charts<br>
# Authors: dan.wendling@nih.gov, <br>
# Last modified: 2018-09-09
# 
# 
# ## Script contents
# 
# 1. Start-up / What to put into place, where
# 2. Load and clean a subset of data
# 3. Put stats into form that matplotlib can consume and export data
# 4. Biggest movers bar chart - Percent change in search frequency
# 
# 
# ## FIXMEs
# 
# Things Dan wrote for Dan; modify as needed. There are more FIXMEs in context.
# 
# * [ ] 
# 
# 
# ## RESOURCES
# 
# - Partly based on code from Mueller-Guido 2017, Visualize_coefficients, p 341.
# - https://stackoverflow.com/questions/tagged/matplotlib
# 

# In[ ]:


# 1. Start-up / What to put into place, where
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from matplotlib.colors import ListedColormap


# Set working directory
os.chdir('/Users/wendlingd/Projects/webDS/_util')

localDir = '05_Chart_the_trends_files/' # Different than others, see about changing


# In[ ]:


# 2. Load and clean a subset of data
# ===================================

logAfterFuzzyMatch = pd.read_excel('03_Fuzzy_match_files/logAfterFuzzyMatch.xlsx')

# Limit to off-LAN, NLM Home
df1 = logAfterFuzzyMatch.loc[logAfterFuzzyMatch['StaffYN'].str.contains('N') == True]
searchfor = ['www.nlm.nih.gov$', 'www.nlm.nih.gov/$']
df1 = df1[df1.Referrer.str.contains('|'.join(searchfor))]

'''
# If you want to remove unparsed
df1 = df1[df1.SemanticGroup.str.contains("Unparsed") == False]
df1 = df1[df1.preferredTerm.str.contains("PubMed strategy, citation, unclear, etc.") == False]
'''


# reduce cols
df2 = df1[['Timestamp', 'preferredTerm', 'SemanticTypeName', 'SemanticGroup']]

# Get nan count, remove nan rows
Unassigned = df2['preferredTerm'].isnull().sum()
df2 = df2[~pd.isnull(df2['Timestamp'])]
df2 = df2[~pd.isnull(df2['preferredTerm'])]
df2 = df2[~pd.isnull(df2['SemanticTypeName'])]
df2 = df2[~pd.isnull(df2['SemanticGroup'])]

# Limit to May and June and assign month name
df2.loc[(df2['Timestamp'] > '2018-05-01 00:00:00') & (df2['Timestamp'] < '2018-06-01 00:00:00'), 'Month'] = 'May'
df2.loc[(df2['Timestamp'] > '2018-06-01 00:00:00') & (df2['Timestamp'] < '2018-07-01 00:00:00'), 'Month'] = 'June'
df2 = df2.loc[(df2['Month'] != "")]




'''
--------------------------
IN CASE YOU COMPLETE CYCLE AND THEN SEE THAT LABELS SHOULD BE SHORTENED

# Shorten names if needed
df2['preferredTerm'] = df2['preferredTerm'].str.replace('National Center for Biotechnology Information', 'NCBI')
df2['preferredTerm'] = df2['preferredTerm'].str.replace('Samples of Formatted Refs J Articles', 'Formatted Refs Authors J Articles')
df2['preferredTerm'] = df2['preferredTerm'].str.replace('Formatted References for Authors of Journal Articles', 'Formatted Refs J Articles')

dobby = df2.loc[df2['preferredTerm'].str.contains('Formatted') == True]
dobby = df2.loc[df2['preferredTerm'].str.contains('Biotech') == True]

writer = pd.ExcelWriter('03_Fuzzy_match_files/logAfterFuzzyMatch.xlsx')
df2.to_excel(writer,'logAfterFuzzyMatch')
# df2.to_excel(writer,'Sheet2')
writer.save()
'''

writer = pd.ExcelWriter('03_Fuzzy_match_files/logAfterFuzzyMatch.xlsx')
df2.to_excel(writer,'logAfterFuzzyMatch')
# df2.to_excel(writer,'Sheet2')
writer.save()


# In[ ]:



# Count number of unique preferredTerm

# May counts
May = df2.loc[df2['Month'].str.contains('May') == True]
MayCounts = May.groupby('preferredTerm').size()
MayCounts = pd.DataFrame({'MayCount':MayCounts})
# MayCounts = MayCounts.sort_values(by='timesSearched', ascending=False)
MayCounts = MayCounts.reset_index()

# June counts
June = df2.loc[df2['Month'].str.contains('June') == True]
JuneCounts = June.groupby('preferredTerm').size()
JuneCounts = pd.DataFrame({'JuneCount':JuneCounts})
# JuneCounts = JuneCounts.sort_values(by='timesSearched', ascending=False)
JuneCounts = JuneCounts.reset_index()


# Remove rows with a count less than 10; next code would make some exponential.
MayCounts = MayCounts[MayCounts['MayCount'] >= 10]
JuneCounts = JuneCounts[JuneCounts['JuneCount'] >= 10]

# Join, removing terms not searched in BOTH months 
df3 = pd.merge(MayCounts, JuneCounts, how='inner', on='preferredTerm')

# Assign the percentage of that month's search share
# MayPercent
df3['MayPercent'] = ""
MayTotal = df3.MayCount.sum()
df3['MayPercent'] = df3.MayCount / MayTotal * 100

# JunePercent
df3['JunePercent'] = ""
JuneTotal = df3.JuneCount.sum()
df3['JunePercent'] = df3.JuneCount / JuneTotal * 100

# Assign Percent Change
df3['PercentChange'] = ""
df3['PercentChange'] = df3.JunePercent - df3.MayPercent

# Prep for next phase

PercentChangeData = df3


# In[ ]:


# 3. Put stats into form that matplotlib can consume and export data
# ===================================================================

PercentChangeData = PercentChangeData.sort_values(by='PercentChange', ascending=True)
PercentChangeData = PercentChangeData.reset_index()
PercentChangeData.drop(['index'], axis=1, inplace=True)          
     
negative_values = PercentChangeData.head(20)

positive_values = PercentChangeData.tail(20)
positive_values = positive_values.sort_values(by='PercentChange', ascending=True)
positive_values = positive_values.reset_index()
positive_values.drop(['index'], axis=1, inplace=True) 

interesting_values =  negative_values.append([positive_values])


# Write out full file and chart file

writer = pd.ExcelWriter(localDir + 'PercentChangeData.xlsx')
PercentChangeData.to_excel(writer,'PercentChangeData')
# df2.to_excel(writer,'Sheet2')
writer.save()

writer = pd.ExcelWriter(localDir + 'interesting_values.xlsx')
interesting_values.to_excel(writer,'interesting_values')
# df2.to_excel(writer,'Sheet2')
writer.save()


# In[ ]:


# 4. Biggest movers bar chart - Percent change in search frequency
# =================================================================
'''
Re-start:
interesting_values = pd.read_excel(localDir + 'interesting_values.xlsx')
'''


# Percent change chart
cm = ListedColormap(['#0000aa', '#ff2020'])
colors = [cm(1) if c < 0 else cm(0)
          for c in interesting_values.PercentChange]
ax = interesting_values.plot(x='preferredTerm', y='PercentChange',
                             kind='bar', 
                             color=colors,
                             fontsize=10) # figsize=(30, 10), 
ax.set_xlabel("preferredTerm")
ax.set_ylabel("Percent change for June")
ax.legend_.remove()
plt.axvline(x=19.4, linewidth=.5, color='gray')
plt.axvline(x=19.6, linewidth=.5, color='gray')
plt.subplots_adjust(bottom=0.4)
plt.ylabel("Percent change in search frequency")
plt.xlabel("Standardized topic name from UMLS+")
plt.xticks(rotation=60, ha="right", fontsize=9)
plt.suptitle('Biggest movers - How June site searches were different from the past', fontsize=16, fontweight='bold')
plt.title('NLM Home page, classify-able search terms only. In June use of the terms on the left\ndropped the most, and use of the terms on the right rose the most, compared to May.', fontsize=10)
plt.show()

# How June was different than May


# In[ ]:


# Outlier check
# =================================================================
'''
Why did Bibliographic Entity increase by 4%?
'''

huh = logAfterFuzzyMatch[logAfterFuzzyMatch.preferredTerm.str.startswith("Biblio") == True] # retrieve records to eyeball
# huh = huh.groupby('preferredTerm').size()

