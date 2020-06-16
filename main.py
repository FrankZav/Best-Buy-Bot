from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)
#driver.get("https://www.bestbuy.com/site/sony-interactive-entertainment-playstation-4-pro-1tb-limited-edition-the-last-of-us-part-ll-console-bundle-black/6414958.p?skuId=6414958")
driver.get("https://www.bestbuy.com/site/apple-watch-series-5-gps-44mm-space-gray-aluminum-case-with-black-sport-band-space-gray-aluminum/5706633.p?skuId=5706633")
#assert "PlayStation 4 Pro" in driver.title
snagged = False
try:
    while not snagged:
        
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-lg.add-to-cart-button"))
        )
        
        atc_button = driver.find_element_by_css_selector(".btn-lg.add-to-cart-button")
        
        if (atc_button.is_enabled()):
            atc_button.click()
            snagged=True
        else:
            print ("retry")
            driver.refresh()
finally:
    driver.close()
