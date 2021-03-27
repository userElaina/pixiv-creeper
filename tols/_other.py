from urllib.parse import unquote_to_bytes,quote_from_bytes

from tols._mian import *
from tols._basic import *

_other_set1={
	'url',
	'uni',
}

def urlencode(s:str)->str:
	return quote_from_bytes(bencode(s))

def urldecode(s:str)->str:
	return unquote_to_bytes(bencode(s)).encode(errors='backslashreplace')

def uniencode(s:str)->str:
	return s.encode(encoding='unicode_escape').decode()
	
def unidecode(s:str)->str:
	return s.encode().decode(encoding='unicode_escape')

def othercode(s:str,api:str,en=True,)->str:
	return eval(api+('en' if en else 'de')+'code(s)')

print('import',__name__,'succ')