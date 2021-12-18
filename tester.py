from enum import auto
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def auto_filling_forms():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get("https://xxxsave.net/")
    element = driver.find_element_by_name("url")
    element.send_keys("https://rt.pornhub.com/view_video.php?viewkey=ph5d9e0632b1a7f")
    element = driver.find_element_by_id("bsubmit").click()
    time.sleep(1)
    pageSource = driver.page_source
    fileToWrite = open("page_source.txt", "w", encoding="utf-8")
    fileToWrite.write(pageSource)
    fileToWrite.close()
    parse_link_for_video(pageSource)

def parse_link_for_video(pageSource):
    soup = BeautifulSoup(pageSource, "html.parser")
    vdatas = soup.find("div",{"class":"mvdata"}).find_all("div",{"class":"vdata"})
    for data in vdatas:
        link = data.find("div",{"class":"link"}).find("a").get("href")
        if "unitube" in link:
            continue
        else:
            print(link)
        break


if __name__ == "__main__":
    auto_filling_forms()