#!/usr/bin/env python3
"""Render the website from real host LVGL screens, using synthetic music/art fixtures.
Requires Pillow and `make -C ui CROSS= host-render`. Run only in a disposable host
container: the existing host harness writes its fixture DB under /usr/data/fiio.
No downloaded album artwork or device screenshots are used.
"""
import argparse, math, os, shutil, sqlite3, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--output', type=Path, default=ROOT/'docs/site/zune')
p.add_argument('--allow-host-fixtures', action='store_true', help='acknowledge disposable /usr/data fixture writes')
a = p.parse_args()
if not a.allow_host_fixtures: p.error('--allow-host-fixtures is required; do not run on a player')
a.output.mkdir(parents=True, exist_ok=True)
colors = {'magenta':'ec008c', 'cyan':'00b7d8', 'orange':'ff751f', 'lime':'9bd238'}
with tempfile.TemporaryDirectory(prefix='disco-site-') as temp:
    tmp = Path(temp); art = tmp/'art'; art.mkdir()
    for k in range(8):
        folder = art/str(k); folder.mkdir()
        im = Image.new('RGB', (360,360)); px = im.load()
        for y in range(360):
            for x in range(360):
                v = (math.sin(x/80+k)+math.cos(y/95-k)+2)/4
                px[x,y] = (int(20+v*150), int(20+y/360*70+k*9)%256, int(65+x/360*100))
        d=ImageDraw.Draw(im)
        d.ellipse((45+k*4,45,300,300), outline=(245,185,125), width=3)
        d.polygon([(0,300-k*10),(360,100+k*10),(360,360),(0,360)], fill=(20+k*6,25,48+k*8))
        im.save(folder/'cover.png'); im.save(folder/'01.png')
        for big,size in [('c',320),('t',120)]: im.resize((size,size)).save(art/f'a{k}_{big}.bmp')
    db=tmp/'catalog.db'; con=sqlite3.connect(db)
    cols='ID INTEGER PRIMARY KEY,PATH,NAME,TITLE,ALBUM,ARTIST,GENRE,DISC,TRACK,IS_CUE,IS_ISO,IS_DSD,OFFSET,DURATION,ALBUM_ARTIST,IS_M3U,M3U_PATH'
    for table in ['SONG','MY_LOVE']: con.execute(f'CREATE TABLE {table}({cols})')
    con.execute('CREATE TABLE CUSTOM_PLAYLIST_INDEX(LIST_ID INTEGER PRIMARY KEY,LIST_NAME,M3U_PATH)')
    con.execute(f'CREATE TABLE CUSTOM_PLAYLIST({cols},PLAYLIST_ID)')
    albums=['Afterglow','Atlas','Endless Summer','Night Drive','OutRun','Monsters','Kids','Dreamwave']
    artists=['The Midnight','FM-84','The Midnight','Timecop1983','Kavinsky','The Midnight','The Midnight','Gunship']
    for k,(album,artist) in enumerate(zip(albums,artists)):
        con.execute('INSERT INTO SONG VALUES('+','.join('?'*17)+')',(k+1,str(art/str(k)/'01.png'),'01.png','Northern Lights',album,artist,'Electronic',1,1,0,0,0,0,240000,artist,0,''))
    con.commit(); con.close()
    dest=Path('/usr/data/fiio/db/song.db');dest.parent.mkdir(parents=True,exist_ok=True)
    for color,rgb in colors.items():
        for page,mode,extra in [('menu','preview-home',{'ZHFOCUS':'0'}),('music','preview-np',{}),('coverflow','preview-albums',{'ALBUM_VIEW':'2','ZUNE_LIBRARY_FIXTURE':'1','PREVIEW_SETTLE':'2000'}),('wall','preview-albums',{'ALBUM_VIEW':'1','ZUNE_LIBRARY_FIXTURE':'1','PREVIEW_SETTLE':'2000'}),('quick','preview-quick',{}),('stats','statsapp',{}),('immersive','preview-immersive',{'SITE_IMM_CONTROLS':'1'})]:
            shutil.copy2(db,dest)
            env={**os.environ,'SITE_ACCENT':rgb,'ZNP_PATH':str(art/'0/01.png'),'STATS_ART_DIR':str(art),'PREVIEW_TECH':'1','NULL_DEMO_FLAC':'1','CFG_INT':'disco_hints=2',**extra}
            ppm=tmp/f'{color}-{page}.ppm'
            subprocess.run([str(ROOT/'ui/tests/host_build/host-render'),'13','0',mode,'0',str(ppm)],env=env,check=True,stdout=subprocess.DEVNULL,timeout=35)
            Image.open(ppm).save(a.output/f'{color}-{page}.webp',quality=94,method=6)
            print(f'{color}/{page}',flush=True)
