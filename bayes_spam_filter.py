import os
import subprocess

# directories including preprocessed spam and ham for statistics
spamdir = 'data/enron1/spam'
hamdir = 'data/enron1/ham'

# function that calculates a probability of an email being spam
# based on a single included word
def pspam_given_word(word):
	total_num_spam = float(len([filename for filename in os.listdir(spamdir)]))
	total_num_ham = float(len([filename for filename in os.listdir(hamdir)]))
	# P(spam)
	pspam = total_num_spam/(total_num_ham + total_num_spam)
	# P(ham)
	pham = 1 - pspam
	# get counts of word in ham and spam
	cmd = 'grep -il ' + word + ' ' + spamdir + '/*.txt'
	word_in_spam = len(subprocess.check_output([cmd], shell=True).splitlines())
	cmd = 'grep -il ' + word + ' ' + hamdir + '/*.txt'
	word_in_ham = len(subprocess.check_output([cmd], shell=True).splitlines())
	# P(word|spam)
	pword_given_spam = word_in_spam/total_num_spam
	# P(word|ham)
	pword_given_ham = word_in_ham/total_num_ham
	# P(word)
	pword = pword_given_spam*pspam + pword_given_ham*pham
	return (pword_given_spam*pspam)/pword

print pspam_given_word('meeting')
