#102202131 林鑫
import urllib.request
from bs4 import BeautifulSoup
url = "http://www.shanghairanking.cn/rankings/bcur/2020"
response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html,'html.parser')
table = soup.find('table',{'class':'rk-table'})
rows = table.find_all('tr')
print("排名\t学校名称\t省市\t学校类型\t总分")
for row in rows[1:]:#跳过表头行
    cols = row.find_all( 'td')
    rank = cols[0].text.strip()
    school_name = cols[1].text.strip()
    province = cols[2].text.strip()
    school_type = cols[3].text.strip()
    score = cols[4].text.strip()
    print(f"{rank}\t{school_name}\t{province}\t{school_type}\t{score}")
