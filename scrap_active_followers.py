import time
import json
from datetime import datetime
import random


from utils import get_driver_instance, login_instagram, check_remove_save_login_info_box, check_remove_notification_on_box, click_home_button, \
    search_and_open_profile, get_posts_on_page, open_post, find_and_click_close_button, load_all_comments, get_all_commented_users, \
    get_url_for_liked_people, get_all_liked_users, click_next_post

# instagram_credentials = {
#     "username": "i3reminders",
#     "password": "Vadodara@1"
#     }

instagram_credentials = {
    "username": "greenarrowscaping",
    "password": "Guelph@12"
    }

target_influencer = "heytony.agency"
# target_influencer = "ibrahimhindy"
total_posts_scraped = 20

driver = get_driver_instance(url="https://www.instagram.com/")


login_instagram(driver=driver, username=instagram_credentials["username"], password=instagram_credentials["password"])

check_remove_save_login_info_box(driver=driver)

check_remove_notification_on_box(driver=driver)

click_home_button(driver)

search_and_open_profile(driver=driver, profile_username=target_influencer)

all_posts = get_posts_on_page(driver=driver, max_posts=1)
targeted_followers = []
post_likes_links_list = []
open_post(driver, all_posts[0])

for n in range(total_posts_scraped):
    load_all_comments(driver)
    all_commented_users_list = get_all_commented_users(driver)
    print(f"Got all commented users {len(all_commented_users_list)}")
    targeted_followers.extend(all_commented_users_list)

    post_likes_link = get_url_for_liked_people(driver)
    post_likes_links_list.append(post_likes_link)

    next_post_availability = click_next_post(driver)
    time.sleep(3)
    if next_post_availability == "No more posts":
        break

for link in post_likes_links_list:
    driver.get(link)
    time.sleep(4)

    liked_users_list = get_all_liked_users(driver)
    print(f"Got all liked users {len(liked_users_list)}")

    targeted_followers.extend(liked_users_list)
    time.sleep(3)
    
    

targeted_followers = list(set(targeted_followers))

if target_influencer in target_influencer:
    targeted_followers.remove(target_influencer)

print(len(targeted_followers))
# print(targeted_followers)

scrap_data_dict={
    "target_influencer": target_influencer,
    "total_posts_scraped": total_posts_scraped,
    "date_on_scrape": datetime.strftime(datetime.now().date(), "%Y-%m-%d"),
    "total_followers_scraped": len(targeted_followers),
    "scraped_followers": targeted_followers
}

with open(f'scraped_output/scraped_followers_{target_influencer}_{str(len(targeted_followers))}_{datetime.strftime(datetime.now().date(), "%Y_%m_%d")}.json', 'w') as f:
    json.dump(scrap_data_dict, f)

input("end?")
