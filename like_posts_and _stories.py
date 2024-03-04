import time
import json
from datetime import datetime
import random
from selenium.webdriver.common.by import By


from utils import get_driver_instance, login_instagram, check_remove_save_login_info_box, check_remove_notification_on_box, click_home_button, \
    search_and_open_profile, get_posts_on_page, open_post, find_and_click_close_button, load_all_comments, get_all_commented_users, \
    get_url_for_liked_people, get_all_liked_users, check_followers_range, check_and_click_post_or_story_like_button, click_next_post, \
    click_profile_pic_for_story

# instagram_credentials = {
#     "username": "i3reminders",
#     "password": "Vadodara@1"
#     }

instagram_credentials = {
    "username": "greenarrowscaping",
    "password": "Guelph@12"
    }

# instagram_credentials = {
#     "username": "imam.mubeen",
#     "password": "Guelph@1"
#     }

posts_to_like_per_user=20
target_influencer = "ibrahimhindy"
total_followers_scraped = 2313
date_file_str = "2024_02_28"
json_file_name = f"scraped_output/scraped_followers_{target_influencer}_{total_followers_scraped}_{date_file_str}.json"


with open(json_file_name) as f:
    data = json.load(f)

driver = get_driver_instance(url="https://www.instagram.com/")


login_instagram(driver=driver, username=instagram_credentials["username"], password=instagram_credentials["password"])

check_remove_save_login_info_box(driver=driver)

check_remove_notification_on_box(driver=driver)


for target_username in data["scraped_followers"][8:15]:

    click_home_button(driver)

    user_found = search_and_open_profile(driver=driver, profile_username=target_username)
    if user_found == "User not found":
        continue 

    user_type = check_followers_range(driver, max_followers_count=7000)
    if user_type == "ordinary":

        # Like posts
        all_posts = get_posts_on_page(driver=driver, max_posts=1)
        if len(all_posts)>=1:

            open_post(driver=driver, post=all_posts[0])
            for _ in range(posts_to_like_per_user):

                check_and_click_post_or_story_like_button(driver)

                next_post_button_availability = click_next_post(driver)

                if next_post_button_availability == "No more posts":
                    find_and_click_close_button(driver)
                    break
                time.sleep(2)

            find_and_click_close_button(driver)
    
        click_profile_pic_for_story(driver, target_username)

        # Like stories
        while True:
            like_button_found = check_and_click_post_or_story_like_button(driver)
            if like_button_found == "No like button found":
                break
            next_post_button_availability = click_next_post(driver)
            time.sleep(1)

    time.sleep(4)
