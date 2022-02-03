import json
import time
from lib2to3.pgen2 import driver

import pandas as pd
import requests
from attr import field
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.nba.com/stats/players/traditional/?sort=PTS&dir=1'
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']

    # driver.find_element_by_xpath(
    #     '/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[9]').click()

    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    # time.sleep(2)

    element = driver.find_element_by_xpath(
        "//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # print(html_content)

    # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # time.sleep(1)
    # Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    print(df)

    # Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)

    return df.to_dict('records')


option = Options()
option.headless = False
driver = webdriver.Chrome(options=option)

driver.get(url)
driver.implicitly_wait(10)  # in seconds
# time.sleep(3)
# driver.maximize_window()
# time.sleep(3)
driver.find_element_by_xpath(
    '//*[@id="onetrust-accept-btn-handler"]').click()


time.sleep(1)

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# 5. Converter dicionario em json
js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()
