from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

USERNAME = "baloro6494"
PASSWORD = "baloro1994"
TO_FETCH_USER = "alveus_dweller"
URL = f"https://twitter.com/search?q=from%3A%40{TO_FETCH_USER}%20-filter%3Aretweets%20-filter%3Areplies%20-filter%3Alinks"


def fetch_tweets_api():
    # TODO: Try https://community.render.com/t/chromedriver-is-assuming-that-chrome-has-crashed/13237/7 for headless
    # Open chrome in headless mode
    # driver_options = webdriver.ChromeOptions()
    # driver_options.add_argument("--headless=new")
    # driver_options.add_argument("--window-size=1024,600")
    # driver_options.add_argument("--allow-insecure-localhost")
    # driver_options.add_argument("--disable-gpu");
    # driver_options.add_argument("--no-sandbox");
    driver = webdriver.Chrome() #type: WebDriver
    driver.set_page_load_timeout(30)
    driver.get(URL)

    ##### Wait till login page appears ####
    # username page
    username_ele = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
    ) #type: WebElement
    username_ele.send_keys(USERNAME)
    button_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button']") #type: list[WebElement]
    for button_ele in button_elements:
        if button_ele.text == "Next": # Next button
            button_ele.click()
            break

    # password page
    password_ele = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']"))
    ) #type: WebElement
    password_ele.send_keys(PASSWORD)
    button_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button']") #type: list[WebElement]
    for button_ele in button_elements:
        if button_ele.text == "Log in": # Log in button
            button_ele.click()
            break


    #### Wait till filtered timeline page appear ####
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Search timeline']"))
    )
    elements = driver.find_elements(By.CSS_SELECTOR , "div[data-testid='tweetText']") #type: list[WebElement]
    tweets = []
    for element in elements:
        tweets.append(element.text)
    driver.quit()

    # TODO: Sentiment analysis on "tweets"
    
    return tweets

if __name__ == '__main__':
    print(fetch_tweets_api())