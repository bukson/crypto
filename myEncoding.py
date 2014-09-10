#-*- coding: utf-8 -*- 
import base64
from types import StringType

# s3cr3t m3ssag3
# ''.join(map(chr, a)) -> "I'm killing your brain like a poisonous mushroom"

# input = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

def hexdecodeone(s):
		if ord('0') <= ord(s) <= ord('9'):
			return (ord(s) - ord('0'))
		elif ord('a') <= ord(s) <= ord('f'):
			return (ord(s) - ord('a') + 10)
		else:
			return (ord(s) - ord('A') + 10)

def hexdecode(ss, string=True):
	assert len(ss) % 2 == 0
	result = []
	for i in xrange(0, len(ss), 2):
		d1 = hexdecodeone(ss[i])
		d2 = hexdecodeone(ss[i + 1])
		result.append(d1 * 16 + d2)
	# idk if it has sense, cos why code smth as hex
	# when we use only number(can be dec or hex or oct, Python doesn't care)
	if string:
		return ''.join(map(chr, result))
	else:
		return result

def hexencode(ss):
	def myhex(s):
		h = hex(s)
		if len(h) < 4:
			return '0' + h[2]
		else:
			return h[2:]
	if type(ss) == StringType:
		ss = map(ord, ss)

	return ''.join((map(myhex, ss)))

# bez uzupełniania do 3 bajtów, wejście podzielne przez 3
def b64encodeone(blck):
	if blck < 26:
		return chr(ord('A') + blck)
	elif blck < 52:
		return chr(ord('a') + blck - 26)
	elif blck < 62:
		return chr(ord('0') + blck - 52) 
	elif blck == 62:
		return '+'
	else:
		return '/'

def b64encode(bytes):
	assert(len(bytes) % 3 == 0)

	result = []
	for i in xrange(0, len(bytes), 3):
		b1 = bytes[i]
		b2 = bytes[i + 1]
		b3 = bytes[i + 2]

		blck1 = b1 >> 2
		blck2 = ((b1 & 0x03) << 4) + (b2 >> 4) 	# 0x03 = 00000111
		blck3 = ((b2 & 0x0f) << 2) + (b3 >> 6)	# 0x0f = 00001111
		blck4 = b3 & 0x3f				# 0x3f = 00111111

		# result.extend([blck1, blck2, blck3, blck4])
		result.extend(map(b64encodeone, [blck1, blck2, blck3, blck4]))
	return ''.join(result)

def b64decode(ss):
	return base64.b64decode(ss)


# Vigenere cipher, its symmetric, so only one function
def vig(text, key, hexdecode=True):

	if type(text) == StringType:
		text = map(ord, text)

	if type(key) == StringType:
		key = map(ord, key)
	# empty key
	if len(key) == 0: 
		return text
	result = []
	for i in xrange(len(text)):
		result.append(text[i] ^ key[i % len(key)])
	if hexdecode:		
		return hexencode(result)
	else:
		return result

