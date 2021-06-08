import bs4, requests
from urllib.request import urlopen, Request
import urllib.request
import re
from InterFunctions import switch_queue, switch_champions

message = input()

summoner = message[7:].split(", ")
info = [{}, {}, {}, {}, {}]
if len(summoner) != 5:
    print("ERROR")
else:

    summonerGroup = message[7:].lower().replace(", ", "%2C").replace(" ", "")
    url = "https://na.op.gg/multi/query=" + summonerGroup

    html = urllib.request.urlopen(url)

    opgg = bs4.BeautifulSoup(html, "html.parser")
    row = opgg.find_all("div", {"class": "MultiSearchResultRow tabWrap"})

    for i in range(5):
        raw_TierRank = row[i].find("div", {"class": "TierRank"})
        raw_MostChampionTable = row[i].find("div", {"class": "MostChampionStats tabItems"}).find("table", {"class": "Table"}).find("tbody", {"class": "Content"})

        info[i]["WinRatio"] = raw_TierRank.find("div", {"class": "WinRatio"}).text.replace("(", "").replace(")", "")
        info[i]["Wins"] = raw_TierRank.find("span", {"class": "Wins"}).text
        info[i]["Losses"] = raw_TierRank.find("span", {"class": "Losses"}).text
        info[i]["TierRank"] = raw_TierRank.find("div", {"class": "TierRank"}).text.replace("\n                                    ", "").split("\n")[0]
        info[i]["LP"] = raw_TierRank.find("span", {"class": "LP"}).text.replace("(", "").replace(")", "")

        raw_LastRank = row[i].find("div", {"class": "MultiSearchResultRowHeader"}).find_all("li")

        print(raw_LastRank)
        if len(raw_LastRank) == 1:
            info[i]["LastRank"] = raw_LastRank[0].text
        else:
            for raw_previous in raw_LastRank:
                raw_seasons.append(raw_previous.replace("<li>", "").replace("</li>", "")

        info[i]["Position"] = row[i].find("div", {"class": "RecentGameContent"}).find("div", {"class": "Position"}).find("div", {"class": "Content tip"}).find("span").text

        info[i]["MostChampion"] = raw_MostChampionTable.find("tr", "Row").find("div", {"class": "ChampionName"}).text

    print(info)


# ;clash evianB, Joknoopy, KR critic, byungmok123, existman512
