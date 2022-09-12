
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
import pickle


alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
alphabetDigits = '0123456789'
alphabetPunctiuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
alphabetComplete = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


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


def generate_num_code(l):
	code = ''

	for j in range(l):
		code += random.choice(alphabetDigits)

	print(code)


def generate_lower_code(l):
	code = ''

	for j in range(l):
		code += random.choice(alphabetLower)

	print(code)


def generate_upper_code(l):
	code = ''

	for j in range(l):
		code += random.choice(alphabetUpper)

	print(code)


def generate_onlychars_code(l):
	code = ''

	for j in range(l):
		code += random.choice(alphabetUpper+alphabetLower)

	print(code)


def generate_alphanumeric_code(l):
	code = ''

	for j in range(l):
		code += random.choice(alphabetUpper+alphabetLower+alphabetDigits)

	print(code)


if __name__ == '__main__':

	if os.path.exists('state.dat'):
		# Restore the previously saved state
		print('Found state.dat, initializing random module')
		with open('state.dat', 'rb') as f:
			state = pickle.load(f)
		random.setstate(state)
	else:
		# Use a well-known start state
		print('No state.dat, seeding')
		random.seed(12345)

	generate_new(10)
	generate_from_key_word(10, 'Pierpaolo')
	generate_num_code(4)
	generate_lower_code(10)
	generate_upper_code(10)
	generate_onlychars_code(10)
	generate_alphanumeric_code(10)

	# Save state for next time
	with open('state.dat', 'wb') as f:
		pickle.dump(random.getstate(), f)