from bs4 import BeautifulSoup
import requests
import json

modules = {
    ('financials',                      '25b/oedmf'),
    ('supply-chain-and-manufacturing',  '25b/oedsc'),
    ('procurement',                     '25b/oedmp'),
    ('human-resources',                 '25b/oedmh'),
    ('sales',                           'oedms')
}

url = 'https://docs.oracle.com/en/cloud/saas/{module}/{code}/toc.htm'
data = {}

for module_index, module in enumerate(modules):
    # Get html pages for table of content
    html = requests.get(url=url.format(module=module[0], code=module[1])).text
    
    data[module[0]] = []
    data_temp = {}

    # Get the soup thingy
    soup = BeautifulSoup(html, 'html.parser')
    
    if module[0] == "financials":
        # Get list of headers and respective tables
        headers = soup.find_all('h2')[1::]
        lists = soup.select('ul:first-child', recurisve = False)
        tables_i = 0
        # Get all categroies plus list of tables
        for index, header in enumerate(headers):
            
            header = ' '.join(header.text.split()[1::])
            
            data_temp[header] = []
            
            for table in lists[tables_i].select('li > a'):
                data_temp[header].append({
                    "table_name" : table.text,
                    "url-suffix" : table.attrs['href']
                })
            
            if tables_i == 30: tables_i += 1
            else: tables_i += 2
                
        data[module[0]].append(data_temp)
    else:
        # Get list of headers and respective tables
        big_list = soup.find_all('ul')[0].find_all('li', recursive=False)[3::]
        
        # Get all categroies plus list of tables
        for index, header in enumerate(big_list):
            header = ' '.join(header.span.text.split()[1::])
            
            data_temp[header] = []
            
            inner_ul = big_list[index].find_all('ul', recursive=False)[0]
            tables = inner_ul.find_all('li', recursive=False)[0]
            
            for table in tables.select('li > a'):
                data_temp[header].append({
                    "table_name" : table.text,
                    "url-suffix" : table.attrs['href']
                })
    
        data[module[0]].append(data_temp)
    
import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
