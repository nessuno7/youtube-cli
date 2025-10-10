from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from ..data_handlers import database_handler as dbh
import sqlite3
import time

def setup_driver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win64", webgl_vendor="AMD", fix_hairline=True, webdriver = False)
    #driver.implicitly_wait(1)

    return driver


def accept_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc Gu558e']")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        accept_button = driver.find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc Gu558e']")
        accept_button.click()
    except:
        pass



def navigate_youtube_channel(driver, channel_name):
    driver.get(f"https://www.youtube.com/{channel_name}/videos")
    accept_cookies(driver=driver)
    

def navigate_single_video(url, driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    accept_cookies(driver=driver)


def recursive_addition(number_list):
    tot = 0
    power = len(number_list)-1
    for number in number_list:
        tot = int(''.join(map(str, number)))*10**power + tot
        power = power-1
    
    return tot



def string_into_time(timestr):
    time = list(timestr)
    i = 0

    number_list = []
    n_seconds = 0

    max = len(time)

    while i <= max:
        if i == max:
            n_seconds = n_seconds*60 + recursive_addition(number_list=number_list)            
        elif time[0] == ':':
            n_seconds = n_seconds*60 + recursive_addition(number_list=number_list)
            number_list= []
            time.pop(0)
        else:
            number_list.append(time[0])
            time.pop(0)
        i=i+1

    return n_seconds


def skip_ad(driver):
    try:
        skip_button = driver.find_element(By.XPATH, "//button[@class='ytp-skip-ad-button']")
        skip_button.click()
        return True
    except:
        return False
           

def wait_ads(driver):
    play_video(driver=driver)

    ad = True
    while ad == True:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='ytp-ad-player-overlay-layout']"))
            )
        except:
            ad = False
        
        if ad == True:
            try:
                duration_webelement = driver.find_element(By.XPATH, "//span[@class='ytp-time-duration']")
                duration = duration_webelement.text
                pause = string_into_time(timestr=duration)
                n_loops = int(pause/5) + 1
                for i in range(0, n_loops):
                    skip = skip_ad(driver=driver)
                    if skip == True:
                        break
                    else:
                        time.sleep(5)
            except:
                print("Non fatal Error: wait_ads()")



def check_before_years(string_list, max_depth):
    for i in range(0, len(string_list)):
        if i%2!=0:
            if max_depth in string_list[i].text and "years" in string_list[i].text:
                return True
    return False



def play_video(driver):
    try:
        play_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((driver.find_element(By.XPATH, "//button[@class='ytp-play-button ytp-button']")))
        )
        play_button.click()
    except:
        try:
            play_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((driver.find_element(By.XPATH, "//button[@data-tooltip-title='Play (k)']")))
            )
            play_button.click()
        except:
            print("Non fatal error: couldn't find play button")




def scroll_down_all_videos(driver, max_depth_search, channel_name):
    navigate_youtube_channel(driver=driver, channel_name=channel_name)

    previous = 0
    n_videos = 1

    webelement_links = []
    webelement_views_dates = []
    
    links = []
    views =[]
    dates = []
    titles = []
    stop = False
    
    while n_videos > previous and stop == False:
        previous = n_videos
        
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='video-title-link'][@class='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media']"))  # Replace with your target element
        )

        webelement_links = []
        webelement_links = driver.find_elements(By.XPATH, "//a[@id='video-title-link'][@class='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media']")
        n_videos = len(webelement_links)


        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='inline-metadata-item style-scope ytd-video-meta-block']"))  # Replace with your target element
        )
        webelement_views_dates = []
        webelement_views_dates = driver.find_elements(By.XPATH, "//span[@class='inline-metadata-item style-scope ytd-video-meta-block']")
        stop = check_before_years(string_list=webelement_views_dates, max_depth=max_depth_search)

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")        
    

    for link in webelement_links:
        links.append(link.get_attribute("href"))
        titles.append(link.get_attribute("title"))


    i = 0
    for i in range(0, len(webelement_views_dates)-1):
        if i%2 == 0:
            views.append(webelement_views_dates[i].text)
        else:
           dates.append(webelement_views_dates[i].text)

    driver.quit()

    links.pop(-1)
    views.pop(-1)
    titles.pop(-1)
    
    #print(len(links))
    #print(len(views))
    #print(len(dates))
    #print(len(titles))
    #print(len(durations))

   #saving to databse
    for i in range(0, len(links)-1):
        dbh.save_to_database(link=links[i], title=titles[i], views=views[i], heatmap="", duration = 0)

    
        

def scrape_heatmap(url, driver):
    navigate_single_video(url=url, driver=driver)
    wait_ads(driver=driver)
    play_video(driver=driver)

    progress_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ytp-progress-bar"))
    )
    ActionChains(driver).move_to_element(progress_bar).perform()

    try:
        heatmap_webelement = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-heat-map-path")))
        heatmap = heatmap_webelement.get_attribute("d")
        return heatmap
    except:
        print("Error: couldn't find heatmap")
        return ""
    
    


    
    

    





