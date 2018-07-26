# pyNyaav2 - A Nyaa v2 API wrapper.
#### Easy to use API wrapper for anyone.

### Installation
```bat
pip install git+https://github.com/noaione/pyNyaav2
```

or

```bat
git clone https://github.com/noaione/pyNyaav2
cd pyNyaav2
python setup.py install
```

### Usage
Using cmd (Upload):
```bat
TODO
```

Using cmd (Search):
```
TODO
```

Full help:
```bat
TODO
```

As a module (Upload):
```py
import pyNyaav2

UNAME = 'User'
PASSW = 'SecretPass'
CATEG = 1_2 #This is Anime English-translated, you can also type 'anime_eng', scroll to the very bottom for reference

description = """
**My test upload to Nyaa.si**

Note: This is an automated upload by [pyNyaav2](https://github.com/noaione/pyNyaav2)
"""

opts = pyNyaav2.set_opts(username=UNAME, password=PASSW, torrent='mystuff.torrent', category=CATEG, name='mystuff', information='https://noaione.github.io', description=description, anonymous=True, hidden=False, complete=False, remake=False, trusted=False)

ret = pyNyaav2.UploadTorrent(opts)

print(ret)
```

As a module (Search):
```py
import pyNyaav2

UNAME = 'User'
PASSW = 'SecretPass'
KEYWORD = 'overlord s3'
CATEG = 1_2 #This is Anime English-translated, you can also type 'anime_eng', scroll to the very bottom for reference
PAGE = 1

ret = pyNyaav2.SearchTorrent(username=UNAME, password=PASSW, keyword=KEYWORD, category=CATEG, page=PAGE)

print(ret)
```
Category List: https://gist.github.com/noaione/2a74eb362588dcc4edc8684e9c270a8c
