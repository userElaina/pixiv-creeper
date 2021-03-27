import struct
import binascii

from tols._mian import *
from tols._basic import *
from tols._int import _inta2d,_intd2b

_b2ab=b'01'
_b8ab=b'01234567'
_b10ab=b'0123456789'
_b16ab=b'0123456789ABCDEF'

def n2encode(s:byte_type)->bytes:
	return bin(int(s)).encode()

def n2decode(s:byte_type)->bytes:
	return str(int(s,2)).encode()
	
def n8encode(s:byte_type)->bytes:
	return oct(int(s)).encode()

def n8decode(s:byte_type)->bytes:
	return str(int(s,8)).encode()

def n16encode(s:byte_type)->bytes:
	return hex(int(s)).encode()

def n16decode(s:byte_type)->bytes:
	return str(int(s,16)).encode()

def b16encode(s:byte_type)->bytes:
	return binascii.hexlify(s).upper()

def b16decode(s:byte_type)->bytes:
	return binascii.unhexlify(s)

_b32ab=b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
_b32rev=[bytes((i,)) for i in _b32ab]
_b32tab=[(a+b) for a in _b32rev for b in _b32rev]
_b32rev={v:k for k,v in enumerate(_b32ab)}

def b32encode(s:byte_type)->bytes:
	leftover=len(s)%5
	
	if leftover:
		s=s+b'\0'*(5-leftover) 
		# ? Don't use += 
	encoded=bytearray()
	from_bytes=int.from_bytes
	for i in range(0,len(s),5):
		c=from_bytes(s[i:i+5],'big')
		encoded+=(
			_b32tab[c>>30]+			# bits 1-10
			_b32tab[(c>>20)&0x3ff]+	# bits 11-20
			_b32tab[(c>>10)&0x3ff]+	# bits 21-30
			_b32tab[c&0x3ff]			# bits 31-40
		)

	if leftover:
		padchars=7-(leftover<<3)//5
		encoded[-padchars:]=b'='*padchars
	return bytes(encoded)

def b32decode(s:byte_type)->bytes:
	padchars=(-len(s))&0x007
	
	decoded=bytearray()
	for i in range(0,len(s),8):
		quanta=s[i:i+8]
		acc=0
		try:
			for c in quanta:
				acc=(acc<<5)+_b32rev[c]
		except KeyError:
			return b'err: b32decode'
		decoded+=acc.to_bytes(5,'big')
	
	if padchars and decoded:
		acc<<=5*padchars
		last=acc.to_bytes(5,'big')
		leftover=(43-5*padchars)//8  
		# 1: 4, 3: 3, 4: 2, 6: 1
		decoded[-5:]=last[:leftover]

	return bytes(decoded)

_b36ab=(
	b'0123456789'
	b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
)

def n36encode(s:byte_type)->bytes:
	return bdecode(_intd2b(int(s),36,_b36ab))

def n36decode(s:byte_type)->bytes:
	return str(int(s,36)).encode()

def b36encode(s:byte_type)->bytes:
	return bdecode(_intd2b(intencode(s),36,_b36ab))

def b36decode(s:byte_type)->bytes:
	return bencode(_intd2b(int(s,36),0,''))


_b58ab=(
	b'123456789'
	b'ABCDEFGHJKLMNPQRSTUVWXYZ'
	b'abcdefghijkmnopqrstuvwxyz'
)

def n58encode(s:byte_type)->bytes:
	return bdecode(_intd2b(int(s),58,_b58ab))

def n58decode(s:byte_type)->bytes:
	return str(int(_inta2d(s,58,_b58ab))).encode()

def b58encode(s:byte_type)->bytes:
	return bdecode(_intd2b(intencode(s),58,_b58ab))

def b58decode(s:byte_type)->bytes:
	return _intd2b(_inta2d(s,58,_b58ab),0,'').encode()

_b62ab=(
	b'0123456789'
	b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	b'abcdefghijklmnopqrstuvwxyz'
)

def n62encode(s:byte_type)->bytes:
	return bdecode(_intd2b(int(s),62,_b62ab))

def n62decode(s:byte_type)->bytes:
	return str(int(_inta2d(s,62,_b62ab))).encode()

def b62encode(s:byte_type)->bytes:
	return bdecode(_intd2b(intencode(s),62,_b62ab))

def b62decode(s:byte_type)->bytes:
	return _intd2b(_inta2d(s,62,_b62ab),0,'').encode()

_b64ab=(
	b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	b'abcdefghijklmnopqrstuvwxyz'
	b'0123456789'
	b'+/'
)

def b64encode(s:byte_type)->bytes:
	return binascii.b2a_base64(s,newline=False)

def b64decode(s:byte_type)->bytes:
	return binascii.a2b_base64(s)


_a85chars1=[bytes((i,)) for i in range(33, 118)]
_a85chars2=[(a+b) for a in _a85chars1 for b in _a85chars1]

