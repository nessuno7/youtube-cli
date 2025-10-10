from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..data_handlers import database_handler as dh
from ..data_handlers import json_handler
from ..data_handlers import channel_database_handler as cdh
import time
from ..config import clips_dir
from pathlib import Path
import shutil
import os



# Setup Selenium
def setup_driver():
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver


# Function to login into TikTok
def login_tiktok(driver, username, password):
    try:
        login_page_loaded = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='tiktok-1cp64nz-DivTextContainer e1cgu1qo3']")))
    except:
        driver.quit()
        print("Login page hasn't loaded after 10 seconds")

    login_button = driver.find_elements(By.XPATH, "//div[@class='tiktok-1cp64nz-DivTextContainer e1cgu1qo3']")
    login_button[1].click()
    
    email_login_button = driver.find_element(By.XPATH, "//a[@class='ep888o80 tiktok-1mgli76-ALink-StyledLink epl6mg0']")
    email_login_button.click()
    
    # Find username and input 
    login_input = driver.find_element(By.NAME, "username")
    login_input.send_keys(username)

    # Find password elemtn and input password
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='Password']")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    try:
        login_success = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Select video']")))
    except:
        print("Error: login failed due to captcha, required manual login with followinf credentials")
        print("username: ", {username})
        print("password: ", {password})
        success = input("Please confirm manual captcha was successfull [Y]/[n]: ")
        if(success != "Y"):
            print("program terminated due to unsucessful manual login")
            driver.quit()
    
    x= input("press anything to continue")



# Function to upload a video
def upload_video(driver, video_path, caption, count):
    select_video = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file'][@class='jsx-2995057667']")))
    select_video.send_keys(video_path)
    time.sleep(5)
    
    if count == 0:
        button = driver.find_element(By.XPATH, "//button[@class='Button__root Button__root--shape-default Button__root--size-medium Button__root--type-neutral Button__root--loading-false'][@data-type='neutral']")
        button.click()
        count = 1
    
    #try:
    #    login_success = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.xpath, "//a[contains(text(),'Replace' i)]")))
    #except:
    #    time.sleep(10)

    caption_element = driver.find_element(By.XPATH, "//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
    caption_element.click()
    for i in range(0,50):
        caption_element.send_keys(Keys.BACK_SPACE)
    caption_element.send_keys(caption)

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)") 
    
    time.sleep(1)
    
    post_button = driver.find_element(By.XPATH, "//button[@class='Button__root Button__root--shape-default Button__root--size-large Button__root--type-primary Button__root--loading-false'][@data-e2e='post_video_button']")
    post_button.click()
    time.sleep(1)


    return count



def create_caption(number, id):
    title = dh.fetch_title(id=id)
    caption = f"All credits to {json_handler.fetch_channel_name()}: "+title+" part "+number+f"/3 #fyp #foryoupage #viral #trending #explore #tiktok #tiktokvideo #{json_handler.fetch_database_name()}"
    return caption 

def post_clips(id):
    list_names = [f"clip_1_1_videoid_{id}.mp4", f"clip_1_2_videoid_{id}.mp4", f"clip_1_3_videoid_{id}.mp4", f"clip_2_1_videoid_{id}.mp4", f"clip_2_2_videoid_{id}.mp4", f"clip_2_3_videoid_{id}.mp4", f"clip_3_1_videoid_{id}.mp4", f"clip_3_2_videoid_{id}.mp4", f"clip_3_3_videoid_{id}.mp4"]

    driver = setup_driver()
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win64", webgl_vendor="AMD", fix_hairline=True, webdriver = False)

    try:
        is_logged_in = driver.find_element(By.ID, "main-content-homepage_hot")
    except:
        driver.get("https://www.tiktok.com/tiktokstudio/upload")
        login_tiktok(driver, cdh.fetch_username_by_name(), cdh.fetch_password_by_name())
    
    count  = 0
    for name in list_names:
        try:
            caption = create_caption(number=name[7], id=id)
            destination = Path.home() / json_handler.fetch_output_dir()
            path_ = destination / name
            if path_.exists() ==  False:
                create_copy(name, destination)
                while path_.exists() == False:
                    time.sleep(1)
            
            count = upload_video(driver=driver, video_path=os.path.normpath(path_), caption=caption, count=count)
            driver.get("https://www.tiktok.com/tiktokstudio/upload")
        except Exception as e:
            print(e)
            print(f"Some error while uploading video with name: {name}")
            print("Caption for manual input: ", caption)
            x = input("press to continue with uploads")
    
    dh.modify_clip(id=id, clip=True) #to know that the clips are posted
    if destination.exists():
        shutil.rmtree(destination)


def create_copy(name, destination):
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy(clips_dir / name, destination / name)