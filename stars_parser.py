from bs4 import BeautifulSoup
import requests
import re
import database
PORNHUB_URL = "https://www.pornhub.com"
def main():
    isNotEnded = True
    page = 1037
    while isNotEnded:
        counter = 1
        print(f"Parsing page:{page}")
        stars_page = requests.get(f"https://www.pornhub.com/pornstars?performerType=amateur&t=a&page={page}")
        page = page + 1
        soup = BeautifulSoup(stars_page.content, "html.parser")
        try:
            popularPornstars = soup.find("ul", {'id':"popularPornstars"}).find_all("li", {'class':"modelLi"})
        except:
            continue
        for star in popularPornstars:
            lists = list(popularPornstars)
            print(f"Scrapping {counter}/{lists.__len__()}")
            counter = counter + 1
            a =  star.find("div",{'class':'wrap'}).find("a",{'class':'js-mxp'})
            href = a.get("href")
            nickName = a.get("data-mxptext")
            try:
                personal_info_page = requests.get(PORNHUB_URL + href)
            except:
                continue
            PornStar = {
                "username":nickName,
                "url":PORNHUB_URL + href
            }
            good_soup = BeautifulSoup(personal_info_page.content, "html.parser")
            try:
                info_piece = good_soup.find("div",{"class":'content-columns js-highestChild columns-2'}).find_all("div",{"class":"infoPiece"})
            except:
                print(f"No info about {nickName}")
                continue
            try:
                for info in info_piece:
                        span = info.find("span").get_text().strip().replace(" ","").replace(":","")
                        small_info = info.find("span",{"class":'smallInfo'}).get_text().strip()
                        if span == "ProfileViews" or span == "VideosWatched" or span == "ProfileViews" or span == "VideoViews":
                            small_info = int(small_info.replace(",",""))
                        elif span == "Height":
                            heightSm =  re.search(r"\(([A-Za-z0-9_]+)\)", small_info)
                            heightSm = float(heightSm.group(1).replace("cm",""))
                            PornStar[span] = small_info
                            PornStar["HeightSm"] = heightSm
                            continue
                        elif span == "Weight":
                            weightLbs = float(small_info.split(" ")[0].replace("lbs.",""))
                            weightKg = re.search(r"\(([A-Za-z0-9_]+)\)", small_info)
                            weightKg = float(weightKg.group(1).replace("kg",""))
                            PornStar["WeightKg"] = weightKg
                            PornStar["WeightLbs"] = weightLbs
                            continue
                        PornStar[span] = small_info
                database.save_pornstars(PornStar)
            except Exception as e:
                print(e)
                continue

        if page == 1317:
            isNotEnded=False


            


    
if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print("Have some errors", e)
        pass
