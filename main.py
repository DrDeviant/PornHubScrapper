
import pornhub_api
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from bs4 import BeautifulSoup
from video import Video
import requests
import pprint

VIEW_VIDEO_PATH = "https://www.pornhub.com/view_video.php?="

def start():
    api = PornhubApi()
    data = api.search.search(
    "russian",
    ordering="hot",
    period="weekly",
    tags=['black']
    )
    list_of_videos = []
    counter = 1
    for vid in data.videos:
        print(str(counter) + "/"+str(len(data.videos)) + vid.title)
        counter = counter + 1
        upVotes, downVotes, author = get_more_info_of_video(vid.video_id)
        video = Video(
            id=vid.video_id,
            title=vid.title,
            url=VIEW_VIDEO_PATH + vid.video_id,
            length=convert_to_time(vid.duration),
            histogram=None,
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
    for video in list_of_videos:
        print(video.__dict__)


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
    req = requests.get(VIEW_VIDEO_PATH + id)
    with open("//home//pi//PornHubScrapper//result.txt", "w", encoding="utf-8") as ss:
        ss.write(req.text)
    soup = BeautifulSoup(req.content, 'html.parser')
    votesUp = soup.find("span", {"class": "votesUp"}).get('data-rating')
    votesDown = soup.find("span", {"class": "votesDown"}).get('data-rating')
    author = soup.find("div",{"class": "userInfo"}).find("span",{"class":"usernameBadgesWrapper"}).get_text()
    return votesUp, votesDown, author

def convert_to_time(length):
    splitted = length.split(':')
    minutes = int(splitted[0])
    seconds = int(splitted[1])
    result = (minutes * 60) + seconds
    return result


#Possible ordering words: #mostviewed, newest, rating, featured
#weekly, monthly, alltime
if __name__=="__main__":
    start()
