import urllib.request
from bs4 import BeautifulSoup
import re
import os
import requests
import subprocess
import sys
import inquirer


ost_title_list = []
ost_dict = {}
ost_name = ""
dir_path = "./test/"
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
'AppleWebKit/537.36 (KHTML, like Gecko) '\
'Chrome/55.0.2883.95 Safari/537.36 '




def fetch_ost_dict():
    query = sys.argv[1].replace(" ", "+")
    base_url = 'https://downloads.khinsider.com/'
    search_url = base_url +'/search?search=' + query
    req = urllib.request.Request(search_url, headers={'User-Agent': ua})
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    mp3s = soup.find_all(href=re.compile("downloads.khinsider.com/game-soundtracks/album/"))
    for mp3 in mp3s:
        title = mp3.get_text()
        url = mp3.get('href')
        ost_dict[title] = url
        ost_title_list.append(title)
    return(ost_dict)

def select_ost(ost_dict):
    ost_candidate_list = []
    global ost_name
    ost_name = ""
    for title in ost_dict:
        ost_candidate_list.append(title) 
    ost_candidates = [ 
        inquirer.List('selected', 
            message="What OST do you want download?", 
            choices=ost_candidate_list, 
        ), 
    ] 

    requires = inquirer.prompt(ost_candidates)
    requires_list = list(requires.values()) 
    ost_name = requires_list[0]
    return(ost_name)

def get_mp3(ost_name, ost_dict):
    mp3_url_list = []
    ost_url = ost_dict[ost_name]
    req = urllib.request.Request(ost_url, headers={'User-Agent': ua})
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
        dir_path = url.split('/')[5]
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        audio_url = soup.find('audio').get('src')
        subprocess.call('wget -P %s %s' % (dir_path, audio_url), shell=True)

def main():
    global ost_title_list
    global ost_name
    fetch_ost_dict()
    select_ost(ost_dict)
    get_mp3(ost_name, ost_dict)

if __name__ == "__main__":
    main()
    
        