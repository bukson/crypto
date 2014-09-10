from __future__ import division
from myEncoding import b64decode, hexdecode
from gmpy import popcount
from types import StringType
from numpy import matrix
from vigenere import vigenere
import textscore as ts


def hammingDist(s1, s2):
	''' count the hammingDist between two lists of equal lenth '''
	assert len(s1) == len(s2)
	
	if type(s1) == StringType:
		s1 = map(ord, s1)
	if type(s2) == StringType:
		s2 = map(ord, s2)

	return sum([popcount(x ^ y) for x,y in zip(s1,s2)])

def binDist(s1, s2):
	return sum([popcount(int(x == y)) for x,y in zip(s1,s2)])

# hammingdist(a XOR k, b XOR k) = hammingdist(a XOR b)
#
# def chardistance(from, to):
#	if type(from) == StringType:
#		from = ord(from)
#	if type(to) == StringType:
#		to = ord(to)
# 	return sum([ popcount(x ^ y) for x in xrange(from, to) 
#									for y in xrange(from, to)]) 
#				/ ((from - to) * (from - to))
#
# 3.38889: avg hammingdist between two ascii from 32..128
# 2.99924: avg hammingdist between two ascii from 65..128
# 2.47337: ...................................... 97..123 or 65..91
#
# Thats why when cracking KeyLen we use top values with the lowest 
# Hamming Distance score, so it is more close to 2.47337
# http://en.wikipedia.org/wiki/Index_of_coincidence
# example has score 2.6, close, beacuse it dont use non A..Z characters
# for example ',', ':', '.'
# Without white space, the score is from 2.19 to 2.78, so we cannot
# use the lowest value to choose, we need distance from 2.47
# (in real world i think it doesnt matter, but Real world is useless
# in mathematics)


def crackKeyLen(text):
	''' return top possible keylength of given text '''
	top = 5
	MAXKEYLEN = int(min(40, len(text)/2))
	def score(keylen):
		blocks = []
		score = 0.0 
		nblocks = int(len(text) / keylen)
		for i in xrange(nblocks):
			blocks.append(text[i*keylen : (i+1)*keylen])
		
		for i in xrange(len(blocks) - 1):
			score += hammingDist(blocks[i], blocks[i+1])
		return - score / ((len(blocks) - 1) * keylen) 
	scores = []
	keyRange = xrange(2, MAXKEYLEN + 1)
	for keylen in keyRange:
		scores.append((score(keylen), keylen))
	return [x[1] for x in sorted(scores, reverse=1)][:top]

def crack(text, scorer=ts.NgramDict('english_quadgrams.txt')):
	''' crack the vigenere cypher '''
	# possible keylengths
	text = map(ord, text)
	keyLens = crackKeyLen(text)
	# each element is text divided by key length and transponed
	blocksList = []
	for kl in keyLens:
		blocks = []
		for i in xrange(int(len(text) / kl)):
			blocks.append(text[i*kl : (i+1)*kl])
		blocksList.append(matrix(blocks).T)
	# crack key character with FreqDict 
	crackKeyFreq = lambda t: ts.crackKey(t, ts.NormDict())
	# for ech blocks in blocks list crack each charackter and then put it together
	# to have list of possible keys
	keys = [''.join(map(chr,k)) for k in map((lambda m : [crackKeyFreq(e) for e in m.tolist()]), blocksList)]
	# for k in keys: print map(ord,k)
	plaintexts = [ hexdecode(vigenere(text, k)) for k in keys]
	ptscores = [scorer.score(pt) for pt in plaintexts]
	# for score in ptscores: print score
	bestindex = ptscores.index(max(ptscores))
	return plaintexts[bestindex], keys[bestindex]

def crackText(text, scorer=ts.NgramDict('english_quadgrams.txt')):
	return crack(text, scorer)[0]

def crackTextF(file, scorer=ts.NgramDict('english_quadgrams.txt')):
	f = open(file, 'r')
	return crack(b64decode(f.read()), scorer)[0]

def crackKey(text, scorer=ts.NgramDict('english_quadgrams.txt')):
	return crack(text, scorer)[1]

def crackKeyF(file, scorer=ts.NgramDict('english_quadgrams.txt')):
	f = open(file, 'r')
	return crack(b64decode(f.read()), scorer)[1]




