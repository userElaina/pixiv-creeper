import os
from tols import *
from tols.pictols import p_end1

PTH='/root/log/pixiv/'

er1pth=PTH+'errs.list'
er1={int(i) for i in opens(er1pth).split('\n') if i!=''}

er2pth=PTH+'errs2.list'
er2={int(i) for i in opens(er2pth).split('\n') if i!=''}

sve1pth=PTH+'sve1.list'
sve1={int(i) for i in opens(sve1pth).split('\n') if i!=''}

sve1=sve1-er1
sve1=sve1-er2
sve(sve1pth,sorted(sve1))

input('warning!!!')
input('anything will be deleted!!!')
a=input('R U sure?')
if 'yes' not in a:
	exit()

for pid in sve1:
	
	p1=PTH+'all/'+str(pid)
		
	for i in os.walk(p1):
		if i[0]!=p1:
			print('Err Bad Path: ',i[0])
			continue
		for j in i[2]:
			order='rm '+p1+'/'+j
			lj=j.rsplit('.',1)
			if '_hash8' not in lj[0] and lj[1] not in p_end1:
				continue
			print(order)
			# input()
			sh(order)