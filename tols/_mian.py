import re
import os
import time
from typing import Union
from json import loads,dumps
from os import system as sh
from random import choice as rd
from time import sleep as slp


num_type=Union[int,float,str,]
num_types=(int,float,str,)

set_type=Union[list,set,tuple,]
set_types=(list,set,tuple,)

byte_type=Union[bytes,bytearray,memoryview,]
byte_types=(bytes,bytearray,memoryview,)

bytes_type=Union[str,bytes,bytearray,memoryview,]
bytes_types=(str,bytes,bytearray,memoryview,)

in_type=Union[dict,set_type,bytes_type,]
in_types=(dict,set_type,bytes_type,)


def pt(x)->None:
	print(repr(x))

def tm()->str:
	return time.strftime('%Y%m%d%H%M%S',time.localtime())
	
def lot(l:list)->str:
	return '\n'.join([str(i) for i in l])	

def trys(c:type,s:all,default=None)->all:
	try:
		return c(s)
	except:
		return default

def test(f)->None:
	while True:
		a=input()
		if a.startswith('exit'):
			exit()
		f(a)

def jsot(
	js:dict,
	pth:str=None,
	indent:Union[int,str]='\t',
	onlyascii:bool=False,
	sort:bool=False,
	log:bool=False
)->str:
	ans=dumps(js,indent=indent,ensure_ascii=onlyascii,skipkeys=True,sort_keys=sort)
	if log:
		ans=ans.replace('\n\t','\n')[1:-1]
	if pth:
		return open(pth,'w',encoding='utf-8',errors='backslashreplace').write(ans)
	else:
		return ans

def sve(pth:str,x:all)->None:
	if isinstance(x,dict):
		return jsot(x,pth=pth,sort=True)
	if isinstance(x,set_types):
		x=lot(x)
	if isinstance(x,byte_types):
		open(pth,'wb').write(x)
	else:
		open(pth,'w',encoding='utf-8',errors='backslashreplace').write(str(x))

def opens(pth:str,s:str='')->str:
	s=''
	try:
		s=open(pth,'r',encoding='utf-8').read()
	except FileNotFoundError:
		open(pth,'w').write(s)
	return s

def openls(pth:str)->list:
	s=''
	try:
		return [i for i in open(pth,'r',encoding='utf-8').read().split('\n') if i!='']
	except FileNotFoundError:
		open(pth,'w').write(s)
	return list()

def openjs(pth:str)->dict:
	try:
		return loads(open(pth,'rb').read())
	except FileNotFoundError:
		open(pth,'w').write('{\n}')
	return dict()	

print('import',__name__,'succ')