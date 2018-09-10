
# coding: utf-8

# # Part 4. Machine Learning Classification
# App to analyze web-site search logs (internal search)<br>
# **This script:** scikit-learn for site-search classifications<br>
# Authors: dan.wendling@nih.gov, <br>
# Last modified: 2018-09-09
# 
# 
# ## THIS SCRIPT (A WORK IN PROGRESS)
# 
# Some rough, not-quite in order, partly not-functioning machine learning 
# code that will eventually result in a dataframe of classification choices 
# for the ~30% of visitor search queries that the UMLS Metathesaurus is not 
# able to classify into broader categories (see 01_Pre-processing.py). 
# Some entries will be automatically assignable if misspellings can be 
# overcome with confidence.
# 
# Desired end result in the future (feature name / column name is first row):
# 
# | adjustedQueryCase  | preferredTerm                     | SemanticType       | SemanticGroup |
# | gallbladder cancer | Malignant neoplasm of gallbladder | Neoplastic Process | Disorders     |
# 
# 
# What this script is trying to generate currently:
#     
# | adjustedQueryCase  | UmlsApproximate | pred-LinearSVC   | pred-LogisticRegression | pred-NaiveBayesMultinomial |
# | cbd oil            | nan             | Organic Chemical | Intellectual Product    | Organic Chemical           |
# 
# (cbd oil is a marajuana-based product that many visitors seem to be 
# interested in. Variations on cbd will be avilable in the training set. 
# (An alternative to this work is clustering, but would it cluster correctly...)
# 
# 
# Feature/column explanations:
#     
# adjustedQueryCase - Lowercased version of query with most punctuation removed.
# preferredTerm - Can be assigned later if needed, but these are the UMLS system
#     picks from more than 200 medical vocabularies. 01_Pre-processing.py will 
#     assign when possible; this script does not use, as described below.
#     The UMLS system has 10s of thousands of these or more.
# SemanticType - Select one of 130 ontology categories. Eventually I will need
#     to select two or more of these categories for searches that look like 
#     "cancer exercise." For now I am okay capturing one category.
# SemanticGroup - One of 15 ontology super-categories.
# UmlsApproximate - A new run of the UMLS API that will be set to more liberal
# matching.
# pred-LinearSVC, etc. - Predictions from the various models. This can be used for eyeballing
# entries and adding manual assignments, to get the under-represented classes 
# some more content for future matching.
# 
# 
# ## Script contents
# 
# 1. Start-up / What to put into place, where; dataframe mods
# 2. Eyeball level of balance among classes under study, in training set
# 3. Training set: Calculate tf-idf vector for each query
# 4. Training set, Chi square: Find the terms most correlated with each item
# 5. Train, test, predict with a multi-class classifier, Naive Bayes-Multinomial
# 6. Model selection - Which among four models is the BEST model for this dataset?
# 
# Asperational, not working
# 7. Look deeper, with a confusion matrix, into the most successful model of
#    our group, LinearSVC (Linear Support Vector Classification)
# 8. Understand the misclassifications. Should we change the model, or not?
# 
# Somewhat working
# 9. Chi-square to find terms MOST CORRELATED with each category
# 10. TryLinearSVCdf - Unmatched terms with LinearSVC
# 11. TryLogisticRegressiondf - Unmatched terms with LogisticRegression
# 
# Not working
# 12. Final report by category
# 
# 
# ## FIXMEs
# 
# Things Dan wrote for Dan; modify as needed. There are more FIXMEs in context.
# 
# * [ ] 
# 
# - Biggest problem: I have under-represented classes such as for NLM
#   products, that we are building manually. See file search-seed_the_ML.xlsx - 
#   these are not matchable to the UMLS API as currently configured (it is 
#   configured for high-confidence matches). We're working now to improve 
#   category prediction for things not found in the UMLS datasets, such as 
#   misspellings, NLM products and services, partial NLM Web page titles 
#   (I scrape the site so I have a file of these, but they are verbose), 
#   historical names, commercial product names, etc. These will be added 
#   to the "GoldStandard" file. We started with the highest-frequency 
#   unmatched; hopefully ML can take over some or most of this. Clustering 
#   and FuzzyWuzzy will probably help here.
#   
# - Dan will add second and third runs for the UMLS API, as described in 
#   01_Pre-processing.py, to resolve non-English queries and provide a feature
#   (column) of UMLS API guesses, whose prediction scores were too low to 
#   return in the "normalized string" procedure I am using in the single 
#   current UMLS API run. Then an editor can perhaps choose among the UMLS, 
#   LinearSVC, LogisticRegression, etc., predictions.
#   
# - For the ML code below, I am trying to assign from the ~130 
#   *SemanticTypeName* categories (see file 01_Pre-processing_files/
#   SemanticNetworkReference.xlsx). I think using *SemanticTypeName* is 
#   best for the project; we could also try to match to the 15 
#   super-categories and then create more routines to match to the 130 
#   sub-categories.
#   
# - Add FuzzyWuzzy, perhaps fix misspellings in place (in col adjustedQueryCase).
#   If confidence is high that it will be the right fix...
# - Add stemming, lemmatization?
# - Future: Add the ability to assign one query to multiple categories.
# - More FIXMEs may appear in context below.
# 
# 
# ## INFLUENCES
# 
# - Susan Li, https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
#   (This code came from her code; I don't know what all of it does. Still has some of her info in comments)
# - Andreas Mueller, https://github.com/amueller/introduction_to_ml_with_python
#   (I am looking to add procedures from here that will assist in manual assign-
#   ments. Not sure what to add; LDA-based charts look useful.)
# 
# 

