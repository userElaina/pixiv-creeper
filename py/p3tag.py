t_name_set={
	"sakura",
	# "kallen",
	# "kiana",
	# "mei",
	# "fuhua",
	# "bronya",
	"seele",
	"olenyeva",
	# "durandal",
	"rita",
	"theresa",
	# "himeko",

	# "cecilia",
	"sirin",
	"syql",		#?时雨绮罗
	# "duya",		#?渡鸦
	# "carol",	#?卡萝尔
	# "ana",		#?安娜
	"xing",		#?杏
	# "lcy",		#?林朝雨
	# "clx",		#?程立雪
	# "kkly",		#?可可利亚
	# "bella",	#?贝拉
	# "fyw",		#?绯玉丸
	# "nvwa",		#?丹朱
	# "fuxi",		#?苍玄
	"tesla",	#?特斯拉
	# "einstein",	#?爱因斯坦
	# "Schrodinger",

	"wzro",		#?武装人偶
	"shenghen",	#?圣痕
	"otto",
	"welt",
	"qgf",		#?齐格飞
	# "kevin",	#?凯文
	"snake",	#?灰蛇
	# "homo",		#?吼姆
	# "honkai",

	# "elaina",
	"saya",		#?沙耶
	# "flan",		#?芙兰

	# "keqing",
	# "fischl",
	# "ganyu",

	# 'noelle',
	# 'amber',
	# 'klee',
	'qiqi',
	# 'diona',

	# 'lzyqn',
}

from tols import *
from math import log

PTH='/root/log/pixiv/all/'
TPTH='/root/log/pixiv/tag/'
bigpth=TPTH+'tag.json'
big=openjs(bigpth)
# detpth=TPTH+'tag_det.json'
# det=dict()

values=[50000,20000,10000,5000,2000,1000,500,0]
dirs=[str(i).zfill(5)+j for i in values for j in ['','r']]


def get_v(x:dict)->int:
	v1=(x['heart']<<1)+x['good']+int(log(3+x['see']))
	for i in values:
		if v1>=i:
			return i
	return 0

def get_dir(x:dict)->str:
	return str(get_v(x['hot'])).zfill(5)+('r' if x['r18'] else '')
	
rn=0
for name in big:
	if name not in t_name_set:
		continue
	print(name,'bg')
	det=dict()
	detpth=TPTH+name+'/tag_det.json'
	for i in dirs:
		det[i]=list()
	for pid in big[name]:
		p1=PTH+pid+'/'+pid+'.json'
		try:
			d1=get_dir(openjs(p1))
		except:
			print(pid,'err!')
			continue
		det[d1].append(pid)
		rn+=1
		if not rn%2333:
			print(rn)
	sve(detpth,sorted([int(i) for i in det]))
	print(name,'end')


# 76574477 err!
# 83507238 err!