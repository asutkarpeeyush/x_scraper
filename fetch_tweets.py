from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

USERNAME = "baloro6494"
PASSWORD = "baloro1994"
EMAIL = "baloro6494@ubinert.com"
TO_FETCH_USER = "alveus_dweller"
URL = f"https://twitter.com/search?q=from%3A%40{TO_FETCH_USER}%20-filter%3Aretweets%20-filter%3Areplies%20-filter%3Alinks"


def fetch_tweets_api():
    # Based on https://community.render.com/t/chromedriver-is-assuming-that-chrome-has-crashed/13237/7
    # Open chrome in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    # options.add_argument('--user-agent={}'.format('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'))
    driver = webdriver.Chrome(options=options) #type: WebDriver
    driver.get(URL)

    ##### Wait till login page appears ####
    # username page
    username_ele = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
    ) #type: WebElement
    username_ele.send_keys(USERNAME)
    button_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button']") #type: list[WebElement]
    for idx in range(len(button_elements)):
        if button_elements[idx].text == "Next": # Next button
            button_elements[idx].click()
            break
            # except StaleElementReferenceException:
            #     button_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")

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


    # At times, the email page comes up again, so wait like ~20 seconds for it.
    try:
        email_ele = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='email']"))
        )
        if email_ele:
            email_ele.send_keys(EMAIL)
            button_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button']") #type: list[WebElement]
            for button_ele in button_elements:
                if button_ele.text == "Next": # Next button
                    button_ele.click()
                    break
    except TimeoutException:
        print("Timeout exception surpassed")
        pass


    #### Wait till filtered timeline page appear ####
    # WebDriverWait(driver, 50).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Search timeline']"))
    # )
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tweetText']"))
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