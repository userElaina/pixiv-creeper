from PIL import Image

p_end1={'jpg','jpeg','gif','png','bmp'}

def phash(pth:str)->int:
	try:
		im=Image.open(pth)
		im=im.resize((8,8),Image.ANTIALIAS).convert('L')
	except:
		return -1
	ans=0
	for i in im.getdata():
		ans+=int(i)
	avg=ans/64
	ans=0
	for i in im.getdata():
		ans=(ans<<1)|(1 if i<avg else 0)
	return ans

def dhash(pth:str)->int:
	try:
		im=Image.open(pth)
		im=im.resize((9,8),Image.ANTIALIAS).convert('L')
	except:
		return -1
	# print(list(im.getdata()))
	ans=0
	le=0
	n=0
	for i in im.getdata():
		if n:
			if n==8:
				n=0
			else:
				n+=1
			ans=(ans<<1)|(1 if le<int(i) else 0)
		else:
			le=int(i)
			n=1

	return ans

def hm_d(h1:int,h2:int)->int:
    h,d=0,h1^h2
    while d:
        h+=1
        d&=d-1
    return int(h)

print('import',__name__,'succ')