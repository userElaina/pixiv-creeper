import os
from os.path import getsize
from tols import *
from tols.pictols import p_end1

PTH='/root/log/pixiv/all/'

epth='/root/log/pixiv/exists.list'
exists=[int(i) for i in opens(epth).split('\n') if i!='']

erpth2='/root/log/pixiv/errs2.list'

errs=set()

def _f(pid:str)->None:
	
	_pth=PTH+str(pid)+'/'
	for i in os.walk(_pth):
		for j in i[2]:
			ppth=i[0]+j
			if j.rsplit('.',1)[-1] not in p_end1:
				continue
			if getsize(ppth)<100:
				errs.add(int(pid))
				print(pid)

rn=0
for i in exists:
	_f(i)
	rn+=1
	if not rn%23333:
		print(rn,i)


sve(erpth2,sorted(errs))