# ## 1. Start-up / What to put into place, where; dataframe mods
# 
# Training file: ApiAssignedSearches.xlsx (successful matches)
# Unmatched terms we want to predict for: search-seed_the_ML.xlsx
# 

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
import numpy as np
import os

# Set working directory
os.chdir('/Users/wendlingd/Projects/webDS/_util')


'''
Bring in and adjust training file, ApiAssignedSearches.xlsx - previous 
successful assignments; we will need adjustedQueryCase, preferredTerm, 
SemanticTypeName, SemanticGroup...
'''

df = pd.read_excel('02_UMLS_API_files/ApiAssignedSearches.xlsx')


# OR...
# df = ApiAssignedSearches


# Don't use preferredTerm for now - will be too inaccurate
df = df.drop(['preferredTerm'], axis=1) # drop col

# Don't try to process any non-Roman characters; eyeball and remove
# df = df[17:]

df.info()
# df.head()
# df.columns

# 6/23: Trouble with fit, so trying this - remove integer data type, perhaps
# Remove int values in adjustedQueryCase by removal or coerced data type change
df['adjustedQueryCase'] = df['adjustedQueryCase'].astype(str)


df = df.sort_values(by='adjustedQueryCase', ascending=True)
df = df.reset_index()
df.drop(['index'], axis=1, inplace=True)

'''
df.drop(12038, inplace=True)
df.drop(10714, inplace=True)
df.drop(6822, inplace=True)
'''
df.drop(26905, inplace=True)
df.drop(26904, inplace=True)
df.drop(26903, inplace=True)

'''
To preserve changes to training file for future sessions

# Useful to write out the cleaned up version; if you do re-processing, you can skip a bunch of work.
writer = pd.ExcelWriter('01_Pre-processing_files/ApiAssignedSearches.xlsx')
df.to_excel(writer,'ApiAssignedSearches')
# df2.to_excel(writer,'Sheet2')
writer.save()
'''

# add a column encoding the product as an integer, because categorical 
# variables are often better represented by integers than strings
df['category_id'] = df['SemanticTypeName'].factorize()[0]

