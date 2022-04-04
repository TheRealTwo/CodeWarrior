import requests
from bs4 import BeautifulSoup

def html_to_text(html):
    html = list(html)
    ind = 0
    while html.count('<') != html.count('<a') + html.count('</a') and ind < len(html):
        if html[ind:ind + 1] == ['<'] and 'a' not in ''.join(html[ind + 1:ind + 3]):
            end_ind = ind
            while html[end_ind] != '>':
                end_ind += 1
            attr = html[ind:end_ind + 1]
            if ''.join(attr) in ('<p>', '</p>', '<li>', '</li>'):
                html.insert(end_ind + 1, '\n')
            del html[ind:end_ind + 1]
            ind -= 1
        ind += 1
    return ''.join(html).replace('\n\n', '\n').replace('$$$', '')

def post_content(id):
    page = requests.get('https://codeforces.com/blog/entry/' + str(id))
    soup = BeautifulSoup(page.content, 'html.parser')
    
    x = [str(x) for x in soup.body.find('div', attrs={'class' : 'content'})]
    x = sorted(x, key=len)[-1]
    return html_to_text(x)