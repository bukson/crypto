from myEncoding import hexencode
from types import StringType

# input = '''Burning 'em, if you ain't quick and nimble
# I go crazy when I hear a cymbal'''

def vigenere(text, key):

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
	return hexencode(result)
