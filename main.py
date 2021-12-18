
import time
from fake_useragent import UserAgent
import pornhub_api
import re
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from bs4 import BeautifulSoup
from video import Video
import get_hist
from actionTag import ActionTag
import database
import requests
import pprint
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
 
VIEW_VIDEO_PATH = "https://rt.pornhub.com/view_video.php?viewkey="
def start():
    api = PornhubApi()
    isNotEnded = True
    page = 95
    while isNotEnded:
        start_time = time.time()
        data = api.search.search(
        ordering="mostviewed",
        period="alltime",
        page=page
        )
        list_of_videos = []
        counter = 1
        for vid in data.videos:
            print(str(counter) + "/"+str(len(data.videos)) + vid.title +" " + str(vid.views))
            counter = counter + 1
            try:
                pageSource, upVotes, downVotes, author,svg = get_more_info_of_video(vid.video_id)
            except Exception as e:
                print(e)
                continue
            video = Video(
                id=vid.video_id,
                title=vid.title,
                url=VIEW_VIDEO_PATH + vid.video_id,
                length=convert_to_time(vid.duration),
                histogram=get_hist.getPeaksTime(svg,convert_to_time(vid.duration) ),
                tags=get_lists_of_tags(vid.tags),
                category=get_list_of_categories(vid.categories),
                views = vid.views,
                dateAdded=vid.publish_date,
                dateUpdated=None,
                up_votes=upVotes,
                down_votes=downVotes,
                author=author
            )
            list_of_videos.append(video)
            try:
                get_data_tag_time_n_name(pageSource, video.id, video.length, video.author)
            except Exception as e:
                print(e, "get_data_tag")
                continue
                pass
            if video.url == "https://rt.pornhub.com/view_video.php?viewkey=ph585c74218308a":
                isNotEnded = False
        page = page + 1
        fileToWrite = open(f"page{str(page)}.txt", "w", encoding="utf-8")
        fileToWrite.write("--- %s seconds ---" % (time.time() - start_time))

def get_lists_of_tags(list_of_tags):
    result = []
    for tag in list_of_tags:
        result.append(tag.tag_name)
    return result

def get_list_of_categories(list_of_categories):
    result = []
    for category in list_of_categories:
        result.append(category.category)
    return result

def get_more_info_of_video(id):
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=op)
    driver.get(VIEW_VIDEO_PATH + id)
    pageSource = driver.page_source
    fileToWrite = open("page_source.txt", "w", encoding="utf-8")
    fileToWrite.write(pageSource)
    fileToWrite.close()
    soup = BeautifulSoup(pageSource)
    votesUp = soup.find("span", {"class": "votesUp"}).get('data-rating')
    votesDown = soup.find("span", {"class": "votesDown"}).get('data-rating')
    author = soup.find("div",{"class": "userInfo"}).find("div",{"class":"usernameWrap clearfix"}).get_text()
    svg = soup.find("div", {"class": "mgp_hotspots mgp_visible"}).find("polygon").get('points')
    return pageSource, int(votesUp), int(votesDown), author.replace("\n",''),svg

def convert_to_time(length):
    splitted = length.split(':')
    minutes = int(splitted[0])
    seconds = int(splitted[1])
    result = (minutes * 60) + seconds
    return result

def get_data_tag_time_n_name(pageSource, id, length, author):
    soup = BeautifulSoup(pageSource,"html.parser")
    all_tags = soup.find_all("div", {"class": "mgp_actionTag"})
    for tag in all_tags:
            dataTimeLine= float(tag.get('style').split(';')[0].split(':')[1].replace("%",''))
            tag = ActionTag(
                videoId=id,
                videoUrl=VIEW_VIDEO_PATH + id,
                author=author,
                dataTagName=tag.get('data-tag'),
                dataTagTime=length * dataTimeLine / 100
            )
            print(tag.__dict__)
            database.save_to_db(tag.__dict__)
            print("saved")

#Possible ordering words: #mostviewed, newest, rating, featured
#weekly, monthly, alltime


if __name__=="__main__":
    start()
