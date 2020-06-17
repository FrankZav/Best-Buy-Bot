from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import json

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)
#driver.get("https://www.bestbuy.com/site/sony-interactive-entertainment-playstation-4-pro-1tb-limited-edition-the-last-of-us-part-ll-console-bundle-black/6414958.p?skuId=6414958")
driver.get("https://www.bestbuy.com/site/the-last-of-us-part-ii-standard-edition-playstation-4/6255399.p?skuId=6255399")

#load up buyer info from json file
f = open('./data/info.json',) 
buyer = json.load(f) 
snagged = False

def goToCheckout(driver):
    cartButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cart-nav"))
        )
    cartButton.click()
    checkOutButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-lg"))
        )
    checkOutButton.click()
    try:
        ageButton= WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Yes')]"))
        )
        ageButton.click()
    except NoSuchElementException:
        pass
    finally:
        guestButton = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "cia-guest-content__continue"))
            )
        guestButton.click()

def contactInfo(driver):
    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user.emailAddress")))
    phone = driver.find_element_by_id('user.phone')
    updates = driver.find_element_by_id('text-updates')
    try:
        firstname = driver.find_element_by_id("consolidatedAddresses.ui_address_2.firstName")
        lastname = driver.find_element_by_id("consolidatedAddresses.ui_address_2.lastName")
        address  = driver.find_element_by_id("consolidatedAddresses.ui_address_2.street")
        if buyer["street_address"]["apt"] != "":
            driver.find_element_by_class_name("address-form__showAddress2Link").click()
            apt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "consolidatedAddresses.ui_address_2.street2")))
        city = driver.find_element_by_id("consolidatedAddresses.ui_address_2.city")
        state = Select(driver.find_element_by_id("consolidatedAddresses.ui_address_2.state"))
        zip = driver.find_element_by_id("consolidatedAddresses.ui_address_2.zipcode")
    
        firstname.send_keys(buyer["street_address"]["firstname"])
        lastname.send_keys(buyer["street_address"]["lastname"])
        driver.find_element_by_class_name("autocomplete__toggle").click()
        address.send_keys(buyer["street_address"]["address"])
        if buyer["street_address"]["apt"] != "":
            apt.send_keys(buyer["street_address"]["apt"])
        city.send_keys(buyer["street_address"]["city"])
        state.select_by_value(buyer["street_address"]["state"])
        zip.send_keys(buyer["street_address"]["zip"])
    except NoSuchElementException:
        pass
    finally:
        email.send_keys(buyer["contact"]["email"])
        phone.send_keys(buyer["contact"]["phone"])
        updates.click()
        driver.find_element_by_class_name('btn-secondary').click()
    
def paymentInfo(driver):
    #FILL OUT CARD NUM FIRST
    card_num = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "optimized-cc-card-number")))
    card_num.send_keys(buyer["payment"]["card_number"])
    #THEN SELECT ALL TAGS TO FILL
    exp_month = Select(driver.find_element_by_name("expiration-month"))
    exp_year = Select(driver.find_element_by_name("expiration-year"))
    cvv = driver.find_element_by_id("credit-card-cvv")
    
    firstname = driver.find_element_by_id("payment.billingAddress.firstName")
    lastname = driver.find_element_by_id("payment.billingAddress.lastName")
    address  = driver.find_element_by_id("payment.billingAddress.street")
        
    city = driver.find_element_by_id("payment.billingAddress.city")
    state = Select(driver.find_element_by_id("payment.billingAddress.state"))
    zip = driver.find_element_by_id("payment.billingAddress.zipcode")

    exp_month.select_by_value(buyer["payment"]["expiration_date"]["month"])
    exp_year.select_by_value(buyer["payment"]["expiration_date"]["year"])
    cvv.send_keys(buyer["payment"]["cvv"])


    firstname.send_keys(buyer["billing_address"]["firstname"])
    lastname.send_keys(buyer["billing_address"]["lastname"])
    address.send_keys(buyer["billing_address"]["address"])
    if buyer["billing_address"]["apt"] != "":
        driver.find_element_by_class_name("address-form__showAddress2Link").click()
        apt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "payment.billingAddress.street2")))
        apt.send_keys(buyer["billing_address"]["apt"])
    city.send_keys(buyer["billing_address"]["city"])
    state.select_by_value(buyer["billing_address"]["state"])
    zip.send_keys(buyer["billing_address"]["zip"])

    ##driver.find_element_by_class_name("create-account__button")


while not snagged:
    try:        
        atc_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-lg.add-to-cart-button"))
        )
                
        if (atc_button.is_enabled()):
            atc_button.click()
            snagged=True
            sleep(1)
        else:
            print ("retry")
            driver.refresh()
    except:
        driver.refresh()
goToCheckout(driver)
contactInfo(driver)
paymentInfo(driver)