#! env/bin/python

from bs4 import BeautifulSoup
import requests
import sys

def Icont():
    _str = input('\ndo you want to continue?\n')
    if _str <> 1:
        sys.exit()


def GetLabs(_result):
    _lab_listing = _result.find_all('div',{'class':'listing-row diagnostic-listing-row'})
    for _e in _lab_listing:
        _lab_name_div = _e.find('div',{'class':'diag-details-block diag-name-container'})
        _lab_html_page = _lab_name_div.find('a',{'class':'link doc-name smokeliftdiagnosticLink'})
        print _lab_html_page.get('href')
        _lab_name_h2 = _lab_name_div.find('h2')
        print _lab_name_h2.text.strip()
        _lab_location_span = _lab_name_div.find('span',{'itemprop':'address'})
        print _lab_location_span.text.strip()
        _r = requests.get(str(_lab_html_page.get('href')))
        _data = _r.text
        _soup = BeautifulSoup(_data)
        _div_address = _soup.find('div',{'class':'practice-address'})
        _web_address = _div_address.text
        print _web_address
        _span_postal_address = _soup.find('span',{'itemprop':'address'})
        _meta_address = _span_postal_address.find_all('meta')
        _postal_address = {}
        for _m in _meta_address:
            print _m['itemprop'],_m['content']
        print '\n\n\nsleeping....'
        import time
        time.sleep(10)




def ScanPractoLab(_city):
    _site = 'https://practo.com/' + _city + '/diagnostics'
    r = requests.get(_site)
    _data = r.text
    _soup = BeautifulSoup(_data,'html5lib')
    _next = _soup.find('a',{'class':'page_link page_link_next'})
    _cnt = 2
    _result = _soup.find('div',{'id':'resultsContainer'})
    GetLabs(_result)
    print '\n\n\nsleeping.... next'
    import time
    time.sleep(10)
    if _next:
        while _next:
            print _next.get('href'), '   ', _cnt
            _address = _site + str(_next.get('href'))
            print _address
            r = requests.get(_address)
            _soup = BeautifulSoup(r.text,'html5lib')
            _result = _soup.find('div',{'id':'resultsContainer'})
            GetLabs(_result)
            _next = _soup.find('a',{'class':'page_link page_link_next'})
            _cnt = _cnt + 1
            print '\n\n\nsleeping.... next'
            import time
            time.sleep(10)
    else:
        print 'none found...'



if __name__ == '__main__':
    print 'practo works...\n\n\n'
    ScanPractoLab(sys.argv[1])
