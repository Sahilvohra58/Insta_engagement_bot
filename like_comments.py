import time
import json
from datetime import datetime


from utils import get_driver_instance, login_instagram, check_remove_save_login_info_box, check_remove_notification_on_box, click_home_button, \
    search_and_open_profile, get_posts_on_page, open_post, find_and_click_close_button, load_all_comments, get_all_commented_users, \
    get_url_for_liked_people, get_all_liked_users, click_next_post, unlike_like_comments

# instagram_credentials = {
#     "username": "i3reminders",
#     "password": "Vadodara@1"
#     }

# instagram_credentials = {
#     "username": "greenarrowscaping",
#     "password": "Guelph@12"
#     }

instagram_credentials = {
    "username": "sahil2024insta",
    "password": "Guelph@1"
    }

# target_influencer = "heytony.agency"
target_influencer = "ibrahimhindy"
total_posts_scraped = 20
url="https://www.instagram.com/"

driver = get_driver_instance(url=url)

print("login")
login_instagram(driver=driver, username=instagram_credentials["username"], password=instagram_credentials["password"])

print("check_remove_save_login_info_box")
check_remove_save_login_info_box(driver=driver)

print("check_remove_notification_on_box")
check_remove_notification_on_box(driver=driver)

print("click_home_button")
click_home_button(driver, url)

print("search_and_open_profile")
search_and_open_profile(driver=driver, profile_username=target_influencer)

print("get_posts_on_page")
all_posts = get_posts_on_page(driver=driver, max_posts=1)

print("open_post")
open_post(driver, all_posts[0])

for _ in range(2):
    print("load_all_comments")
    load_all_comments(driver)
    
    print("unlike_like_comments-unlike")
    unlike_like_comments(driver, action="Unlike")    
    
    print("unlike_like_comments-like")
    unlike_like_comments(driver, action="Like")

    print("click_next_post")
    next_post_availability = click_next_post(driver)
    time.sleep(3)
    if next_post_availability == "No more posts":
        break