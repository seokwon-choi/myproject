from selenium import webdriver
import time
import pandas as pd
import argparse
import re
import math
from datetime import datetime

# 오늘 날짜 불러오기
today = datetime.today()
today_year = today.year
today_quarter = math.ceil(today.month/3)


# parser 생성
parser = argparse.ArgumentParser(description='set option')
parser.add_argument("--file_name", type=str,
                    default='service_center',
                    help="please input file name   ex) If you use only test, please input 'test'")
parser.add_argument("--input_url", type=str,
                    default = 'https://play.google.com/store/apps/details?id=com.lguplus.mobile.cs&hl=ko&gl=KR&showAllReviews=true',
                    help = "please input URL")
parser.add_argument("--year", type=int, default=today_year, help="please input year")
parser.add_argument("--quarter", type=int, default=today_quarter, help="please input quarter")
parser.add_argument("--only", default="False", help="True: only input data, False: latest to input data")
args = parser.parse_args()
url = args.input_url
input_year = args.year
input_quarter = args.quarter
output_path = '/content/drive/Shareddrives/capstone/Elegant_Friends/rsc/crawling_data/'+args.file_name+'.tsv'
mode_only = True if args.only == 'True' else False


# chromedriver option 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
chrome_options.add_argument('lang=ko')
driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver.get(url)


# 최신 버튼 누르기 (최신 날짜 별로 정렬)
latest_button = driver.find_element_by_xpath("//span[@class='DPvwYc']")
latest_button.click()
time.sleep(1.5)
latest = driver.find_elements_by_css_selector('div.OA0qNb.ncFHed > div.MocG8c.UFSXYb.LMgvRb')
latest[0].click()


# 더보기 스크롤까지 내리기
SCROLL_PAUSE_TIME = 1.5
last_height = driver.execute_script("return document.body.scrollHeight")
for c in range(100):
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

    dates = driver.find_elements_by_xpath("//div[@class='bAhLNe kx8XBd']")
    date = dates[-1].text.split('\n')[1]   # 더보기 누르기 전 가장 마지막 날짜를 확인
    date = re.split('년|월|일', date)
    year, month = date[0], date[1]

    if input_year > int(year):  # 해당 년도 해당 분기가 아닐 시 스크롤 중단
        break
    elif input_year == int(year) and input_quarter > math.ceil(int(month)/3):
        break


    spread_review = driver.find_elements_by_xpath("//span[@class='RveJvd snByac']")

    for i in range(len(spread_review)):
        driver.execute_script("arguments[0].click();", spread_review[i])

# 전체 리뷰 버튼 누르기
spread_review = driver.find_elements_by_xpath("//button[@jsaction='click:TiglPc']")

for i in range(len(spread_review)):
    driver.execute_script("arguments[0].click();", spread_review[i])

# 알바 리뷰 * 전체 리뷰 따로 수집 + 하나로 합치기
reviews = driver.find_elements_by_xpath("//span[contains(@jsname, 'bN97Pc')]")
long_reviews = driver.find_elements_by_xpath("//span[@jsname='fbQN7e']")
merged_reviews = [t.text if t.text!='' else long_reviews[i].text for i,t in enumerate(reviews)]

# 날짜, 범위 정하기
dates = driver.find_elements_by_xpath("//div[@class='bAhLNe kx8XBd']")
stars = driver.find_elements_by_xpath("//span[@class='nt2C1d']/div[@class='pf5lIe']/div[@role='img']")

# 리뷰, 날짜 별점 저장
res_dict = []
for i in range(len(merged_reviews)):

    date = dates[i].text.split('\n')[1]
    date2 = re.split('년|월|일', date)
    year, month = date2[0], date2[1]

    if mode_only: # 입력 년도/분기 데이터만 저장
        if input_year == int(year) and input_quarter == math.ceil(int(month)/3):
            res_dict.append({
                'DATE' : date,
                'STAR' : stars[i].get_attribute('aria-label'),
                'REVIEW' : merged_reviews[i]
            })
    else:  # 최신 데이터부터, 입력 년도/분기 데이터까지 모두 저장
        if input_year < int(year) or (input_year == int(year) and input_quarter <= math.ceil(int(month)/3)):
            res_dict.append({
                'DATE' : date,
                'STAR' : stars[i].get_attribute('aria-label'),
                'REVIEW' : merged_reviews[i]
            })

# 리뷰 개수 출력
print("총 리뷰 수:", len(res_dict))

# DataFrame 으로 만들기
res_df = pd.DataFrame(res_dict)

# tsv 파일로 변환
res_df.to_csv(output_path, sep='\t', mode='w', encoding = 'utf-8-sig')
driver.close()