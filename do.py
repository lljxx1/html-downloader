# -*- coding: cp936 -*-
import urllib2,urllib,os,re,sys
from urlparse import urlparse
import re
import argparse
import pprint
from bs4 import BeautifulSoup 

#
#   解析路径
# 

def parse_path(url):
    url = url.split('/')
    url.pop()
    return '/'.join(url)

#
#   创建文件夹   
#

def make_a_dir(path):
    os.path.exists('.'+path) or os.makedirs('.'+path)

#
#   解析css文件 把background下载下来   
#

def parse_file(url, content):
    ms = re.findall('url\((.*?)\)',content)
    for m in ms:
        m = m.strip().strip('\"').strip('\'')
        r = save_metrial(parse_relative_path(url, m))
        #print r

#
#   相对路径解析成绝对路径
#

def parse_relative_path(url, path):
    path = path.replace('\\', "/")
    p_len = len(path)
    url = url.split('/')
    a_c = path.count('/');
    path_l = path.split('/');
    offset = 0;
    if a_c > 0:
        offset = path_l[0].count('.')
    if offset > 0:
        if path[offset:offset+1] == '/' :
            path = path[offset+1:p_len]
        else :
            path = path[offset:p_len]
    for i in range(1, offset):
        url.pop()
    print 'Relative path is:'+'/'.join(url)+'/'+path
    return '/'.join(url)+'/'+path

#
#   保存素材
#

def save_metrial(url):
    p_url = urlparse(url)
    #print(p_url)
    f_path = parse_path(p_url.path)
    make_a_dir(f_path)
    #content =  urllib.urlopen(url).read()
    #fp = open('.'+p_url.path,"w")
    #print url
    print 'Metrial url:' +url
    print 'Metrial save path:' +'.'+p_url.path
    urllib.urlretrieve(url, '.'+p_url.path)

#
#   保存文件
#

def save_file(url, site, type):
    if(url[0:4] != "http"): url = site+url
    #print url
    p_url = urlparse(url)
    #print p_url
    if (p_url.netloc != "fonts.googleapis.com"):
        domain = p_url.scheme+'://'+p_url.netloc
        #print(p_url)
        f_path = parse_path(p_url.path)
        print 'File path:'+f_path
        make_a_dir(f_path)
        print 'File url:'+ url
        content =  urllib.urlopen(url).read()
        if(type == "css"): parse_file(domain+f_path, content)
        print 'File save path:'+p_url.path
        fp = open('.'+p_url.path.strip(),"wb")
        fp.write(content)
        fp.close()
        #urllib.urlretrieve(url, '.'+p_url.path)

#
#   
#

def save_css_js(soup, site):
    all_css = soup.findAll('link',type="text/css")
    for css in all_css:
        save_file(css['href'], site, 'css')
    all_script = soup.findAll('script',type="text/javascript")
    for script in all_script:
        if script.get('src'):
            save_file(script['src'], site, 'js')

def save_img(soup, site):
	all_img = soup.findAll('img')
	for img in all_img:
		if img.get('src'): save_file(img['src'], site, 'img')

def parse(url):
    req = urllib2.Request(
            url = url,
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'}
    )
    p_url = urlparse(url)
    domain = p_url.scheme+'://'+p_url.netloc+'/'
    content = urllib2.urlopen(req).read()
    fa = open('index.html',"wb")
    fa.write(content)
    fa.close()
    soup = BeautifulSoup(content)
    save_img(soup, domain)
    save_css_js(soup, domain)

parse(sys.argv[1])