# create a couple of dictionaries for future use
category_id_df = df[['SemanticTypeName', 
                     'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'SemanticTypeName']].values)

# what the first rows look like after the mods
df.head()

# Bring in entries to match
unassignedAfterUmls1 = pd.read_excel('02_UMLS_API_files/unassignedAfterUmls1.xlsx')
unassignedAfterUmls1 = unassignedAfterUmls1.drop(['timesSearched'], axis=1) # drop col


# In[ ]:



'''
*** I'M STUCK ON THIS ONE (FILE BELOW) ***

Not sure of your definition of fuzzy matching, but I use it to describe 
misspellings and also this - verbose product, service, etc. names.

Advice on how this should be implemented would be very useful!

People often look for words within web pages - librarians call this a 
"known item search," for a web page/product page/service page they are 
trying to get to. Many person names are in our biography pages. Product,
service names, etc. Multiple searches for "Kenneth Walker" - people
are probably trying to get to https://www.nlm.nih.gov/news/nlm_mourns_ken_walker.html,
or that's where we want them to get to. 

I use SEO Spider to scrape web page content, including page titles, in this 
case
they probably are trying to get to the page titled "NLM Mourns the Loss 
of H. Kenneth Walker, MD, MACP, FAAN, Former Chair of the National 
Library of Medicine Board of Regents."

Do I have to vectorize this whole title? How should the matches between
visitor search terms and verbose title pages, be implemented? Name 
extraction first?

I also have to do this with the list of 200+ named NLM products (mostly
databases such as pubmed.gov).
'''

# This data needs to be used to fuzzy match against web page names.
ShouldBeFuzzyMatched = pd.read_excel('03_ML-classification_files/ShouldBeFuzzyMatched.xlsx')

ShouldBeFuzzyMatched.head(n=10)

'''
ShouldBeFuzzyMatched is not used in this script; please suggest methods. 
For the above example I would like eventually to end up with:

| adjustedQueryCase | preferredTerm | SemanticType | SemanticGroup         |
| kenneth walker    | NLM News 2018 | NLM Web Page | Intellectual Products |


FYI, preferredTerm is not part of this script currrently, I am dropping 
that column above. But the value of preferredTerm would be 
ShouldBeFuzzyMatched['ContentGroup']) when a match is made to the page title.
Regarding SemanticType, to the original ontology of ~130 types I have added 
several NLM-specific type names such as "NLM Web Page." Not many in the
training set yet.
'''


# In[ ]:


# 2. Eyeball level of balance among classes under study, in training set
# Less than 1 minute
# =======================================================================
'''
Perhaps this should be used with item 12 below, Final report, after that
has been run.
'''

fig = plt.figure(figsize=(10,20))
df.groupby('SemanticTypeName').adjustedQueryCase.count().sort_index(ascending=False).plot.barh(ylim=0, fontsize=6, color="slateblue")
fig.subplots_adjust(left=0.3)
plt.title("Eyeball level of balance among classes", fontsize=12)
plt.xlabel("Number of queries")
plt.show()


'''
(Wow, lots of variation. Many under-represented classes.)
'''


# In[ ]:


# 3. Training set: Calculate tf-idf vector for each query
# Less than 1 minute
# ========================================================
'''
Current classifiers and learning algorithms can not directly process 
text in its original form; most of them expect numerical feature vectors 
with a fixed size, rather than raw text of variable length. Therefore, 
in this preprocessing step, comment text will be converted to a more manageable 
representation.

One common approach for extracting features from text is to use the 
"bag of words" model, where for each document, a complaint narrative 
in our case, the presence (and often the frequency) of words is taken 
into consideration, but the order in which they occur is ignored.

Specifically, for each term in our dataset, we will calculate a measure 
called Term Frequency, Inverse Document Frequency, abbreviated to tf-idf. 

We will use sklearn.feature_extraction.text.TfidfVectorizer to calculate 
a tf-idf vector for each of our consumer complaint narratives.

Cf. http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
'''

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(sublinear_tf=True, # True = Use a logarithmic form for frequency
                        min_df=5,   # minimum number of documents a word must be present in to be kept
                        norm='l2',  # to ensure all our feature vectors have a euclidian norm of 1
                        encoding='latin-1', 
                        ngram_range=(1, 2), # both unigrams and bigrams
                        stop_words='english') # remove common "noise" words, limit resulting features to useful ones

features = tfidf.fit_transform(df.adjustedQueryCase).toarray()
labels = df.category_id
features.shape


'''
Shape example, (29289, 75036)

Now, each of 29289 queries is represented by 75036 features, representing 
the tf-idf score for different unigrams and bigrams.
'''


# In[ ]:


# 4. Training set, Chi square: Find the terms most correlated with each item
# Less than 1 minute
# ===========================================================================
'''
We can use sklearn.feature_selection.chi2 to find the terms that are the 
most correlated with each of the products.

Cf. http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.chi2.html
'''

from sklearn.feature_selection import chi2

N = 2
for Product, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("# '{}':".format(Product))
  print("  . Most correlated unigrams:\n       . {}".format('\n       . '.join(unigrams[-N:])))
  print("  . Most correlated bigrams:\n       . {}".format('\n       . '.join(bigrams[-N:])))
  


# In[ ]:


# 5. Train, test, predict with a multi-class classifier, Naive Bayes-Multinomial
# Less than 1 minute
# ===============================================================================
'''
To train supervised classifiers, we first transformed the “Consumer 
complaint narrative” into a vector of numbers. We explored vector 
representations such as TF-IDF weighted vectors.

After having a vector representation of the text, we can train 
supervised-learning classifiers to train unseen “Consumer complaint narrative” 
entries and predict which of our products to assign them to.

Here we will vectorize with CountVectorizer and transform with TfidfTransformer.
'''

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

X_train, X_test, y_train, y_test = train_test_split(df['adjustedQueryCase'], df['SemanticTypeName'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


'''
Now that we have all the features and labels, we can start training the 
classifier. There are a number of algorithms that might be useful for the 
current dataset. Naive Bayes is a common go-to. The model most suitable 
for word counts is the multinomial variant.

Cf. http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html

'''

from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB().fit(X_train_tfidf, y_train)


# After fitting the training set, let’s try a few predictions.

# Tests
print(clf.predict(count_vect.transform(["herpes i"])))
print(clf.predict(count_vect.transform(["bemer"])))
print(clf.predict(count_vect.transform(["dental journals"])))
print(clf.predict(count_vect.transform(["intermittent fasting"])))
print(clf.predict(count_vect.transform(["cardiac tamponade pericardial lymphoma"])))
print(clf.predict(count_vect.transform(["fisioterapia"])))
print(clf.predict(count_vect.transform(["diabete"])))
print(clf.predict(count_vect.transform(["journal of clinical and diagnostic research"])))
print(clf.predict(count_vect.transform(["hippocrates"])))
print(clf.predict(count_vect.transform(["the new england journal of medicine"])))


# In[ ]:


# 6. Model selection - Which among four models is the BEST model for this dataset?
# ~1 minute
# REQUIRES AT LEAST 5 EXAMPLES PER CLASS
# =================================================================================
'''
Let's benchmark four models used for this type of dataset, evaluate their 
accuracy, and visualize their classification accuracy for our dataset.

1. (Multinomial) Naive Bayes, http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
2. Logistic Regression, http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
3. Linear Support Vector Classification, http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
4. Random Forest, http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
'''

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import cross_val_score

models = [
    MultinomialNB(),
    LogisticRegression(random_state=0),
    LinearSVC(),
    RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
]
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])


import seaborn as sns
# Cf. https://seaborn.pydata.org/generated/seaborn.boxplot.html

sns.boxplot(x='model_name', y='accuracy', data=cv_df).set_title("Classifier performance (box plot)")
sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
              size=8, jitter=True, edgecolor="gray", linewidth=2)
plt.show()

cv_df.groupby('model_name').accuracy.mean()


# In[ ]:


# 7. Look deeper, with a confusion matrix, into the most successful model of
# our group, LinearSVC (Linear Support Vector Classification)
# Less than 1 minute
# ========================================================================
'''
Too many categories to display. Future, could use SemanticGroup (only 15 classes)

Continuing with LinearSVC, the most-accurate model of the ones we tested, 
let's create a confusion matrix to show the discrepancies between predicted 
and actual labels within the categories.

Parameters: http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
'''

from sklearn.model_selection import train_test_split

model = LinearSVC()

X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(
        features, labels, df.index, test_size=0.33, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

from sklearn.metrics import confusion_matrix

conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.Product.values, 
            yticklabels=category_id_df.Product.values)
plt.rcParams.update({'font.size': 8})
plt.ylabel('Actual')
plt.subplots_adjust(left=0.5, bottom=0.5)
plt.xlabel('Predicted')
plt.show()

# Reduce long tag to see this as it was intended, with the Actual and 
# Predicted labels, 'Credit reporting, credit repair services, or other 
# personal consumer reports'.

'''
The vast majority of the predictions end up on the diagonal (predicted 
label = actual label), where we want them to be. 

However, there are a number of misclassifications, and it might be 
interesting to see what those are caused by.
'''


# In[ ]:


# 8. Understand the misclassifications. Should we change the model, or not?
# Less than 1 minute
# ==========================================================================
'''
From Susan Li's blog post, not working with this dataset.

Uses dictionary id_to_category.
'''

from IPython.display import display

for predicted in category_id_df.category_id:
  for actual in category_id_df.category_id:
    if predicted != actual and conf_mat[actual, predicted] >= 6:
      print("'{}' predicted as '{}' : {} examples.".format(
              id_to_category[actual], id_to_category[predicted], 
              conf_mat[actual, predicted]))
      display(df.loc[indices_test[(y_test == actual) & 
                                  (y_pred == predicted)]]
      [['SemanticTypeName', 'adjustedQueryCase']])
      print('')

'''
When things belong in multiple categories, errors will happen; not directly
fixable.
'''


# In[ ]:


# 9. Chi-square to find terms MOST CORRELATED with each category
# Less than 1 minute
# ========================================================================
'''
Again, we use the chi-squared test to find the terms that are the most 
correlated with each of the categories.

In IPython console:
    Start recording print output: %logstart dan1.txt
    Stop recording print output: %logstop

Or don't specifiy file name and then look for ipython_log.py
https://ipython.org/ipython-doc/3/interactive/reference.html
'''

model.fit(features, labels)

from sklearn.feature_selection import chi2

N = 3
stringCapture = ""
for Product, category_id in sorted(category_to_id.items()):
  indices = np.argsort(model.coef_[category_id])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in reversed(feature_names) if len(v.split(' ')) == 1][:N]
  bigrams = [v for v in reversed(feature_names) if len(v.split(' ')) == 2][:N]
  print("# '{}':".format(Product))
  print("  . Top unigrams:\n       . {}".format('\n       . '.join(unigrams)))
  print("  . Top bigrams:\n       . {}".format('\n       . '.join(bigrams)))
  stringCapture += '\n\n' + str(Product) + '\n Top unigrams:\n   ' + str(unigrams) + '\n Top bigrams:\n   ' + str(bigrams)


