from tols import *
import os


PTH='C:\\Users\\Sakura\\AppData\\Local\\Packages\\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\\LocalState\\rootfs\\root\\log\\pixiv\\'

epth=PTH+'exists.list'
exists={int(i) for i in opens(epth).split('\n') if i!=''}

er1pth=PTH+'errs.list'
er1={int(i) for i in opens(er1pth).split('\n') if i!=''}

er2pth=PTH+'errs2.list'
er2={int(i) for i in opens(er2pth).split('\n') if i!=''}

sve1pth=PTH+'sve1.list'
sve1={int(i) for i in opens(sve1pth).split('\n') if i!=''}

sve1=sve1-er1
sve1=sve1-er2
sve(sve1pth,sorted(sve1))
sve(epth,sorted(exists))

need_sve=sorted(exists-sve1-er1-er2)

RPTH='D:\\pixiv\\'

def cp1(pid:Union[int,str],rpth:str,onlyp=False)->bool:
	p1=PTH+'all\\'+str(pid)

	if not onlyp:
		pjs=p1+'\\'+str(pid)+'.json'
		try:
			j1=openjs(pjs)
		except:
			er2.add(int(pid))
			sve(er2pth,sorted(er2))
			return False
		if j1['saved']:
			return True

	if not os.path.exists(rpth):
		os.makedirs(rpth)
		
	for i in os.walk(p1):
		if i[0]!=p1:
			print('Err Bad Path: ',i[0])
			continue
		for j in i[2]:
			if '_hash8' in j:
				order='del '+p1+'\\'+j
				print(order)
				sh(order)
				continue
			if onlyp and j.rsplit('.',1)[-1] not in {'jpg','gif','jpeg','png','bmp'}:
				continue
			pth=p1+'\\'+j
			order='copy '+pth+' '+rpth+j
			print(order)
			if sh(order)!=0:
				return False
			# input()
	
	return True


def sve_all()->None:
	rn=0
	for pid in need_sve:
		if pid>rn:
			rn+=23333
			print(pid,'end')
		if cp1(str(pid),RPTH+'all\\'+str(pid)+'\\'):
			sve1.add(int(pid))
			sve(sve1pth,sorted(sve1))
			# print(1)
			# continue
	
def sve_tag()->None:
	tag=openjs(PTH+'tag.json').keys()
	for name in tag:
		j1pth=PTH+'tag\\'+name+'\\tag_det.json'
		j1=openjs(j1pth)
		j2pth=PTH+'tag\\'+name+'\\tag_svd.json'
		j2=openjs(j2pth)

		for value in j1:
			n_v_pth=RPTH+'tag\\'+name+'\\'+value+'\\'
			l=set(j1[value].copy())
			if value not in j2:
				j2[value]=list()
			else:
				l-=set(j2[value].copy())
			for pid in sorted(l):
				if cp1(pid,n_v_pth,onlyp=True):
					j2[value].append(pid)
					sve(j2pth,j2)
				
def sve_usr()->None:
	j1pth=PTH+'usr\\usr.json'
	j1=openjs(j1pth)
	j2pth=PTH+'usr\\usr_svd.json'
	j2=openjs(j2pth)
	for uid in j1:
		u_pth=RPTH+'usr\\'+uid+'\\'

		l=set(j1[uid].copy())
		
		if uid not in j2:
			j2[uid]=list()
		else:
			l-=set(j2[uid].copy())
		for pid in sorted(l):
			if cp1(pid,u_pth,onlyp=True):
				j2[uid].append(pid)
				sve(j2pth,j2)

sve_all()
sve_tag()
sve_usr()

