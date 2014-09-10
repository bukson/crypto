from __future__ import division
from myEncoding import hexdecode, hexencode
from xor2 import xor2
from string import ascii_letters, ascii_lowercase, digits
from numpy.linalg import norm
from math import log10
from types import StringType

class TextScore(object):
	''' abstract class representing an object, that can "score" the
		the text '''

	def __init__(self):
		pass

	def score(self, text):
		''' Abstract function to score the text,
		the bigger the score, the more probability that
		in belongs to (default) english '''
		pass

class EtaoinDict(TextScore):
	pass

class CoincidenceDict(TextScore):
	pass
	
class NormDict(TextScore):
	''' use norm and vector of frequency to count the score of text'''
	engFreq = {
				'a' : 0.08167,
				'b' : 0.01492,
				'c' : 0.02782,
				'd' : 0.04253,
				'e' : 0.13,
				'f' : 0.02228,
				'g' : 0.02015,
				'h' : 0.06094,
				'i' : 0.06966,
				'j' : 0.00153,
				'k' : 0.00772,
				'l' : 0.04025,
				'm' : 0.02406,
				'n' : 0.06749,
				'o' : 0.07507,
				'p' : 0.01929,
				'q' : 0.00095,
				'r' : 0.05987,
				's' : 0.06327,
				't' : 0.09056,
				'u' : 0.02758,
				'v' : 0.00978,
				'w' : 0.0236,
				'x' : 0.0015,
				'y' : 0.01974,
				'z' : 0.00074,
				}

	def __init__(self):
		self.__dict = {}
		for char in ascii_lowercase:
			self.__dict[char] = 0.0
		self.__count = 0
		self.__bad = 0 # characketrs < 32, usefull to distinguish between A and a

	def __insert(self, letter):
		if 'a' <= letter.lower() <= 'z':
			self.__dict[letter.lower()] = self.__dict[letter.lower()] + 1
		elif ord(letter) < 32:
			self.__bad += 1
		self.__count += 1
		return self

	def __insertMany(self, letters):
		for l in letters:
			self.__insert(l)
		return self

	def score(self, text):
		self.__insertMany(text)
		if self.__count == 0:
			score =  -1000.0,-1000.0
		else:
			score = - norm([(self.__dict[k] / self.__count) - self.engFreq[k]
				for k in self.engFreq.keys()])
		for k in self.__dict:
			self.__dict[k] = 0
		bad = - self.__bad
		self.__count = 0
		self.__bad = 0
		return (score, bad)

input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

class NgramDict(TextScore):
    ''' use ngrams to score the text '''
    def __init__(self, ngramfile, sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        for line in file(ngramfile):
            key,count = line.split(sep) 
            self.ngrams[key] = int(count)
        self.ngramLen = len(key)
        self.all = sum(self.ngrams.itervalues())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.all)
        self.floor = log10(0.01 / self.all)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        # prepare text
        text = text.replace(" ","")
        # print text
        for i in xrange(len(text) - self.ngramLen + 1):
            chunk = text[i:i+self.ngramLen].upper()
            if chunk in self.ngrams: 
                score += ngrams(chunk)
            else: 
                score += self.floor
        return score / (len(text) - self.ngramLen + 1)

def crack(input, textscore=NgramDict('english_quadgrams.txt')):
	poss = []
	keys = []
	if type(input) == StringType:
		input = map(ord, input)
	# for char in map(ord, ascii_letters + digits + ' \n\t'):
	for char in	xrange(0,128):
		xorLetters = []
		for i in input:
				xorLetters.append(chr(xor2([char], [i])[0]))
		poss.append(textscore.score(''.join(xorLetters)))
		keys.append(char)
	bestIndex = poss.index(max(poss))
	key = keys[bestIndex]
	result = []
	for i in input:
		result.append(chr(xor2([key], [i])[0]))
	return (''.join(result),key) # dodane ''.join

def crackText(input, textscore):
	return crack(input, textscore)[0]

def crackKey(input, textscore):
	return crack(input, textscore)[1]