# In[ ]:


# 10. TryLinearSVCdf - Unmatched terms with LinearSVC
# Less than 1 minute
# ========================================================================

TryLinearSVCdf = pd.DataFrame()
TryLinearSVCdf['adjustedQueryCase'] = ""
TryLinearSVCdf['pred-LinearSVC'] = ""

TryLinearSVC = unassignedAfterUmls1['adjustedQueryCase'].astype(str)

text_features = tfidf.transform(TryLinearSVC)

predictions = model.predict(text_features)


for queryTerm, predicted in zip(TryLinearSVC, predictions):
    TryLinearSVCdf = TryLinearSVCdf.append(pd.DataFrame({'adjustedQueryCase': queryTerm, 
            'pred-LinearSVC': id_to_category[predicted]}, index=[0]), ignore_index=True, sort=True)

TryLinearSVCdf = TryLinearSVCdf[['adjustedQueryCase', 'pred-LinearSVC']]


# In[ ]:


# 11. TryLogisticRegressiondf - Unmatched terms with LogisticRegression
# Less than 1 minute
# ========================================================================
'''
https://towardsdatascience.com/logistic-regression-using-python-sklearn-numpy-mnist-handwriting-recognition-matplotlib-a6b31e2b166a
'''

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

logisticRegr = LogisticRegression(random_state=0)

