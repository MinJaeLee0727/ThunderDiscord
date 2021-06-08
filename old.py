import discord
import random, os

import bs4, requests
from urllib.request import urlopen, Request
import urllib.request

client = discord.Client()

language = "English"
default_language = True
thunder_color = 0x0096ff
profix = ";"


@client.event
async def on_ready():
    print("login")
    print("----------------")
    print(client.user.name)
    print(client.user.id)
    print("----------------")
    await client.change_presence(game=discord.Game(name=';help', type=1))


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    # variables
    user = message.author.id
    channel = message.channel
    thunder_color = 0x0096ff

    summoner = {}

    global default_language, language

        if default_language:
            if message.content.startswith(';lang'):
                message = message.content[6:]
                if message == "KR":
                    language = "Korean"
                    await client.send_message(channel, "한국어로 변경되었습니다.")
                    default_language = False

                elif message == "EN":
                    language = "English"
                    await client.send_message(channel, "Default Language has been changed to English.")
                    default_language = False

                else:
                    await client.send_message(channel, "Current Language: " + language)

            else:
                embed = discord.Embed(title="Change Language", description="To start the bot, you should declare defualt language", color=thunder_color)
                embed.add_field(name=";lang status", value='Showing current language', inline=False)
                embed.add_field(name=";lang English", value='Default Language will remain as English', inline=False)
                embed.add_field(name=";lang KR", value='Default Language will change to Korean', inline=False)
                embed.add_field(name="Other languages", value='Sorry, English and Korean are only available now.')
                await client.send_message(channel, embed=embed)

        else:
            if message.content.startswith(';lang'):
                message = message.content[6:]
                if message == "KR":
                    language = "Korean"
                    await client.send_message(channel, "한국어로 변경되었습니다.")

                elif message == "EN":
                    language = "English"
                    await client.send_message(channel, "Default Language has been changed to English.")

                else:
                    await client.send_message(channel, "Current Language: " + language)

            else:
                if language == "English":
                    await client.send_message(channel, "Sorry, Not Available now.\rPlease use Korean")

                if language == "Korean":
                    if message.content == ';help':
                        embed = discord.Embed(title="Thunder", url="http://thunderweb.herokuapp.com",
                                              description="League of Legends stats and history provider",
                                              color=thunder_color)
                        embed.add_field(name="기본 기능", value='', inline=False)
                        embed.add_field(name=";안녕", value="say hello", inline=False)
                        embed.add_field(name=";주사위", value="1 ~ 6 사이의 정수를 무작위로 출력합니다.", inline=False)
                        embed.add_field(name=";랜덤선택 [항목] [항목] [...]", value="무작위로 항목을 선택합니다", inline=False)
                        embed.add_field(name=';팀선택', value='RED팀과 BLUE팀 중 하나를 선택합니다.', inline=False)
                        embed.add_field(name=';사다리타기 [항목] [항목] [...] / [항목] [항목] [...]',
                                        value='좌측 항목과 우측 항목을 무작위로 연결해줍니다.'
                                        , inline=False)
                        embed.add_field(name=';투표 [투표제목] /[항목1]/[항목2]/[...]', value='투표를 만듭니다.', inline=False)
                        embed.add_field(name=';날씨검색 (위치)', value='해당 위치의 현재 기온을 출력합니다. (naver)', inline=False)
                        embed.add_field(name=';롤 전적검색 (소환사 이름)', value='해당 소환사의 랭크를 출력합니다. (NA/ OP.GG)', inline=False)
                        embed.add_field(name=';members', value='이 서버의 멤버 이름들을 출력합니다.', inline=False)
                        embed.add_field(name=';익명 [내용]', value='익명으로서 메세지를 보냅니다.', inline=False)
                        embed.add_field(name=';계산기 [1항] [사칙연산] [2항]', value='단순한 사칙연산을 계산해줍니다.', inline=False)
                        embed.add_field(name=';사용자등록 [롤 닉네임]', value='롤 닉네임을 등록합니다.', inline=False)

                        await client.send_message(channel, embed=embed)

                    if message.content.startswith(";설정"):

                        if message.content == ";안녕":
                            await client.send_message(channel, "안녕하세요, <@" + user + ">님")

                        if message.content == ";주사위":
                            dice = random.randint(1, 6)
                            await client.send_message(channel, str(dice))

                        if message.content.startswith(';랜덤선택'):
                            choice = message.content.split(" ")
                            choicenumber = random.randint(1, len(choice) - 1)
                            choiceresult = choice[choicenumber]
                            await client.send_message(channel, choiceresult)

                        if message.content == ";팀선택":
                            team = ["RED", "BLUE"]
                            teamnumber = random.randint(0, 1)
                            await client.send_message(channel, " <@" + user + "> 님은 " + team[teamnumber] + "팀 입니다.")

                        if message.content.startswith(';메모장쓰기'):
                            data = message.content.split(";메모장쓰기 ")
                            file = open("DiscordNote.txt", "w")
                            file.write(data[1])
                            file.close()

                        if message.content.startswith(';메모장읽기'):
                            file = open("DiscordNote.txt")
                            await client.send_message(channel, file.read())
                            file.close()

                        if message.content.startswith(';사다리타기'):
                            team = message.content[7:]
                            peopleTeam = team.split("/")
                            people = peopleTeam[0]
                            team = peopleTeam[1]
                            person = people.split(" ")
                            print(person)
                            teamName = team.split(" ")
                            random.shuffle(teamName)
                            for i in range(0, len(person)):
                                await client.send_message(channel, person[i] + " --> " + teamName[i])

                        if message.content.startswith(';투표'):
                            vote = message.content[4:].split("/")
                            await client.send_message(channel, "투표 - " + vote[0])

                            for i in range(1, len(vote)):
                                votechoice = await client.send_message(channel, "```" + vote[i] + "```")
                                await client.add_reaction(message=votechoice, emoji='👍')

                        if message.content.startswith(';members'):
                            x = message.server.members
                            for member in x:
                                await client.send_message(channel,
                                                          member.name)  # you'll just print out Member objects your way.

                        if message.content.startswith(';날씨검색'):
                            learn = message.content.split(" ")
                            location = learn[1]
                            enc_location = urllib.parse.quote(location + '날씨')
                            hdr = {'User-Agent': 'Mozilla/5.0'}
                            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
                            req = Request(url, headers=hdr)
                            html = urllib.request.urlopen(req)
                            bsObj = bs4.BeautifulSoup(html, "html.parser")
                            todayBase = bsObj.find('div', {'class': 'main_info'})

                            todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
                            todayTemp = todayTemp1.text.strip()  # 온도
                            await client.send_message(channel, location + "의 현재 기온은 " + todayTemp + "도 입니다.")

                        if message.content.startswith(';롤 전적검색'):
                            summoner = message.content[8:]
                            print(summoner)
                            enc_summoner = urllib.parse.quote(summoner)
                            url = "https://na.op.gg/summoner/userName=" + enc_summoner
                            html = urllib.request.urlopen(url)

                            opgg = bs4.BeautifulSoup(html, "html.parser")

                            rank1 = opgg.find("div", {"class": "TierRankInfo"})
                            rank2 = rank1.find("div", {"class": "TierRank"})
                            rank4 = rank2.text.strip()
                            print(rank4)

                            point1 = rank1.find("div", {"class": "TierInfo"})
                            point2 = point1.find("span", {"class": "LeaguePoints"})
                            point3 = point2.text.strip()
                            print(point3)

                            # avg1 = opgg.find("td", {"class": "KDA"})
                            # avg2 = avg1.find("div", {"class": "KDARatio"})
                            # avg3 = avg2.find("span", {"class: KDARatio"})
                            # avg4 = avg3.text.strip()
                            # print(avg4)

                            #
                            # await client.send_message(message.channel, embed = embed)
                            embed = discord.Embed(title="롤 전적검색: " + summoner,
                                                  description=summoner + " 님은 " + rank4 + " " + point3 + " 입니다.",
                                                  color=0x00ff00)
                            await client.send_message(channel, embed=embed)

                        if message.content.startswith(';익명'):
                            args = message.content[3:]
                            await client.delete_message(message)
                            await client.send_message(channel, "???: " + args)

                        if message.content.startswith(';del'):
                            await client.delete_message(message)

                        if message.content.startswith(';계산기'):

                            terms = message.content[5:].split(" ")
                            firstTerms = int(terms[0])
                            arithmetics = terms[1]
                            secondTerms = int(terms[2])

                            if arithmetics == '+':
                                answer = firstTerms + secondTerms
                            if arithmetics == '-':
                                answer = firstTerms - secondTerms
                            if arithmetics == '/':
                                answer = firstTerms / secondTerms
                            if arithmetics == '*':
                                answer = firstTerms * secondTerms

                            print(answer, firstTerms, arithmetics, secondTerms)

                            await client.send_message(channel, str(answer) + "입니다.")

                        if message.content.startswith(';link') or message.content.startswith('링크'):
                            await client.send_message(channel, "https://thunderweb.herokuapp.com")

                        # if message.content.startswith(';add'):
                        #     summoner["summonerName"] = message.split[" "][1]
                        #     sum_result = {}
                        #
                        #     api_key = 'RGAPI-b408538f-4a26-4d36-a2bb-8f888adfd9cc'
                        #
                        #     summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(
                        #         summoner["summonerName"])  # 소환사 정보 검색
                        #     params = {'api_key': api_key}
                        #     res = requests.get(summoner_url, params=params)
                        #
                        #     # summoners_result = json.loads(((res.text).encode('utf-8')))
                        #     if res.status_code == requests.codes.ok:  # 결과값이 정상적으로 반환되었을때만 실행하도록 설정
                        #         summoner_exist = True
                        #         summoners_result = res.json()  # response 값을 json 형태로 변환시키는 함수
                        #         if summoners_result:
                        #             # 소환사 기본 정보
                        #             sum_result['name'] = summoners_result['name']
                        #             sum_result['level'] = summoners_result['summonerLevel']
                        #             sum_result['accountId'] = summoners_result['accountId']







access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

if not discord.opus.is_loaded():
    discord.opus.load_opus()