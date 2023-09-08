# Import libraries and modules
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Firefox options, make it headless and set window size
options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')

def scrape_price_history(url):

    """
    Scrape price history data from a given company URL from Sharesansar.

    Args:
    url (str): The URL of the webpage containing price history data.

    Returns:
    tuple: A tuple containing lists of scraped data, including Date, Open, High, Low, Ltp, Per_Change, Qty, and Turnover.
    
    """
    
    # Initialize a Firefox webdriver with the specified options
    driver = webdriver.Firefox(options = options)

    # Open the provided URL in the browser
    driver.get(url)

    # Find and click on the "Price History" button
    price_history_button = driver.find_element("xpath", '//a[@id="btn_cpricehistory"]')
    price_history_button.click()
    time.sleep(1)

    # Find drop down and select to show 50 entries   
    show_50_entries = Select(driver.find_element("xpath", "//select[@name='myTableCPriceHistory_length']"))
    show_50_entries.select_by_visible_text('50')
    time.sleep(1)

    # Find pagination element and determine the number of pages
    pagination = driver.find_element("xpath", "//div[@id ='myTableCPriceHistory_paginate']")
    pages = pagination.find_elements("tag name", "a")
    last_page = int(pages[-2].text)

    current_page = 1

    # Initialize empty lists to store data
    Date = []
    Open = []
    High = []
    Low = []
    Ltp = []
    Per_Change = []
    Qty = []
    Turnover = []

    # Loop through all pages of the price history
    while current_page <= last_page:
        
        time.sleep(1)

        # Find all rows in the price history table
        price_history = driver.find_elements("xpath", "//table[@id='myTableCPriceHistory']/tbody/tr")

        # Extract data from each row and append it to the respective lists
        for price in price_history:
            
            Date.append(price.find_element("xpath", "./td[2]").text)
            Open.append(price.find_element("xpath", "./td[3]").text)
            High.append(price.find_element("xpath", "./td[4]").text)
            Low.append(price.find_element("xpath", "./td[5]").text)
            Ltp.append(price.find_element("xpath", "./td[6]").text)
            Per_Change.append(price.find_element("xpath", "./td[7]").text)
            Qty.append(price.find_element("xpath", "./td[8]").text)
            Turnover.append(price.find_element("xpath", "./td[9]").text)


        current_page += 1
        
        try:
            # Move to next page
            next_page = driver.find_element("xpath", "//a[@id='myTableCPriceHistory_next']")
            next_page.click()
        
        except:
            # If there's no next page, exit the loop
            pass

    # Quit the browser
    driver.quit()
    
    # Return the scraped data as a tuple
    return Date, Open, High, Low, Ltp, Per_Change, Qty, Turnover