logisticRegr.fit(X_train, y_train)

predictions = logisticRegr.predict(X_train)

'''
# Use score method to get accuracy of model
score = logisticRegr.score(x_test, y_test)
print(score)
'''

TryLogisticRegressionDf = pd.DataFrame()
TryLogisticRegressionDf['adjustedQueryCase'] = ""
TryLogisticRegressionDf['pred-LogisticReg'] = ""

TryLogisticRegression = unassignedAfterUmls1['adjustedQueryCase'].astype(str)

text_features = tfidf.transform(TryLogisticRegression)

for queryTerm, predicted in zip(TryLogisticRegression, predictions):
    TryLogisticRegressionDf = TryLogisticRegressionDf.append(pd.DataFrame({'adjustedQueryCase': queryTerm, 
            'pred-LogisticReg': id_to_category[predicted]}, index=[0]), ignore_index=True, sort=True)

TryLogisticRegressionDf = TryLogisticRegressionDf[['adjustedQueryCase', 'pred-LogisticReg']]


# In[ ]:


# JOIN NEW DATAFRAMES

twoGuesses = pd.merge(TryLinearSVCdf, TryLogisticRegressionDf)

writer = pd.ExcelWriter('01_Pre-processing_files/twoGuesses.xlsx')
twoGuesses.to_excel(writer,'twoGuesses')
# df2.to_excel(writer,'Sheet2')
writer.save()


