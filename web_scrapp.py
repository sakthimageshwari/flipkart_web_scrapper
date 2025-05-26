import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import json

mainURL = "https://www.flipkart.com/search?q=" 
categories = ['footware','clothing','home decor','sports products','watch','electronics','kitchen accessories']     
product_data = []

chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service('C:\\chromedriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)


def scrape_products():
    #products = driver.find_elements(By.XPATH, '//div[@class="_2kHMtA"]')
    #for product in products:
    try:
        #title = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[3]/div/div[1]/h1/span[2]').text
        title = driver.find_element(By.CLASS_NAME, 'VU-ZEz').text
        #price = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[3]/div/div[4]/div[1]/div/div[1]').text
        price = driver.find_element(By.CSS_SELECTOR, '.Nx9bqj.CxhGGd').text
        
        #--------------SUB-CATEGORY---------------
        a_elements = driver.find_elements(By.CLASS_NAME, 'R0cyWM') #to get the list of sub categories of a product
        anchor_data = [] 
        for a in a_elements:
            href = a.get_attribute('href')
            text = a.text
            anchor_data.append(re.sub(r'[^A-Za-z0-9\s]','',text))
        subcat = '; '.join(anchor_data[1:]) # merge all the a tag subcategory
        #--------------SUB-CATEGORY---------------

        #--------------PROD Description Click---------------
        #prod_descs = driver.find_elements(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[7]/div[2]/div/div/div[2]/div/div') #t7DWYS
        prod_descs = driver.find_elements(By.CSS_SELECTOR, '.col.col-11-12.rYpYQA') #t7DWYS
        if prod_descs: #checking for prod details
            for prod_desc in prod_descs:
                prod_desc.click()
            read_more = driver.find_elements(By.CSS_SELECTOR, ".QqFHMw.n4gy8q") #prod spec read more button #TODO: Change it to xpath
            if read_more:
                for element in read_more:
                    element.click()
        else: #fetch specification
            prod_descs = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[8]/div[2]/div/div[2]/div[1]') # for specifications
            for prod_desc in prod_descs:
                prod_desc.click()
            read_more = driver.find_elements(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[8]/div[2]/div/div[2]/button')
            if read_more:
                for element in read_more:
                    element.click()
        #--------------PROD Description Click---------------

        #fetching the product details 
        #--------------PROD Description Fetch---------------
        prod_details = driver.find_elements(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[7]/div[2]/div/div/div[2]/div/div')
        if prod_details:
            for element in prod_details:
                prod_details_txt = element.text
        else:
            prod_details = driver.find_elements(By.CSS_SELECTOR, '.sBVJqn')
            if prod_details:
                for element in prod_details:
                    prod_details_txt = element.text
        #--------------PROD Description Fetch---------------
        index = len(product_data) + 1
        product_data.append({
            'index': index,
            'title': title,
            'subcategoryDump': subcat,
            'price': price,
            'productdesc': prod_desc,
            'desc': prod_details_txt
        })
    except Exception as e:
        print(f"Error: {e}")
    return product_data

def openProductLink(new_url):
    driver.get(new_url)
    product_data = scrape_products()
    print(product_data)

def extractProductURLs(categoryURL):
    driver.get(categoryURL)
    a_elements = driver.find_elements(By.CLASS_NAME, 'rPDeLR')
    listofProducts = []
    counter = 0
    for a in a_elements:
        print("fetching the URL no: " + str(counter) )
        counter = counter + 1
        prod_url = a.get_attribute('href')
        if prod_url:
            listofProducts.append(prod_url) 
        
    return listofProducts
   
        
def fetchProdDetails(listofProducts):
    for prod_url in listofProducts:
        openProductLink(prod_url)

def main():
   # all_product_urls = []
   # all_product_data = []
    counter = 0
    for i in categories:
        print(i)
        categoryURL = mainURL + i
        for j in range(0,10):
            if counter == 0:
                listofProducts = extractProductURLs(categoryURL)
                fetchProdDetails(listofProducts)
              #  all_product_urls.extend(listofProducts)
                
            else:
                counter += 1
               # additional_listofProducts = extractProductURLs(categoryURL + "&page=2")
                extractProductURLs(categoryURL+"&page=2")
               # all_product_urls.extend(additional_listofProducts)
        break
    driver.quit()




if __name__ == "__main__":
    main()
    print('done')
    print(product_data)