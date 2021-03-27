'''
`trys` `test` `jsot` `sve` `opens` `openls` `openjs`

`pt` `tm` `lot` `sh` `rd` `slp`

`re` `time` `Union` `loads` `dumps`

`num` `set` `byte` `bytes` `in`

	>>> import re
	>>> import time
	>>> from typing import Union
	>>> from os import system as sh
	>>> from random import choice as rd
	>>> from time import sleep as slp

	>>> [num]   int,float,str,
	>>> [set]   list,set,tuple,
	>>> [byte]  bytes,bytearray,memoryview,
	>>> [bytes] str,bytes,bytearray,memoryview,
	>>> [in]    dict,[set],[bytes],

	>>> pt(x)
	>>> tm()->str
	>>> lot(l:list)->str
	
	>>> trys(s:all,c:type,default=None)->all
	>>> test(f)->None
	>>> jsot(js:dict,pth=None,indent='\t',onlyascii=False,sort=False,log=False)->str
	>>> sve(pth:str,x:all)->None
	>>> opens(pth:str,s='')->str
	>>> openls(pth:str)->list:
	>>> openjs(pth:str)->dict:
'''

if __name__=='__main__':
	raise Warning('This module can\'t run directly!')

from tols._mian import *

# from tols import codetols,intols,talktools,threadtols,utols


print('import',__name__,'succ')