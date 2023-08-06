# Ptt2Json

A simple python library to extract pages and posts information from https://www.ptt.cc/bbs/ to json format

```python
>>> from ptt2json import *
>>> ptt = PttPage(boardname="Gossiping")
>>> print(ptt.posts)

[{'url': '/bbs/Gossiping/M.1560591164.A.B9C.html',
  'post_id': 'M.1560591164.A.B9C',
  'timestamp': '1560591164',
  'title': '[新聞] 暴動！財經女神訪歐曬日光浴 白皙長腿惹',
  'nrec': '',
  'author': 'cycling',
  'mark': ''},
 {'url': '/bbs/Gossiping/M.1560591174.A.B05.html',
  'post_id': 'M.1560591174.A.B05',
  'timestamp': '1560591174',
  'title': '[新聞] 韓國瑜造勢到底多少人? 椅子精算師四叉貓算給你',
  'nrec': '',
  'author': 'sweat992001',
  'mark': ''},
 {'url': '/bbs/Gossiping/M.1560591182.A.50D.html',
  'post_id': 'M.1560591182.A.50D',
  'timestamp': '1560591182',
  'title': 'Re: [新聞] 大烏龍！攝影師砸30萬修MacBook 最後發現',
  'nrec': '',
  'author': 'YHOTV4096',
  'mark': ''},
  ...]
```
