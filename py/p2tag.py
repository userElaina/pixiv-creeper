import p1
from tols import *
from tols.utols import *

places={
	'honkai',
	'genshin',
}

t_name_set={
	# "sakura",
	# "kallen",
	# "kiana",
	# "mei",
	# "fuhua",
	# "bronya",
	# "seele",
	# "olenyeva",
	# "durandal",
	# "rita",
	# "theresa",
	# "himeko",

	# "cecilia",
	# "sirin",
	# "syql",		#?时雨绮罗
	# "duya",		#?渡鸦
	# "carol",	#?卡萝尔
	# "ana",		#?安娜
	# "xing",		#?杏
	# "lcy",		#?林朝雨
	# "clx",		#?程立雪
	# "kkly",		#?可可利亚
	# "bella",	#?贝拉
	# "fyw",		#?绯玉丸
	# "nvwa",		#?丹朱
	# "fuxi",		#?苍玄
	# "tesla",	#?特斯拉
	# "einstein",	#?爱因斯坦
	# "Schrodinger",

	# "wzro",		#?武装人偶
	# "shenghen",	#?圣痕
	# "otto",
	# "welt",
	# "qgf",		#?齐格飞
	# "kevin",	#?凯文
	# "snake",	#?灰蛇
	# "homo",		#?吼姆
	# "honkai",

	# "elaina",
	"saya",		#?沙耶
	"flan",		#?芙兰

	# "keqing",
	# "fischl",
	# "ganyu",

	'noelle',
	'amber',
	'klee',
	'qiqi',
	'diona',

	'lzyqn',
}

not_name_set={
	'yuri',
	'cxbsdyh'
}

PTH='/root/log/pixiv/tag/'
bigpth=PTH+'tag.json'
big=openjs(bigpth)

#@ 0 is #tag and 1 is srch
#@ 0 s_mode=s_tag_full 有大小写 带#的tag
#@ 1 s_mode=s_tag 忽略大小写 直接搜索

#? 同人圈：cp图不能打单人tag


js=openjs('/root/log/pixiv/tag.json')
for name in js:
	sh('mkdir -p '+PTH+name)
	if isinstance(js[name][0],str):
		js[name]=[js[name].copy()]
	if len(js[name])==1:
		js[name].append(js[name][0])

s1='https://www.pixiv.net/ajax/search/artworks/'
s2='?order=popular_d&s_mode=s_tag'

def addset1(a:set,b:set)->set:
	return {i+j for i in a for j in b}

def addset2(a:str,b:set)->set:
	a=a.split(' ')
	x={a[0],}
	j=1
	while(j<len(a)):
		x={i+a[j] for i in addset1(x.copy(),b)}
		j+=1
	return x

space1={' ','_','-','','\t','·','・'}
space2={' ','_','-',''}

def addfull(x:str)->bool:
	for i in '_-()':
		if i in x:
			return True
	return False

def s2set(s:str,isname:bool=True)->set:
	if '(' in s:
		return {s,}
	set1={
		s,
		s.lower(),
		s.upper(),
		s[0].upper()+s[1:].lower(),
		' '.join([
			i0[0].upper()+i0[1:].lower()
				for i0 in s.lower().split(' ')
		]),
	}
	set2={
		i0 for i1 in set1 for i0 in addset2(
			i1,(space1 if isname else space2)
		) 
	}
	return set2

def tag2l(tag:str,nj:dict)->list:
	u=s1+urlencode(tag.replace('#',''))+s2
	if '#' in tag:
		u+='_full'
	res=p1.get(u)
	p='"total":[0-9]+,'
	n=int(p1.sgetl(res.text,p,8,-1)[0])
	if n==0:
		return 
	if tag in nj:
		if -32<=(n-nj[tag])<=8:
			return
	p='"id":"[0-9]+"'
	ans=p1.sgetl(res.text,p,6,-1)
	u+='&p='
	for i in range(2,n//60+2):
		if not i&15:
			print(i,'...')
		res=p1.get(u+str(i))
		ans+=p1.sgetl(res.text,p,6,-1)
	return n,ans


def mian(
	name:str,
	jmp:bool=True,	#@ if name not in NameSet: return
	up:bool=True,	#@ update dict
	down:bool=True,	#@ download list
	rm:bool=False,	#@ del i for i not in tags
	upbig:bool=True,#@ update list
):
	'''
	jmp:\n
		if name not in NameSet: return
	up:\n
		update dict
	down:\n
		download list
	rm:\n
		del i for i not in tags
	'''
	if name in not_name_set:
		return 'jmp'

	if jmp and name not in t_name_set:
		return 'jmp'

	anspth=PTH+name+'/'+name+'.json'
	ans=openjs(anspth)
	npth=PTH+name+'/'+name+'_n.json'
	nj=openjs(npth)
	
	if up or rm:
		print('find tags',name)
		ftags={
			'##'+i for j in js[name][0]
				for i in s2set(j,isname=bool(name not in places))
		}|{
			i.lower().replace(' ','') 
				for i in js[name][1]
		}|{
			i.lower() 
				for i in js[name][1] 
					if addfull(i)
		}
		divn='/'+str(len(ftags))
		print('\n',name,divn)
		print(ftags)

	if up:
		print('up',name)
		rn=0
		for tag in ftags:
			rn+=1
			flg=str(rn)+divn+' '+tag
			print('\nget list of',flg)
			l=tag2l(tag,nj)
			if l:
				nj[tag],ans[tag]=l
				sve(anspth,ans)
				sve(npth,nj)
				print('end',nj[tag],flg)
			else:
				print('jmp',flg)

	if rm:
		for tag in nj.copy():
			if tag not in ftags:
				del nj[tag]
				print('del nj',tag)
		for tag in ans.copy():
			if tag not in ftags:
				del ans[tag]
				print('del ans',tag)
		sve(anspth,ans)
		sve(npth,nj)

	if down:
		rn=0
		divn='/'+str(len(ans))
		for tag in ans:
			rn+=1
			flg=str(rn)+divn+' '+tag
			print('begin down',flg)
			p1.lp(ans[tag])
			print('end down',flg)
	
	if upbig:
		big[name]=sorted({
			i for tags in ans for i in ans[tags]
		})
		sve(bigpth,big)

if __name__=='__main__':
	for i in js:
		mian(i,jmp=False,up=False,down=False)
