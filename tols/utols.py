'''
`requests`
`hashname` `smd5` `fmd5` `urlencode` `urldecode`
`HEADERS`

	>>> hashname(x:str)->str
	>>> smd5(x:str)->str
	>>> fmd5(pth:str)->str
'''

import requests
from tols._other import urlencode,urldecode
from tols._u import hashname,smd5,fmd5

HEADERS={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

print('import',__name__,'succ')