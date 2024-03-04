import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def get_driver_instance(url):

    options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install(), 
            ),
            options=options
        )
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    return driver

def login_instagram(driver, username, password):
    username_input = driver.find_element(By.XPATH, '//input[@name="username"]')
    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')

    for i in list(username):
        username_input.send_keys(i)
        time.sleep(0.1)

    for i in list(password):
        password_input.send_keys(i)
        time.sleep(0.1)

    time.sleep(2)

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(8)


def check_remove_save_login_info_box(driver):
    try:
        driver.find_element(By.XPATH, '//*[contains(text(), "Not now")]').click()
        time.sleep(2)
    except NoSuchElementException:
        print("Cannot find the save_login_info_box")
        None


def check_remove_notification_on_box(driver):
    try:
        driver.find_element(By.XPATH, '//*[contains(text(), "Not Now")]').click()
        time.sleep(3)
    except NoSuchElementException:
        print("Cannot find the remove_notification_on_box")
        None

def click_home_button(driver, url):
    try:
        driver.find_element(By.XPATH, '//*[local-name()="svg" and @aria-label="Home"]').click() 
        time.sleep(3)
    except NoSuchElementException:
        print("Cannot find the home button")
        driver.get(url=url)
        time.sleep(3)
        None

def search_and_open_profile(driver, profile_username):
    driver.find_element(By.XPATH, '//*[local-name()="svg" and @aria-label="Search"]').click()
    time.sleep(3)

    search_bar = driver.find_element(By.XPATH, '//input[@aria-label="Search input"]')
    for i in list(profile_username):
        search_bar.send_keys(i)
        time.sleep(0.1)

    time.sleep(5)
    # driver.find_element(By.XPATH, f"""//img[@alt="{target_influencer}'s profile picture"]""").click()
    # driver.find_element(By.XPATH, f'//*[contains(text(), "{profile_username}")]').click()
    try:
        user = driver.find_element(By.XPATH, f'//a[@href="/{profile_username}/"]')
        if user:
            user.click()
        return_text = "User clicked"
    except NoSuchElementException:
        return_text= "User not found"
    time.sleep(4)
    return return_text

def get_posts_on_page(driver, max_posts):
    all_posts = driver.find_elements(By.XPATH, '//img[@style="object-fit: cover;"]')
    if len(all_posts)>=1:
        all_posts = all_posts[:max_posts]
    return all_posts

def open_post(driver, post):
    driver.execute_script("arguments[0].click();", post)
    time.sleep(2)

def click_next_post(driver):
    try:
        driver.find_element(By.XPATH, '//*[local-name()="svg" and @aria-label="Next"]').click()
        return None
    except NoSuchElementException:
        return "No more posts"


def find_and_click_close_button(driver):
    close_buttons = driver.find_elements(By.XPATH, '//*[local-name()="svg" and @aria-label="Close"]')
    for button in close_buttons:
        try:
            button.click()
        except:
            None
    time.sleep(2)

def load_all_comments(driver):
    try:
        while True:  
            try:
                while True:
                    driver.find_elements(By.XPATH, '//span[contains(text(), "View replies ")]')[0].click()
                    time.sleep(2)
            except:
                driver.find_element(By.XPATH, '//*[local-name()="svg" and @aria-label="Load more comments"]').click()
                time.sleep(2)
    except NoSuchElementException:
        None


def get_all_commented_users(driver):
    all_commented_users_list = []
    all_commented_users = driver.find_elements(By.XPATH, '//span[@class="xt0psk2"]')
    for user in all_commented_users:
        all_commented_users_list.append(user.text)
    return all_commented_users_list

def get_url_for_liked_people(driver):
    post_likes_link = driver.find_element(By.XPATH, '//a[contains(@href, "liked_by")]').get_attribute('href')
    return post_likes_link

def get_all_liked_users(driver):
    liked_users_list = []
    liked_people_element_list = driver.find_elements(By.XPATH, '//a[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd"]')

    for user in liked_people_element_list:
        username = user.get_attribute('href').split("/")[-2]
        liked_users_list.append(username)
    return liked_users_list

def check_followers_range(driver, max_followers_count):
    followers_count = driver.find_element(By.XPATH, '//span[@class="_ac2a" and @title]')
    title = followers_count.get_attribute("title")

    total_followers = int(title.replace(",", ""))
    if total_followers > max_followers_count:
        user_type = "influencer"
    else:
        user_type = "ordinary"

    return user_type


def check_and_click_post_or_story_like_button(driver):
    try:
        driver.find_element(By.XPATH, '//*[local-name()="svg" and @aria-label="Like" and @height=24 and @width=24]').click()
        time.sleep(2)
    except NoSuchElementException:
        return "No like button found"

def click_profile_pic_for_story(driver, target_username):
    driver.find_element(By.XPATH, f"""//img[@alt="{target_username}'s profile picture"]""").click()
    time.sleep(1)


# def like_comments(driver):
#     try:
#         comment_like_buttons_list = driver.find_elements(By.XPATH, '//*[local-name()="svg" and @aria-label="Like" and @height=12 and @width=12]')
#         for comment_like_button in comment_like_buttons_list:
#             if random.choice([True, False]):
#                 comment_like_button.click()
#                 time.sleep(1)
#     except NoSuchElementException:
#         return "No comments found to like" 

def unlike_like_comments(driver, action):
    try:
        comment_like_buttons_list = driver.find_elements(By.XPATH, f'//*[local-name()="svg" and @aria-label="{action}" and @height=12 and @width=12]')
        for comment_like_button in comment_like_buttons_list:
            if random.choice([True, False]):
                try:
                    comment_like_button.click()
                    time.sleep(2)
                except StaleElementReferenceException:
                    continue
    except NoSuchElementException:
        return f"No comments found to {action}" 