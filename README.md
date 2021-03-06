# pyNyaav2 - A Nyaa v2 API wrapper.
#### Easy to use API wrapper for anyone.
![Python Version](https://img.shields.io/badge/python-3.5,%203.6,%203.7-blue.svg?longCache=true&style=for-the-badge) [![License](https://img.shields.io/github/license/noaione/pyNyaav2.svg?style=for-the-badge)](https://github.com/noaione/pyNyaav2/blob/master/LICENSE.md) ![Requirements](https://img.shields.io/requires/github/noaione/pyNyaav2.svg?style=for-the-badge)

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

### Requirements
- Python 3.5 or better
- Requests
- BeautifulSoup4

(Requests and Beautifulsoup4 will be installed automatically if you use `pip` command)


### Usage
**Using cmd (Upload)**:
```bat
nyaav2 -m upload -U USER -P PASS -i myfile.torrent --category anime_raw --description "My test upload using pyNyaav2" --anonymous --hidden
```

Will upload myfile.torrent with description plus upload it as Anonymous and Hidden.
#### For Sukebei, put --sukebei/-nsfw

**Using cmd (Search)**:
```
nyaav2 -m search -U USER -P PASS -i "hataraku saibou" --category all
```

Will search "hataraku saibou" in all category
#### For Sukebei, put --sukebei/-nsfw

**Full help (cmd: `nyaav2 -h`)**:
```bat
usage: nyaav2 [-h] --mode [{search,upload}] --sukebei/-nsfw --username USER --password PASSW
              --input TORKEY
              [--category {all,anime,amv,anime_eng,anime_non-eng,anime_raw,audio,audio_lossless,audio_lossy,books,books_eng,books_non-eng,books_raw,live_action,la_eng,la_idolpv,la_non-eng,la_raw,pictures,pics_graphics,pics_photos,softwaree,sw_apps,sw_games,art,art_anime,art_doujinshi,art_games,art_manga,art_pics,real_life,real_pics,real_videos}]
              [--name NAME] [--information INFO] [--description DESC]
              [--anonymous] [--hidden] [--remake] [--trusted]
```

**As a module (Upload)**:
```py
import pyNyaav2

UNAME = 'User'
PASSW = 'SecretPass'
CATEG = 1_2 #This is Anime English-translated, you can also type 'anime_eng', scroll to the very bottom for reference

description = """
**My test upload to Nyaa.si**

Note: This is an automated upload by [pyNyaav2](https://github.com/noaione/pyNyaav2)
"""
#for Sukebei, change set_opts to set_opts_sukebei
opts = pyNyaav2.set_opts(username=UNAME, password=PASSW, torrent='mystuff.torrent', category=CATEG, name='mystuff', information='https://noaione.github.io', description=description, anonymous=True, hidden=False, complete=False, remake=False, trusted=False)

#for Sukebei, change UploadTorrent to UploadSukebeiTorrent
ret = pyNyaav2.UploadTorrent(opts)

print(ret)
```

**As a module (Search)**:
```py
import pyNyaav2

UNAME = 'User'
PASSW = 'SecretPass'
KEYWORD = 'overlord s3'
CATEG = 1_2 #This is Anime English-translated, you can also type 'anime_eng', scroll to the very bottom for reference
PAGE = 1

#for Sukebei, change SearchTorrent to SearchSukebeiTorrent
ret = pyNyaav2.SearchTorrent(username=UNAME, password=PASSW, keyword=KEYWORD, category=CATEG, page=PAGE)

print(ret[0])
```
**Category List**: https://gist.github.com/noaione/2a74eb362588dcc4edc8684e9c270a8c
