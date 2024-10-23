from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random
import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from colorama import Fore

# Khởi động trình duyệt Chrome
options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Mở trang web
driver.get("https://nhasachphuongnam.com/van-hoc-duong-dai.html?sort_by=popularity&sort_order=desc&items_per_page=50")

def random_color():
    return str(random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]))
def wait_xpath(xpath):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

def generate_id():
    return 'B' + str(random.randint(1000000, 9999999))
def crawl(i):
    book = {
        'id': '',
        'name': '',
        'description': '',
        'big_category': '',
        'small_category': '',  
        'author': '',
        'NXB': '',
        'img': ''
    }
    print("Đang chọn quyển thứ" + str(i))
    wait_xpath('//*[@id="categories_view_pagination_contents"]/div[1]')
    driver.find_element(By.XPATH, '//*[@id="categories_view_pagination_contents"]/div[' + str(i) +']').click()
    wait_xpath('//*[@id="features"]/a')

    #lay category
    print(random_color() + "Đang lấy category")
    big_category = driver.find_element(By.XPATH, '//*[@id="breadcrumbs_11"]/div/a[4]/bdi').text
    small_category = driver.find_element(By.XPATH, '//*[@id="breadcrumbs_11"]/div/a[5]/bdi').text
    print(random_color() + "Đã lấy xong category")
    
    # lay mo ta 
    print(random_color() + "Đang lấy mô tả sách")
    description_div = driver.find_element(By.XPATH, '//*[@id="content_description"]/div')
    paragraphs = description_div.find_elements(By.TAG_NAME, "p")
    for p in paragraphs:
        book['description'] += p.text + '<br>'
    print(random_color() + "Đã lấy xong mô tả sách")

    driver.find_element(By.XPATH, '//*[@id="features"]/a').click()
    wait_xpath('//*[@id="content_features"]/div/div[4]/div[2]')
    # lay thong tin 
    print(random_color() + "Đang lấy thông tin sách")
    name = driver.find_element(By.XPATH, '//*[@id="tygh_main_container"]/div[3]/div/div/div/div/div[1]/div[2]/div[1]/h1/bdi').text
    author = driver.find_element(By.XPATH, '//*[@id="content_features"]/div/div[4]/div[2]').text
    NXB = driver.find_element(By.XPATH, '//*[@id="content_features"]/div/div[6]/div[2]').text
    img = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/span/a/img').get_attribute("src")
    print(random_color() + "Đã lấy xong thông tin sách")

    book['id'] = generate_id()
    book['name'] = name
    book['big_category'] = big_category
    book['small_category'] = small_category
    book['author'] = author
    book['NXB'] = NXB
    book['img'] = img

    print(random_color() + "Lưu thông tin vào file")
    with open('data.json', 'a', encoding='utf-8') as f:
        json.dump(book, f, ensure_ascii=False, indent=4)
        f.write(',\n')
    print(random_color() + "Đã lưu thông tin vào file")
    os.system('cls')
    driver.back()


try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ty-column4"))
    )
    print(random_color() + "Trang đã load xong.")
    
except:
    print("Không thể load trang.")

for i in range(1, 51):
    crawl(i)


