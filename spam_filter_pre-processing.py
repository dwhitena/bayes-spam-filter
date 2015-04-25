import os
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime

# directories including preprocessed spam and ham for statistics
spamdir = 'data/enron1/spam'
hamdir = 'data/enron1/ham'

# function that calculates a probability of word in a spam email 
# as defined by (num of instances in spam)/(total num of instances)
def pword_spam(word):
	# get counts of word in spam emails
	cmd = 'grep -il ' + word + ' ' + spamdir + '/*.txt | wc -l'
	word_in_spam = float(subprocess.check_output([cmd], shell=True))
	# get counts of word in ham 
	cmd = 'grep -il ' + word + ' ' + hamdir + '/*.txt | wc -l'
	word_in_ham = float(subprocess.check_output([cmd], shell=True))
	# probability
	return word_in_spam/word_in_ham

words = []
for filename in os.listdir(spamdir):
	with open(spamdir + '/' + filename, 'r') as email:
		wordslist = [word for word in email.read().split(' ') 
		    if word.isalpha() and len(word) > 3 and word not in words]
		words = words + wordslist

# put the list into a pandas dataframe
words_df = pd.DataFrame(words, columns=['word'])
print len(words)
del(words)

a = datetime.now()
i = 0
words_df['theta'] = 0
words_df['wj'] = 0
for word in words_df['word'].values:
	# compute theta = P(word|spam)
	th = pword_spam(word)
	print th
	# save theta in the dataframe
	words_df.ix[i]['theta'] = th
	# save wj = log(theta/(1-theta)), a coefficient used in the
	# naive bayes algo, in the dataframe
	words_df.ix[i]['wj'] = np.log(th/(1.0-th))
	i += 1
	if i > 10:
		break
b = datetime.now()
c = b-a

print c.seconds
