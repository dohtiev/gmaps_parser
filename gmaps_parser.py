from selenium import webdriver
from parsel import Selector
from bs4 import BeautifulSoup
import time
from tkinter import *
import json

root = Tk()
root.title("gmaps_parser")
root.geometry("250x188+100+100")
root.resizable(False, False)
img = PhotoImage(file='background_img.png')
Label(
    root,
    image=img
).pack()
Name_v = StringVar()
City_v = StringVar()
Country_v = StringVar()
name_bool_v = BooleanVar()
phone_bool_v = BooleanVar()
link_bool_v = BooleanVar()

Label(text="Input information").place(x=65, y=0)
Label(text="Input required data:").place(x=0, y=20)
Label(text="City (option):").place(x=0, y=40)
Label(text="Country (option):").place(x=0, y=60)
Entry(textvariable=Name_v).place(x=115, y=20)
Entry(textvariable=City_v).place(x=115, y=40)
Entry(textvariable=Country_v).place(x=115, y=60)
Label(text="Choose output data").place(x=65, y=80)
option_1 = Checkbutton(text="Title", variable=name_bool_v)
option_2 = Checkbutton(text="Phone", variable=phone_bool_v)
option_3 = Checkbutton(text="Link", variable=link_bool_v)
option_1.place(x=0, y=100)
option_2.place(x=0, y=120)
option_3.place(x=0, y=140)
count = 0
Label(text="Data amount:").place(x=100, y=120)
def start():
    Name = Name_v.get()
    City = City_v.get()
    Country = Country_v.get()
    name_bool = name_bool_v.get()
    phone_bool = phone_bool_v.get()
    link_bool = link_bool_v.get()

    options = webdriver.ChromeOptions()

    options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        executable_path="D:\\progr\\scrap\\gmaps_parser\\chromedriver\\chromedriver.exe",
        options=options
    )
    url = f'https://www.google.com/maps/search/{Name}+{City}+{Country}'
    driver.get(url)
    time.sleep(5)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'lxml')
    divs = {}
    divs = soup.find_all(class_="Nv2PK")
    info = []
    count = 0
    response = Selector(page_content)

    results = []
    for element in divs:
        if name_bool == True:
            name = element.find(class_="qBF1Pd").text
            name = name.replace(name[0], "")
            l = len(name)
            name = name[:l-1]
        else:
            name = ""
        if phone_bool == True:
            near_phones_block = element.find_all(class_="W4Efsd")
            try:
                phones_block = near_phones_block[3]
                phone = phones_block.text
                phone = phone[-16:].replace(" ", "")
                if phone.isdigit()==False:
                    phone = ""
            except Exception:
                continue
        else:
            phone = ""
        if link_bool == True:
            link = element.find("a").get("href")
        else:
            link = ""
        info.append(
            {
                "name": name,
                "phone": phone,
                "link": link,
            })
        with open("base.json", "w", encoding="utf-8") as file:
            json.dump(info, file, indent=4, ensure_ascii=False)
        Label(text=count).place(x=180, y=120)
        count+=1
    driver.quit()
Button(text="Start", command=start).place(x=95, y=160)
Button(text="Quit", command=root.destroy).place(x=130, y=160)
root.mainloop()