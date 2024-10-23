from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi động trình duyệt Chrome
driver = webdriver.Chrome()

# Mở trang web
driver.get("https://nhasachphuongnam.com/van-hoc-vi.html?sort_by=popularity&sort_order=desc&items_per_page=50")

def wait_xpath(xpath):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
def crawl():
    for i in range(1, 51):
        wait_xpath('//*[@id="categories_view_pagination_contents"]/div[1]')
        driver.find_element(By.XPATH, '//*[@id="categories_view_pagination_contents"]/div[1]').click()
        wait_xpath('//*[@id="features"]/a')
        # lay mo ta 
        description_div = driver.find_element(By.XPATH, '//*[@id="content_description"]/div')
        paragraphs = description_div.find_elements(By.TAG_NAME, "p")
        for p in paragraphs:
            print(p.text)

        driver.find_element(By.XPATH, '//*[@id="features"]/a').click()


try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ty-column4"))
    )
    print("Trang đã load xong.")
    
except:
    print("Không thể load trang.")

crawl()


