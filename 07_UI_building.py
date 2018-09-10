
# coding: utf-8

# # Part 7. UI building
# App to analyze web-site search logs (internal search)<br>
# **This script:** Build UI information<br>
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

# In[ ]:


# 1. Start-up / What to put into place, where
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import numpy as np
import os

''' 100-percent content inventory from SEO Spider or other. Our allPages 
  dataframe is based on a 100-percent content inventory, so we 
  can analyze pages with zero traffic or zero searches. Also includes
  the page title, date the page was last updated - lots of rich info.
- Summary stats by communication package, from content inventory.'''
contentInventoryFileName = '00 SourceFiles/page.csv'
packageSummaryFileName = '00 SourceFiles/group.csv'

''' Traffic log. This script assumes Google Analytics unsampled report;  
references two column names: Page and Unique Pageviews. I export 
report header so I'll know later what is in the file, which means my 
import command skips the first ~6 rows.'''
newTrafficFileName = '00 SourceFiles/Pages_Q2.csv'

'''
The following custom dictionary files need to be in place in /01/Pre-process

GoldStandard.csv - Already-assigned term list, from UMLS and other sources, 
    vetted.
NamedEntities.csv - Known entities such as person names, product names, acronyms, 
    abbreviations, org parts, etc. Will overlap with GoldStandard; however, 
    UPDATE THIS FILE and this will replicate over to GoldStandard.
MisspelledOrForeign.csv - Short list of frequently misspelled words with HIGH
    confidence that they can be replaced without review. Okay to include
    foreign words.
'''


# ## 2. Plots

# In[ ]:


# Pie for percentage of rows assigned; https://pythonspot.com/matplotlib-pie-chart/
totCount = len(logWithGoldStandard)
unassigned = logWithGoldStandard['SemanticGroup'].isnull().sum()
assigned = totCount - unassigned
labels = ['Assigned', 'Unassigned']
sizes = [assigned, unassigned]
colors = ['lightskyblue', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.f%%', shadow=True, startangle=100)
plt.axis('equal')
plt.title("Status after 'GoldStandard' processing")
plt.show()


# Bar of SemanticGroup categories, horizontal
# Source: http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
ax = logWithGoldStandard['SemanticGroup'].value_counts().plot(kind='barh', figsize=(10,6),
                                                 color="slateblue", fontsize=10);
ax.set_alpha(0.8)
ax.set_title("Categories assigned after 'GoldStandard' processing", fontsize=14)
ax.set_xlabel("Number of searches", fontsize=9);
# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31,             str(round((i.get_width()), 2)), fontsize=9, color='dimgrey')
# invert for largest on top 
ax.invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)