def _85encode(s:byte_type,chars1:list,chars2:list,foldnuls=False,foldspaces=False):
	padding=(-len(s))%4
	if padding:
		s=s+b'\0'*padding
		# ? Don't use += 
	words=struct.Struct('!%dI'%(len(s)//4)).unpack(s)

	chunks=[
		b'z' if foldnuls and not word else
		b'y' if foldspaces and word==0x20202020 else(
			chars2[word//614125]+
			chars2[word//85%7225]+
			chars1[word%85]
		)for word in words
	]
	return b''.join(chunks)


_a85l=b'<~'
_a85r=b'~>'

def a85encode(s:byte_type,*,foldspaces=False,pad=False)->bytes:
	result=_85encode(s,_a85chars1,_a85chars2,True,foldspaces)
	return _a85l+result+_a85r

def a85decode(s:byte_type,*,foldspaces=False)->bytes:
	if s.endswith(_a85r):
		s=s[:-2]
	if s.startswith(_a85l):
		s=s[2:]
	
	packI=struct.Struct('!I').pack
	decoded=[]
	decoded_append=decoded.append
	curr=[]
	curr_append=curr.append
	curr_clear=curr.clear
	for x in s+b'u'*4:
		if b'!'[0]<=x<=b'u'[0]:
			curr_append(x)
			if len(curr)==5:
				acc=0
				for x in curr:
					acc=85*acc+(x-33)
				try:
					decoded_append(packI(acc))
				except:
					return b'err: a85decode'
				curr_clear()
		elif x==b'z'[0]:
			if curr:
				continue
			decoded_append(b'\0\0\0\0')
		elif foldspaces and x==b'y'[0]:
			if curr:
				continue
			decoded_append(b'\x20\x20\x20\x20')
		else:
			continue

	result=b''.join(decoded)
	padding=4-len(curr)
	if padding:
		result=result[:-padding]
	return result


_b85ab=(
	b'0123456789'
	b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	b'abcdefghijklmnopqrstuvwxyz'
	b'!#$%&()*+-;<=>?@^_`{|}~'
)
_b85chars1=[bytes((i,)) for i in _b85ab]
_b85chars2=[(a+b) for a in _b85chars1 for b in _b85chars1]
_b85dec=[None]*256

for i,c in enumerate(_b85ab):
	_b85dec[c]=i

def b85encode(b:byte_type)->bytes:
	return _85encode(b,_b85chars1,_b85chars2)

def b85decode(b:byte_type)->bytes:
	padding=(-len(b))%5
	b=b+b'~'*padding
	# ? Don't use += 

	out=[]
	packI=struct.Struct('!I').pack
	for i in range(0,len(b),5):
		chunk=b[i:i+5]
		acc=0
		try:
			for c in chunk:
				acc=acc*85+_b85dec[c]
			out.append(packI(acc))
		except:
			return b'err:b85decode'

	result=b''.join(out)
	if padding:
		result=result[:-padding]
	return result

_b91ab=(
	b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	b'abcdefghijklmnopqrstuvwxyz'
	b'0123456789'
	b'!#$%&()*+,./:;<=>?@[]^_`{|}~"'
)

def b91encode(s:byte_type)->bytes:
	return bdecode(_intd2b(intencode(s),91,_b91ab))

def b91decode(s:byte_type)->bytes:
	return _intd2b(_inta2d(s,91,_b91ab),0,'').encode()


_ps={
	2:('[^01]+',False,),
	8:('[^0-7]+',False,),
	16:('[^0-9A-Fa-f]+',True,),
	32:('[^2-7A-Za-z]+',True,),
	36:('[^0-9A-Za-z]+',True,),
	58:('[^1-9A-HJ-NP-Za-z]+',False,),
	62:('[^0-9A-Za-z]+',False,),
	64:('[^0-9A-Za-z\+\-]+',False,),
	85:('',False,),
	91:('',False,),
	92:('',False,),
}

_base_set1={
	'n2',
	'n8',
	'b16',
	'b32',
	'n36',
	'b36',
	'n58',
	'b58',
	'n62',
	'b62',
	'b64',
	'a85',
	'b85',
	'b91',
}

def basecode(s:all,api:str,en:bool=True,ab:str=None)->str:
	if api not in _base_set1:
		raise Warning(api+' not in module _base')
	if api.startswith('a'):
		ab=None
	l=int(api[1:])
	if ab:
		if len(ab)==l:
			ab2=eval('_b'+str(l)+'ab').decode()
		else:
			ab=None
	if en:
		s=bdecode(s,p=_ps[api])
		api+='decode(s)'
		x=eval(api).decode(errors='backslashreplace')
		if ab:
			x=_intd2b(_inta2d(x,api,ab),api,ab2)
	else:
		if ab:
			s=_intd2b(_inta2d(s,api,ab2),api,ab)
		s=bencode(s)
		api+='encode(s)'
		x=eval(api).decode(errors='backslashreplace')
	return x



print('import',__name__,'succ')

