import json
import time
import random


from utils import get_driver_instance, login_instagram, check_remove_save_login_info_box, check_remove_notification_on_box, \
    click_home_button, search_and_open_profile, get_posts_on_page, open_post, load_all_comments, click_next_post, \
    unlike_random_comments, like_comments, send_telegram_message

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--username", help="the name os the user for which you want to runt he code for",
                    type=str)
args = parser.parse_args()


input_controls = json.load(open("input_controls.json"))[args.username]

instagram_credentials = {
    "username": input_controls["username"],
    "password": input_controls["password"]
    }

comments_likes_lower_limit = input_controls["comments_likes_lower_limit"]
comments_likes_upper_limit = input_controls["comments_likes_upper_limit"]
all_likes_duration = input_controls["all_likes_duration"]
max_posts_scrolls_per_influencer = input_controls["max_posts_scrolls_per_influencer"]
retry_wait_time = input_controls["retry_wait_time"]
wait_between_post_intervals = input_controls["wait_between_post_intervals"]
telegram_api = input_controls["telegram_api"]
telegram_group_id = input_controls["telegram_group_id"]
target_influencers = input_controls["target_influencers"]

instagram_url="https://www.instagram.com/"
API_URL = f"https://api.telegram.org/bot{telegram_api}"

print(f"Opening {instagram_url}")
driver = get_driver_instance(url=instagram_url)

print("loging in")
login_instagram(driver=driver, username=instagram_credentials["username"], password=instagram_credentials["password"])

print("check_remove_save_login_info_box")
check_remove_save_login_info_box(driver=driver)

print("check_remove_notification_on_box")
check_remove_notification_on_box(driver=driver)

print("click_home_button")
click_home_button(driver, instagram_url)


send_telegram_message(
                group_id=telegram_group_id, 
                message_text=f"New login for {input_controls['username']}", 
                api_url=API_URL
)

while True:
    try:
        target_influencer = random.choice(target_influencers)

        print(f"Searching and opening - {target_influencer}")
        search_and_open_profile(driver=driver, profile_username=target_influencer)

        print(f"getting first post (1) - {target_influencer}")
        all_posts = get_posts_on_page(driver=driver, max_posts=1)
        open_post(driver, all_posts[0])

        chosen_post_number = random.choice(range(1, max_posts_scrolls_per_influencer))
        print(f"Going to post number {chosen_post_number}")

        current_post_number = 1
        while current_post_number < chosen_post_number:
            # print(f"current post number - {current_post_number}")
            next_post_availability = click_next_post(driver)
            time.sleep(3)
            if next_post_availability == "No more posts":
                break
            current_post_number += 1
        
        print(f"Loading all comments - {target_influencer}")
        load_all_comments(driver)
        
        print(f"unlike random comments - {target_influencer}")
        unlike_random_comments(driver) 
        
        print(f"Like random comments - {target_influencer}")
        like_comments(
            driver=driver, 
            upper_limit=comments_likes_upper_limit, 
            lower_limit=comments_likes_lower_limit, 
            all_likes_duration=all_likes_duration, 
            telegram_group_id=telegram_group_id, 
            telegram_api_url=API_URL,
            target_influencer=target_influencer)
            
    
    except Exception as E:
        send_telegram_message(
            group_id=telegram_group_id, 
            message_text=f"Encountered error for {target_influencer}'s post in current run - {E} - Rerunning in 5 mins", 
            api_url=API_URL)

        time.sleep(retry_wait_time)
        
    driver.get(instagram_url + target_influencer)
    time.sleep(wait_between_post_intervals)


send_telegram_message(
    group_id=telegram_group_id, 
    message_text=f"Program crashed. It needs manual restart!!", 
    api_url=API_URL)