from types import StringType

# input1 = '1c0111001f010100061a024b53535009181c'
# input2 = '686974207468652062756c6c277320657965' # "hit the bull's eye"

def xor2(s1, s2):
	assert len(s1) == len(s2)

	if type(s1) == StringType:
		s1 = map(ord, s1)
	if type(s2) == StringType:
		s2 = map(ord, s2)
		 
	result = []
	for i in xrange(len(s1)):
		result.append(s1[i] ^ s2[i])

	return result

# s3cr3t m3ssag3
# '.join(map(chr, hexdecode(xor2(input1, input2)))) -> "the kid don't play"