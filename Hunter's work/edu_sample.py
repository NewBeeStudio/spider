# coding: utf-8
from BeautifulSoup import BeautifulSoup
import urllib2, cookielib, urllib, urlparse
import re, os
import requests # not used yet. need to install "requests"

# predefined arguments.
id = ''
pw = ''
interface_url = "/Interface.aspx?url=" # seems to be interface btw front/back-end.
assignment_url = "/Assignment.aspx?url="
login_suffix = "@php/v1_user/teacher/login?source=webTeahcer&version=2.4.0"
main_url = "http://www.zuoyehezi.com"

# turn web page into file name.
# not used yet
def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)  
    s = ''.join(c for c in s if c in valid_chars)
    return s

# make index for crawled pages -- into "index.txt"
# make page contents into directory called html.
def add_page_to_folder(page, content): 
    index_filename = 'index.txt'
    folder = 'html'                 
    filename = valid_filename(page) 
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\n')
    index.close()
    if not os.path.exists(folder): 
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)                
    f.close()


# original log in functions. 
# seems to be uncessecery.
def edu_login(id, pw):
    content = requests.get(page)
    # log in.
    login_url = main_url + interface_url + urllib.quote(login_suffix, safe='')
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    postdata = urllib.urlencode({
        'mobile':   id,
        'password': pw
        })
    req = urllib2.Request(login_url, data = postdata)
    useragent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    req.add_header('User-Agent', useragent)
    responce = urllib2.urlopen(req)

    # access homepage
    home_url = main_url + assignment_url
    responce = urllib2.urlopen(home_url)
    add_page_to_folder(home_url, responce.read())

def edu_crawl():
    # access question
    cookiename = '1HUuLSP7HSqJ4NyK1I0qMTHHr7Rxmz2bVJ3FRYFrO/OS6YF8mmNsqNbreKvmqebU'
                            # cookie: knowbox_teacherToken.
    ID = '211'              # id for question list.
    questionType =  '0'    # -1: all, 0: choice, 1: multi-choice, 2: answer, 5: cloze.
    collectType =   '0'     # 1: being collected. "收藏"
    outType =       '0'     # 2: not included "未出"
    pagesize =      '10'    # questions per page
    pagenum =       '0'     # pagination num.
    tmp_url =   "@php/v1_tiku/knowledge/question?source=webTeacher&from=kb&token=%s&version=2.4.0&knowledge_id=%s&question_type=%s&collect=%s&out=%s&page_size=%s&page_num=%s" % \
                (cookiename, ID, questionType, collectType, outType, pagesize, pagenum)

    question_url = main_url + interface_url + urllib.quote(tmp_url, safe='')
    print question_url
    responce = urllib2.urlopen(question_url)

    # TODO: get a suitable title for every page.
    add_page_to_folder("test.html", responce.read())

def main():
    # edu_login(id, pw)
    edu_crawl()

main()

# get_questions(type, ID, pagesize, pagenum, questionType, outType1, collectType1)