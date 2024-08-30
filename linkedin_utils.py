import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI() 

def get_all_questions(driver):
    questions_directory = "https://www.linkedin.com/pulse/topics/browse/m/"

    driver.get(questions_directory)
    time.sleep(5) 
    click_tab(driver=driver)
    # click_close_button(driver=driver)
    all_questions = get_all_questions_list(driver=driver)
    all_questions_df = pd.DataFrame(all_questions, columns=["questions"])
    all_questions_df.to_csv("allQuestions.csv", index=False)

def get_element(driver, element_xpath):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        time.sleep(2)
        return element
    except NoSuchElementException:
        print(f"Cannot find the element - {element_xpath}")
        return None

def input_text_in_element(element, text):
    # for i in list(text):
    element.send_keys(text)
        # time.sleep(0.01)

def press_escape(driver):
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)

        

def click_tab(driver, tab_name):
    try:
        driver.find_element(By.XPATH, f'//*[contains(text(), "{tab_name}")]').click()
        time.sleep(5)
    except NoSuchElementException:
        print(f"Cannot find the {tab_name} tab")
        None


def get_all_questions_list(driver):
    all_questions_list = []
    all_questions_list_elements = driver.find_elements(By.XPATH, "//*[@class='mb-1 overflow-hidden break-words font-sans text-lg font-[500] babybear:text-md']")
    for question_element in all_questions_list_elements:
        all_questions_list.append(question_element.text)
    return all_questions_list


def click_close_button(driver):
    try:
        driver.find_element(By.XPATH, '//*[local-name()="icon" and @class="contextual-sign-in-modal__modal-dismiss-icon lazy-loaded"]').click() 
        time.sleep(3)
    except NoSuchElementException:
        print("Cannot find the close button")
        time.sleep(3)
        None

def click_question(driver, question):
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), " + '"'+ question + '"' + ")]").click() 
        time.sleep(3)
    except NoSuchElementException:
        print(f"Cannot find the question {question}")
        time.sleep(3)
        None

def click_start_contribution(driver):
    try:
        driver.find_element(By.XPATH, '//button[@class="x-featured-section__start-contribution-button cursor-pointer pill "]').click() 
        time.sleep(3)
    except NoSuchElementException:
        print(f"Cannot find the start contribution button")
        time.sleep(3)
        None

def write_contribution(driver, answer):
    x_path = '//textarea[@class="contribution-text-area leading-normal placeholder:text-color-input-hint box-border w-full resize-none border-0 bg-color-transparent p-0 text-md leading-open tracking-wide text-color-text outline-none placeholder:text-color-text-disabled lg:text-lg"]'

    # div_xpath = '//div[@class="contribution-text-area-border ease-linear duration-300 mb-2 rounded-md border-1 border-solid border-[var(--color-input-container-border)] p-2 transition-all focus-within:shadow-border hover:shadow-border active:shadow-border-active md:px-3"]'

    try:
        input_area = driver.find_element(By.XPATH, x_path)
        for i in list(answer):
            input_area.send_keys(i)
            time.sleep(0.01)
        
        time.sleep(2)
        add_button_xpath = '//button[@class="submit-contribution-button ease-linear duration-300 btn-sm btn-primary transition-all lg:btn-md"]'
        add_button = driver.find_element(By.XPATH, add_button_xpath)
        

        if add_button:
            try:
                add_button.click()
            except Exception as E:
                driver.execute_script("arguments[0].click();", add_button)
        time.sleep(3)
    except NoSuchElementException:
        print(f"Cannot find the start contribution button")
        time.sleep(3)
        None

def login_linkedin(driver, username, password):
    username_input = driver.find_element(By.XPATH, '//input[@id="username"]')
    password_input = driver.find_element(By.XPATH, '//input[@id="password"]')

    for i in list(username):
        username_input.send_keys(i)
        time.sleep(0.1)

    for i in list(password):
        password_input.send_keys(i)
        time.sleep(0.1)

    time.sleep(2)

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(8)


def get_gpt_response(question):
    ans_len = 1000

    while ans_len > 700:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=130,
            messages=[
                {"role": "system", "content": 
                 "You are useful assistant that helps in writing linkedin content for expert contributions. "
                 "The response should be maximum 110 tokens."
                 "A user will ask you a question in which they are an expert. "
                 "They would then want to share the your answer with their linkedin audience. "
                 "Your response format for each of these questions should be in 3-4 small points. "
                 "Add a space of line between each of the points. "
                 "Give the post content as an exact answer and do not write anything else in the response. "
                 "The user should be able to directly copy your entire response and post it imediately without any modifications. "
                 "You can add a hook at the beginning of the response to catch the attention of the reader into reading the post. "
                 },
                {"role": "user", "content": question}
            ]
            )
        answer = completion.choices[0].message.content
        finish_reason = completion.choices[0].finish_reason

        print(f"length = {len(answer)} - reason - {finish_reason}")

        if finish_reason == "stop":
            answer = completion.choices[0].message.content
            answer = answer.replace("*", "")
            ans_len = len(answer)
            print(ans_len)
    return answer
    
