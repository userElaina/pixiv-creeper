import hashlib

from tols._mian import *
from tols._basic import bencode

_hash_set1={
	'md5','sha1',
	'sha224','sha256','sha384','sha512',
	'blake2b','blake2s',
	'sha3_224','sha3_256','sha3_384','sha3_512',
}
_hash_set2={
	'shake_128','shake_256',
}

def hashcode(s:all,api:str)->str:
	s=bencode(s)
	if api in _hash_set1:
		return eval('hashlib.'+api+'(s).hexdigest()')
	if api in _hash_set2:
		return eval('hashlib.'+api+'(s).hexdigest(512)')
	raise Warning(api+'not in module _hash')

def test():
	s='撒旦发生覅案说法案说法阿桑的歌♥のasfwaegwwadrawerweag'
	for i in _hash_set1|_hash_set2:
		print(i,hashcode(s,api=i))

print('import',__name__,'succ')
