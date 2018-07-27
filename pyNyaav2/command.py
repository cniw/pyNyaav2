import argparse
import os, sys
import json

from .common import Nyaav2Exception
from .upload import set_opts, UploadTorrent
from .search import SearchTorrent

def main():
    parser = argparse.ArgumentParser(prog='nyaav2')
    parser.add_argument('--mode', '-m', required=True, default='search', const='search', nargs='?', choices=['search', 'upload'])
    parser.add_argument('--username', '-U' , required=True, dest='user',help='Your username')
    parser.add_argument('--password', '-P', required=True, dest='passw', help='Your password')
    parser.add_argument('--input', '-i', dest='torkey', required=True, action='store', default=None, help='Keyword to be search')
    parser.add_argument('--category', dest='cname', choices=['all', 'amv', 'anime_eng', 'anime_non-eng', 'anime_raw', 'audio_lossless', 'audio_lossy', 'books_eng', 'books_non-eng', 'books_raw', 'la_eng', 'la_idolpv', 'la_non-eng', 'la_raw', 'pics_graphics', 'pics_photos', 'sw_apps', 'sw_games'], required=False, action='store', default='anime_eng', help='Torrent category (default: anime_eng)')

    uploadmode = parser.add_argument_group('Upload Arguments')
    uploadmode.add_argument('--name', dest='name', required=False, action='store', default=None, help='Torrent name')
    uploadmode.add_argument('--information', dest='info', required=False, action='store', default=None, help='Torrent information (website, etc)')
    uploadmode.add_argument('--description', dest='desc', required=False, action='store', default=None, help='Torrent description (can be a file too)')
    uploadmode.add_argument('--anonymous', '-anon', dest='is_anon', action='store_true', required=False, default=False, help='Set torrent as an anonymous torrent')
    uploadmode.add_argument('--hidden', dest='is_hidden', action='store_true', required=False, default=False, help='Set torrent to hidden')
    uploadmode.add_argument('--remake', dest='is_remake', action='store_true', required=False, default=False, help='Set torrent as remake torrent')
    uploadmode.add_argument('--trusted', dest='is_trusted', action='store_true', required=False, default=False, help='Set torrent as trusted torrent')

    args = parser.parse_args()

    if args.mode == 'search':
        print('e')
    elif args.mode == 'upload':
        if os.path.splitext(args.torkey)[1] != '.torrent':
            raise Nyaav2Exception('Upload mode choosen but input argument not a torrent files')

        if args.desc is not None:
            if os.path.isfile(args.desc):
                with open(args.desc, 'rb') as fdesc:
                    descr = str(fdesc.read())
            else:
                descr = args.desc

        print('@@ Creating options')
        options = set_opts(username=args.user, password=args.passw, torrent=args.torkey, category=args.cname, name=args.name, information=args.info, description=descr, anonymous=args.is_anon, hidden=args.is_hidden, remake=args.is_remake, trusted=args.is_trusted)

        re = json.loads(UploadTorrent(options=options))

        hashhex = re['hash']
        torid = re['id']
        name = re['name']
        url = re['url']

        text = f'!! Torrent Successfully Uploaded\n@ Name: {name}\n@ ID: {torid}\n@ URL: {url}\n@ Torrent hash: {hashhex}'
        print(text)
        

if __name__=='__main__':
    main()