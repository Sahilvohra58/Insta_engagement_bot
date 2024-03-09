import time
import random


from utils import get_driver_instance, login_instagram, check_remove_save_login_info_box, check_remove_notification_on_box, \
    click_home_button, search_and_open_profile, get_posts_on_page, open_post, load_all_comments, click_next_post, \
    unlike_random_comments, like_comments, send_telegram_message

instagram_credentials = {
    "username": "i3reminders",
    "password": "i3Institute!!!"
    }

# instagram_credentials = {
#     "username": "sahil2024insta",
#     "password": "Guelph@1"
#     }

comments_likes_lower_limit = 10
comments_likes_upper_limit = 15
all_likes_duration = 3420
max_posts_scrolls_per_influencer = 30
retry_wait_time = 240
wait_between_post_intervals = 60

telegram_api = "7186132763:AAHiIfZLvCEZ0f6XHj5nMuTI7tJrnK9Dfo4"
API_URL = f"https://api.telegram.org/bot{telegram_api}"
telegram_group_id = -4148825294
instagram_url="https://www.instagram.com/"

target_influencers = ["ibrahimhindy", "isna_canada", "scdawah", "mohammedhijabofficial", 
                      "thinkingmuslimpodcast", "5pillarsnews", "salhachimi", "thatmuslimguyy", 
                      "alidawah", "histopalestine", "mikaeelahmedsmith", "uticamasjid", "toxaidworker", 
                      "ieraorg", "shaykhalaa", "dilly.hussain88", "bloodxbrothers", "sacred_ummah", "themuslimcowboy", 
                      "the3muslims", "mradnanrashid", "asrarrashidofficial", "musaadnan", "asimkhan21c"]


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