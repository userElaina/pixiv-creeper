import p1
from tols import *

PTH='/root/log/pixiv/rank/'
u='https://www.pixiv.net/ranking.php'

ps=list()
mode1=[
	'daily','daily_r18',
	'weekly','weekly_r18','r18g',
	'monthly',
	'rookie',
]
mode2=[
	'original',
	'male','male_r18',
	'female','female_r18',
]
content1=[
	'all','illust','manga',
]
for i in mode1:	
	for j in content1:
		ps.append((j,i))
for i in mode2:
	ps.append(('all',i))

def mian(today:str)->str:
	today=str(today)
	yesterday=None
	sh('mkdir -p '+PTH+today)

	anspth=PTH+today+'/'+today+'.json'
	ans=openjs(anspth)

	for i in ps:
		k=' '.join(i)
		if k in ans:
			print('jmp',k,today)
			continue
		p={
			'mode':i[1],
			'date':today,
			'content':i[0],
			'p':1,
			'format':'json',
		}

		res=p1.get(u,p=p)
		js=res.json()
		if 'error' in js:
			print('err',k,today)
			continue
		if 'prev_date' in js:
			if js['prev_date']:
				yesterday=js['prev_date']
		print(js['rank_total'],k,today)
		l=[j['illust_id'] for j in js['contents']]
		while js['next']:
			p['p']=js['next']
			res=p1.get(u,p=p)
			js=res.json()
			l+=[k['illust_id'] for k in js['contents']]
		ans[k]=l
		print(len(l),k,today)
		p1.lp(l)
		sve(anspth,ans)
		print('end',k,today,'\n')

	if yesterday:
		return yesterday

	p={
		'date':today,
		'format':'json',
	}
	res=p1.get(u,p=p)
	js=res.json()
	return js['prev_date']


if __name__=='__main__':
	t=20210213
	print('from',t)
	while t:
		t=mian(t)