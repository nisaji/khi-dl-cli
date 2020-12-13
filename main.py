import urllib.request
from bs4 import BeautifulSoup
import re
import os
import requests
import subprocess
import sys

def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)

def main():
    # khinsider.com
    url = sys.argv[1]
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) '\
    'Chrome/55.0.2883.95 Safari/537.36 '


    new_dir_path = url.split('/')[5]
    # print(new_dir_path)
    try:
        os.mkdir(new_dir_path)
    except FileExistsError:
        pass

    mp3_url_list = []
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    mp3s = soup.find_all(href=re.compile(".mp3"))
    for mp3 in mp3s:
        mp3_url = mp3.get('href')
        if mp3_url not in mp3_url_list:
            mp3_url_list.append(mp3_url)

    for mp3_url in mp3_url_list:
        base_url = 'https://downloads.khinsider.com'
        url = base_url + mp3_url
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        audio_url = soup.find('audio').get('src')
        print(audio_url)
        audio_file_name = new_dir_path + audio_url.split("/")[6].replace("%20", " ")
        # audio = requests.get(audio_url).content
        subprocess.call('wget -P %s %s' % (new_dir_path, audio_url), shell=True)

if __name__ == "__main__":
    main()
        