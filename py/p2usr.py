import p1
from tols import *
PTH='/root/log/pixiv/usr/'

anspth=PTH+'usr.json'
ans=openjs(anspth)
npth=PTH+'usr_n.json'
nj=openjs(npth)

s1='https://www.pixiv.net/ajax/user/'
s2='/following?limit=100&rest=show&offset='
s3='/profile/all'

def g2u(gid:str)->set:
	u=s1+gid+s2+'0'
	res=p1.get(u)
	p='"total":[0-9]+,'
	n=int(p1.sgetl(res.text,p,8,-1)[0])
	p='"userId":"[0-9]+"'
	ans=p1.sgetl(res.text,p,10,-1)
	rn=100
	u=s1+gid+s2
	while rn<n:
		res=p1.get(u+str(rn))
		ans+=p1.sgetl(res.text,p,10,-1)
		rn+=100
	return set(ans)

def u2set(uid:str)->list:
	u=s1+uid+s3
	res=p1.get(u)
	p='"[0-9]+":null'
	return sorted([
		int(i) for i in set(p1.sgetl(res.text,p,1,-6))
	])
		
def adown(gid:str='44447852')->list:
	marks=sorted(g2u(gid))
	rn=0
	divn='/'+str(len(marks))
	for uid in marks:
		rn+=1
		flg=uid+' '+str(rn)+divn
		print('begin',flg)
		sh('mkdir -p '+PTH+uid)
		l=u2set(uid)
		n=len(l)
		if uid in nj:
			if n<=nj[uid]:
				print('jmp',flg)
				continue
		nj[uid]=n
		ans[uid]=l
		sve(anspth,ans)
		sve(npth,nj)
		print(n,uid)
		p1.lp(l)
		print('end',flg)
	return marks

if __name__=='__main__':
	print(adown('26495670'))


