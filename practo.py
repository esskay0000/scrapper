#! env/bin/python

from bs4 import BeautifulSoup
import requests
import sys

if __name__ == '__main__':
    print 'practo works...'
    r = requests.get(sys.argv[1])
    _data = r.text
    _soup = BeautifulSoup(_data,'html5lib')
    #_result = _soup.find_all('div',{'id':'resultsContainer'})
    _next = _soup.find('a',{'class':'page_link page_link_next'})
    _cnt = 2
    if _next:
        while _next:
            print _next.get('href'), '   ', _cnt
            _address = sys.argv[1] + str(_next.get('href'))
            print _address
            r = requests.get(_address)
            _soup = BeautifulSoup(r.text,'html5lib')
            _next = _soup.find('a',{'class':'page_link page_link_next'})
            _cnt = _cnt + 1
            import time
            time.sleep(10)
    else:
        print 'none found...'

