from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
import requests
import json

modules = {
    ('financials', 'oedmf'),
    ('supply-chain-and-manufacturing', 'oedsc'),
    ('procurement', 'oedmp'),
    ('human-resources', 'oedmh'),
    ('sales', 'oedms')
}

url = 'https://docs.oracle.com/en/cloud/saas/{module}/25b/{code}/toc.htm'
data = {}

for module_index, module in enumerate(modules):
    # Get html pages for table of content
    html = requests.get(url=url.format(module=module[0], code=module[1])).text
    data_temp = {}

    # Get the soup thingy
    soup = BeautifulSoup(html, 'html.parser')

    # Get list of headers and respective tables
    headers = soup.find_all('h2')[1::]
    lists = soup.select('ul:first-child')
    
    data[module[0]] = []

    # Get all categroies plus list of tables
    for index, header in enumerate(headers):
        
        header = ' '.join(header.text.split()[1::])
        
        data_temp[header] = []
        
        for table in lists[index].select('li > a'):
            data_temp[header].append({
                "table_name" : table.text,
                "url-suffix" : table.attrs['href']
            })

    data[module[0]].append(data_temp)
    
import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
