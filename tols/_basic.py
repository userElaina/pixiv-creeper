from tols._mian import *

def bencode(s:all)->byte_type:
	if isinstance(s,byte_types):
		return s
	try:
		return memoryview(s).tobytes()
	except TypeError:
		return str(s).encode(errors='backslashreplace')

def bdecode(s:all,p:tuple=('',False,))->byte_type:
	if isinstance(s,byte_types):
		return s
	try:
		return memoryview(s).tobytes()
	except TypeError:
		s=str(s)
		if p:
			s=re.sub(p[0],'',s.upper() if p[1] else s)
		return s.encode(encoding='ascii',errors='backslashreplace')

def intencode(s:all)->int:
	return int.from_bytes(bytes=bencode(s),byteorder='big',)

def intdecode(s:int)->bytes:
	s=abs(trys(int,s,0))
	decoded=bytearray()
	while s:
		decoded.append(s&255)
		s>>=8
	decoded.reverse()
	return bytes(decoded)

print('import',__name__,'succ')