# In[ ]:


# 12. Final report by category
# Less than 1 minute
# ========================================================================
'''
Classes where more training data is needed, or other changes need to be
made.
'''
  
from sklearn import metrics

print(metrics.classification_report(y_test, y_pred, 
                                    target_names=df['SemanticTypeName'].unique()))


'''

                                         precision    recall  f1-score   support

                 NLM Product or Service       0.66      0.48      0.55       299
                   Quantitative Concept       0.31      0.22      0.26        78
Nucleic Acid, Nucleoside, or Nucleotide       0.40      0.14      0.21        57
    Therapeutic or Preventive Procedure       0.66      0.47      0.55       383
                                  Plant       0.53      0.12      0.19       178
                       Organic Chemical       0.26      0.94      0.41      1212
                   Intellectual Product       0.50      0.29      0.36       270
        Amino Acid, Peptide, or Protein       0.68      0.24      0.35       409
                         Cell Component       0.65      0.36      0.46        36
                Pharmacologic Substance       0.29      0.15      0.20       143
  Indicator, Reagent, or Diagnostic Aid       0.20      0.08      0.12        12
                       Temporal Concept       0.36      0.20      0.26        45
                    Nucleotide Sequence       0.00      0.00      0.00         3
                   Laboratory Procedure       0.57      0.54      0.55        98
   Body Part, Organ, or Organ Component       0.55      0.39      0.45       199
                                Finding       0.40      0.26      0.32       334
                    Disease or Syndrome       0.68      0.51      0.58      1040
                        Spatial Concept       0.20      0.02      0.04        43
                    Manufactured Object       0.28      0.11      0.16        91
                                   Cell       0.66      0.61      0.64        44
                         Gene or Genome       0.95      0.54      0.69       448
                                Vitamin       0.00      0.00      0.00         4
                     Immunologic Factor       0.78      0.34      0.47       116
          Cell or Molecular Dysfunction       0.40      0.14      0.21        14
                   Diagnostic Procedure       0.62      0.41      0.50       104
                     Molecular Function       0.47      0.24      0.32        29
                            semTypeName       0.77      0.66      0.71       176
                     Neoplastic Process       0.00      0.00      0.00         5
       Self-help or Relief Organization       0.20      0.16      0.18        19
                Body Location or Region       0.58      0.37      0.45       119
                        Sign or Symptom       0.00      0.00      0.00        31
                   Acquired Abnormality       0.59      0.28      0.38       169
                         Medical Device       0.21      0.18      0.19        28
                 Anatomical Abnormality       0.74      0.67      0.70       116
                    Injury or Poisoning       0.41      0.33      0.37        27
                     Clinical Attribute       0.53      0.44      0.48       125
       Mental or Behavioral Dysfunction       0.26      0.15      0.19       131
                    Pathologic Function       0.54      0.24      0.33        59
                       Population Group       1.00      0.33      0.50         9
                    Embryonic Structure       0.40      0.17      0.24        12
                      Regulation or Law       0.18      0.08      0.11        98
                    Qualitative Concept       0.62      0.22      0.33        94
                 Congenital Abnormality       0.29      0.10      0.15        72
                     Functional Concept       0.00      0.00      0.00        35
                  Occupational Activity       0.47      0.24      0.32        67
                         Mental Process       0.29      0.19      0.23        62
     Professional or Occupational Group       0.25      0.09      0.13        11
                           Organization       0.50      0.29      0.37        90
                                   Food       0.00      0.00      0.00        74
                              Eukaryote       0.00      0.00      0.00        20
                  Phenomenon or Process       0.54      0.22      0.32        58
       Health Care Related Organization       0.50      0.10      0.17        49
                      Organism Function       0.12      0.06      0.09        31
               Organ or Tissue Function       0.36      0.15      0.21        34
                        Social Behavior       0.31      0.08      0.13        59
                        Idea or Concept       0.96      0.32      0.48        78
                              Bacterium       0.00      0.00      0.00         2
                               Chemical       0.56      0.17      0.26        29
          Natural Phenomenon or Process       0.31      0.17      0.22        24
                               Activity       0.00      0.00      0.00         2
                   Professional Society       0.45      0.41      0.43       123
                   Health Care Activity       0.33      0.06      0.10        17
               Element, Ion, or Isotope       0.17      0.05      0.07        21
                   Physiologic Function       0.38      0.25      0.30        32
         Daily or Recreational Activity       0.65      0.47      0.54       129
    Biomedical Occupation or Discipline       0.00      0.00      0.00        10
           Chemical Viewed Structurally       0.73      0.40      0.52        20
                               Receptor       0.63      0.32      0.42        38
                                  Virus       0.75      0.17      0.27        18
                                 Tissue       0.00      0.00      0.00        21
                     Organism Attribute       0.00      0.00      0.00         7
           Chemical Viewed Functionally       0.50      0.31      0.38        32
                    Individual Behavior       0.12      0.12      0.12         8
                              Age Group       0.27      0.50      0.35         8
                        Group Attribute       0.44      0.41      0.42        17
           NLM Organizational Component       0.27      0.25      0.26        12
                          Cell Function       0.44      0.21      0.28        39
               Occupation or Discipline       0.43      0.07      0.12        90
                        Geographic Area       0.56      0.74      0.64        31
                          Clinical Drug       0.40      0.10      0.16        20
                                 Fungus       0.45      0.49      0.47        49
                      Research Activity       0.14      0.07      0.10        14
                              Substance       0.00      0.00      0.00         2
         Environmental Effect of Humans       1.00      0.29      0.44         7
              Patient or Disabled Group       0.00      0.00      0.00         4
                                  Human       0.38      0.19      0.25        16
              Laboratory or Test Result       0.00      0.00      0.00         1
                                Reptile       0.00      0.00      0.00         2
          Experimental Model of Disease       0.17      0.05      0.08        20
          Biologically Active Substance       0.00      0.00      0.00        16
                      Conceptual Entity       0.47      0.21      0.29        39
          Biomedical or Dental Material       0.69      0.19      0.30        47
                                 Mammal       0.00      0.00      0.00         1
                    Amino Acid Sequence       0.11      0.11      0.11        18
                         Body Substance       0.00      0.00      0.00         3
                              Amphibian       0.00      0.00      0.00         6
                      Biologic Function       1.00      0.08      0.15        12
                                   Bird       0.00      0.00      0.00         0
                   Anatomical Structure       0.50      0.12      0.20         8
                                Hormone       0.00      0.00      0.00        16
                         Classification       0.00      0.00      0.00         6
                                   Fish       0.00      0.00      0.00         3
                                 Animal       0.00      0.00      0.00         1
                                  Event       0.31      0.31      0.31        13
                 Body Space or Junction       0.00      0.00      0.00         3
                             Antibiotic       0.00      0.00      0.00        14
    Governmental or Regulatory Activity       0.77      0.38      0.51        26
                   Educational Activity       0.00      0.00      0.00         2
                               Archaeon       0.00      0.00      0.00        13
       Hazardous or Poisonous Substance       0.00      0.00      0.00         5
                       Machine Activity       0.40      0.32      0.35        19
                       Genetic Function       0.00      0.00      0.00        14
                     Inorganic Chemical       0.00      0.00      0.00         4
                               Behavior       0.75      0.30      0.43        10
     Human-caused Phenomenon or Process       0.00      0.00      0.00         7
   Molecular Biology Research Technique       0.44      0.31      0.36        13
                            Body System       0.40      0.44      0.42         9
                               Language       0.50      0.07      0.12        15
                               Organism       0.00      0.00      0.00         5
                                  Group       0.29      0.17      0.21        12
                           Family Group       0.00      0.00      0.00         2
                        Research Device       0.00      0.00      0.00         1
                        Physical Object       0.00      0.00      0.00         2
                            NLM Product       0.00      0.00      0.00         1

                            avg / total       0.51      0.42      0.40      8878                                 
'''

