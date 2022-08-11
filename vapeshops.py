from selenium import webdriver
from parsel import Selector
from bs4 import BeautifulSoup
import time

import json
options = webdriver.ChromeOptions()

options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    executable_path="D:\\progr\\scrap\\vapeshop\\chromedriver\\chromedriver.exe",
    options=options
)
url = 'https://www.google.com/maps/search/%D0%B2%D0%B5%D0%B9%D0%BF+%D1%88%D0%BE%D0%BF/@48.8566245,35.7839119,8z/data=!3m1!4b1?authuser=0&hl=uk'
driver.get(url)
time.sleep(45)
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'lxml')
divs = {}
divs = soup.find_all(class_="Nv2PK")
info = []
count = 0
response = Selector(page_content)

results = []
for element in divs:
    name = element.find(class_="qBF1Pd").text
    link = element.find("a").get("href")
    near_phones_block = element.find_all(class_="W4Efsd")
    # address_block = near_phones_block[2]
    # address = address_block.text.replace("  · Магазин електронних сигарет і аксесуарів     · ", "").replace("Безкоштовна Доставка В Будь-яку Точку Міста, ", "").replace("   · Магазин     · ", "")
    # print(address)

    try:
        phones_block = near_phones_block[3]
        phone = phones_block.text
        phone = phone[-16:].replace(" ", "")
    except Exception:
        phone = ""
        name = ""
    info.append(
        {
            "name": name,
            "phone": phone,
            "link": link,
        })
    with open("base.json", "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4, ensure_ascii=False)
    # count += 1
    # print(str(count))
# //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div/div/div
# for el in response.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'):
#     name = el.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div/span').extract_first('')
#     name = name.replace(name[0:21], "").replace("</span>", "")
#     print(name)
#     adress = el.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[1]/span[2]/jsl/span[2]').extract_first('')
#     adress = adress.replace(adress[0:21], "").replace("</span>", "")
#     print(adress)
#     phone = el.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[2]/span[2]/jsl/span[2]').extract_first('')
#     phone = phone.replace(phone[0:21], "").replace("</span>", "")
#     print(phone)
# print(results)

# for element in divs:
#     name = element.find(class_="qBF1Pd").text
#     phone = element.findNext('div', {'id':'QA0Szd'}).findNext('div').text
#     print(phone)
#     info.append(
#         {
#             "name": name,
#             "phone": phone,
#         })
#     with open("base.json", "w", encoding="utf-8") as file:
#         json.dump(info, file, indent=4, ensure_ascii=False)
#     count += 1
#     print(str(count))

driver.quit()