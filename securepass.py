
# creazione di password sicura:
# 	- lunghezza (min lunghezza max)
#	- tipo: num, alfanum, solo lettere
#	- simboli speciali
#	- upper lowercase
#	- parola chiave (non consigliato)

import string
import random
import os
import dbm
import numpy as np


alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
alphabetDigits = '0123456789'
alphabetPunctiuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
alphabetComplete = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
#string.digits  string.punctuation

type = 0 #(0: numerica, 1:alfanumerica, 2: letterale)
simbols = True 

def generate_from_key_word(l, kw):
	pw = ''

	numDigits = int(random.random()*10)
	numPunct = int(random.random()*10)

	for j in range(l):
		pw += random.choice(alphabetLower)
		if j <= (len(kw) - 1): 
			pw += kw[j].upper()

	print(pw)

def generate_new(l):
	pw = ''

	for j in range(l):
		pw += random.choice(alphabetComplete)

	print(pw)



if __name__ == '__main__':

	db = dbm.open('state.dat', 'c')
	state = db.get('state')

	if state != None:    
	    print('state found')
	    s = np.random.RandomState(int(state))
	    random.setstate(s)
	else:
	    # Use a well-known start state
	    random.seed(12345)
	    print('new state')

	#generate_from_key_word(length, keyWord)

	generate_new(20)
	db['state'] = random.getstate().__str__()
	db.close()
