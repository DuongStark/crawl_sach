from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random
import threading  # Để quản lý luồng
from colorama import Fore
import time

# Khóa để tránh xung đột khi ghi vào file
lock = threading.Lock()

def random_color():
    return str(random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]))

def wait_xpath(driver, xpath):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def generate_id():
    return 'B' + str(random.randint(1000000, 9999999))

def crawl_books(start, end, url):
    """Crawl sách từ index `start` đến `end` trên cùng một trình duyệt với link đã cho."""
    driver = webdriver.Chrome()
    driver.get(url + '?sort_by=popularity&sort_order=desc&items_per_page=50')  # Đảm bảo url được format đúng

    for i in range(start, end + 1):
        try:
            print(f"Đang chọn quyển thứ {i}")
            wait_xpath(driver, '//*[@id="categories_view_pagination_contents"]/div[1]')
            driver.find_element(By.XPATH, f'//*[@id="categories_view_pagination_contents"]/div[{i}]').click()
            wait_xpath(driver, '//*[@id="features"]/a')

            # Khởi tạo đối tượng sách
            book = {
                'id': generate_id(),
                'name': '',
                'description': '',
                'big_category': '',
                'small_category': '',
                'author': '',
                'NXB': '',
                'img': ''
            }

            # Lấy category
            print(random_color() + "Đang lấy category")
            book['big_category'] = driver.find_element(By.XPATH, '//*[@id="breadcrumbs_11"]/div/a[4]/bdi').text
            book['small_category'] = driver.find_element(By.XPATH, '//*[@id="breadcrumbs_11"]/div/a[5]/bdi').text
            print(random_color() + "Đã lấy xong category")

            # Lấy mô tả
            print(random_color() + "Đang lấy mô tả sách")
            time.sleep(1)
            description_div = driver.find_element(By.ID, 'content_description')
            paragraphs = description_div.find_elements(By.TAG_NAME, "p")
            for p in paragraphs:
                if p.text == 'Thông tin tác giả':
                    break
                book['description'] += p.text + '<br>'
            print(random_color() + "Đã lấy xong mô tả sách")

            driver.find_element(By.XPATH, '//*[@id="features"]/a').click()
            wait_xpath(driver, '//*[@id="content_features"]/div/div[4]/div[2]')

            # Lấy thông tin chi tiết
            print(random_color() + "Đang lấy thông tin sách")
            information = driver.find_elements(By.CLASS_NAME, 'ty-product-feature')
            for in4 in information:
                label = in4.find_element(By.CLASS_NAME, 'ty-product-feature__label')
                value = in4.find_element(By.CLASS_NAME, 'ty-product-feature__value')
                if label.text == 'Tác giả':
                    book['author'] = value.text
                elif label.text == 'Nhà Xuất Bản':
                    book['NXB'] = value.text

            # Lấy tên và hình ảnh sách
            book['name'] = driver.find_element(By.XPATH, '//*[@id="tygh_main_container"]/div[3]/div/div/div/div/div[1]/div[2]/div[1]/h1/bdi').text
            book['img'] = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/span/a/img').get_attribute("src")

            print(random_color() + "Đã lấy xong thông tin sách")

            # Ghi dữ liệu vào file với khóa
            print(random_color() + "Lưu thông tin vào file")
            with lock:
                with open('con_lai.json', 'a', encoding='utf-8') as f:
                    json.dump(book, f, ensure_ascii=False, indent=4)
                    f.write(',\n')

            print(random_color() + "Đã lưu thông tin vào file")

            # Quay lại trang trước
            driver.back()

        except Exception as e:
            print(f"Lỗi khi crawl sách thứ {i}: {e}")

    driver.quit()  # Đóng trình duyệt sau khi hoàn thành

# Danh sách các link
urls = [
    "https://nhasachphuongnam.com/manga-vi.html",
    "https://nhasachphuongnam.com/comic.html",
    "https://nhasachphuongnam.com/van-hoc-thieu-nhi.html",
    "https://nhasachphuongnam.com/truyen-co-tich-ngu-ngon.html",
    "https://nhasachphuongnam.com/to-mau-luyen-chu-cat-dan.html",
    "https://nhasachphuongnam.com/dao-duc-ky-nang-song.html",
    "https://nhasachphuongnam.com/sach-thieu-nhi-khac-vi-2.html",
   
]

# Chạy crawl cho từng link một
for url in urls:
    threads = []
    num_books = 50
    num_threads = 5
    books_per_thread = num_books // num_threads

    for i in range(num_threads):
        start = i * books_per_thread + 1
        end = (i + 1) * books_per_thread
        t = threading.Thread(target=crawl_books, args=(start, end, url))
        threads.append(t)

    # Chạy các luồng cho link hiện tại
    for t in threads:
        t.start()

    # Đợi tất cả các luồng hoàn thành cho link hiện tại
    for t in threads:
        t.join()

print("Đã hoàn thành crawl dữ liệu!")
