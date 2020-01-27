import discord
import random, os

import bs4, requests
from urllib.request import urlopen, Request
import urllib.request

# Youtube Play
import asyncio
import youtube_dl
import re

client = discord.Client()


@client.event
async def on_ready():
    print("login")
    print("----------------")
    print(client.user.name)
    print(client.user.id)
    print("----------------")
    await client.change_presence(game=discord.Game(name=';help', type=1))


que = {}
playerlist = {}
playlist = list()  # 재생목록 리스트


def queue(id):  # 음악 재생용 큐
    if que[id] != []:
        player = que[id].pop(0)
        playerlist[id] = player
        del playlist[0]
        player.start()


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    # variables
    user = message.author.id
    channel = message.channel

    # Advance commands
    if message.content == ";안녕":
        await client.send_message(message.channel, "안녕하세요, <@" + user + ">님")

    if message.content == ';help':
        embed = discord.Embed(title="Thunder", description="Thunder.gg의 League Discord Bot입니다.", color=0x00ff10)
        embed.add_field(name="WEB", description="thunder001.herokuapp.com", inline=False)
        # embed = discord.Embed(title="도움말", description="; 를 사용해 명령어를 부릅니다. EX: ;랜덤선택 빨강 파랑", color=0x00ff10)

        embed.add_field(name='\r;안녕', value='인사를 해줍니다.', inline=False)
        embed.add_field(name=';주사위', value='1 ~ 6 사이의 정수를 무작위로 출력합니다.', inline=False)
        embed.add_field(name=';랜덤선택 (항목) (항목) (...)', value='원하는 만큼 항목을 적으면 그 중 하나를 출력합니다.', inline=False)
        embed.add_field(name=';팀선택', value='RED팀과 BLUE팀 중 하나를 선택합니다.', inline=False)
        embed.add_field(name=';사다리타기 (항목) (항목) (...) / (항목) (항목) (...)', value='좌측 항목과 우측 항목을 무작위로 연결해줍니다.'
                        , inline=False)
        embed.add_field(name=';투표 (투표제목) /(항목1)/(항목2)/(...)', value='투표를 만듭니다.', inline=False)
        embed.add_field(name=';날씨검색 (위치)', value='해당 위치의 현재 기온을 출력합니다. (naver)', inline=False)
        embed.add_field(name=';롤 전적검색 (소환사 이름)', value='해당 소환사의 랭크를 출력합니다. (na.opgg)', inline=False)
        embed.add_field(name=';members', value='이 서버의 멤버 이름들을 출력합니다.', inline=False)
        embed.add_field(name=';익명 [내용]', value='익명으로서 메세지를 보냅니다.', inline=False)
        embed.add_field(name=';계산기 [1항] [사칙연산] [2항]', value='단순한 사칙연산을 계산해줍니다.', inline=False)

        await client.send_message(channel, embed=embed)

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
        data = message.content.split("/메모장쓰기 ")
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
            await client.send_message(channel, member.name)  # you'll just print out Member objects your way.

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

        # embed = discord.Embed(title="롤 전적검색: " + summoner, description = "이거슨 설명이라고 합니다!", color = 0x00ff00)
        #
        # await client.send_message(message.channel, embed = embed)
        embed = discord.Embed(title="롤 전적검색: " + summoner,
                              description=summoner + " 님은 " + rank4 + " " + point3 + " 입니다.", color=0x00ff00)
        await client.send_message(channel, embed=embed)

    if message.content.startswith(';익명'):
        args = message.content[3:]
        await client.delete_message(message)
        await client.send_message(channel, "???: " + args)

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








    # Music
    if message.content.startswith("!음악"):  # 음성채널에 봇을 추가 및 음악 재생
        msg = message.content.split(" ")
        try:
            url = msg[1]
            url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))',
                            url)  # 정규 표현식을 사용해 url 검사
            if url1 is None:
                await client.send_message(channel, embed=discord.Embed(title=":no_entry_sign: url을 제대로 입력해주세요.",
                                                                       colour=0x2EFEF7))
                return
        except IndexError:
            await client.send_message(channel,
                                      embed=discord.Embed(title=":no_entry_sign: url을 입력해주세요.", colour=0x2EFEF7))
            return

        voice_channel = message.author.voice.voice_channel
        server = message.server
        voice_client = client.voice_client_in(server)

        if client.is_voice_connected(server) and not playerlist[server.id].is_playing():  # 봇이 음성채널에 접속해있으나 음악을 재생하지 않을 때
            await voice_client.disconnect()
        elif client.is_voice_connected(server) and playerlist[server.id].is_playing():  # 봇이 음성채널에 접속해있고 음악을 재생할 때
            player = await voice_client.create_ytdl_player(url, after=lambda: queue(server.id), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            if server.id in que:  # 큐에 값이 들어있을 때
                que[server.id].append(player)
            else:  # 큐에 값이 없을 때
                que[server.id] = [player]
            await client.send_message(channel,
                                      embed=discord.Embed(title=":white_check_mark: 추가 완료!", colour=0x2EFEF7))
            playlist.append(player.title)  # 재생목록에 제목 추가
            return

        try:
            voice_client = await client.join_voice_channel(voice_channel)
        except discord.errors.InvalidArgument:  # 유저가 음성채널에 접속해있지 않을 때
            await client.send_message(channel,
                                      embed=discord.Embed(title=":no_entry_sign: 음성채널에 접속하고 사용해주세요.", colour=0x2EFEF7))
            return

        try:
            player = await voice_client.create_ytdl_player(url, after=lambda: queue(server.id), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            playerlist[server.id] = player
            playlist.append(player.title)
        except youtube_dl.utils.DownloadError:  # 유저가 제대로 된 유튜브 경로를 입력하지 않았을 때
            await client.send_message(channel,
                                      embed=discord.Embed(title=":no_entry_sign: 존재하지 않는 경로입니다.", colour=0x2EFEF7))
            await voice_client.disconnect()
            return
        player.start()

    if message.content == "!종료":  # 음성채널에서 봇을 나가게 하기
        server = message.server
        voice_client = client.voice_client_in(server)

        if voice_client == None:  # 봇이 음성채널에 접속해있지 않았을 때
            await client.send_message(channel,
                                      embed=discord.Embed(title=":no_entry_sign: 봇이 음성채널에 없어요.", colour=0x2EFEF7))
            return

        await client.send_message(channel,
                                  embed=discord.Embed(title=":mute: 채널에서 나갑니다.", colour=0x2EFEF7))  # 봇이 음성채널에 접속해있을 때
        await voice_client.disconnect()

    if message.content == "!스킵":
        id = message.server.id
        if not playerlist[id].is_playing():  # 재생 중인 음악이 없을 때
            await client.send_message(channel,
                                      embed=discord.Embed(title=":no_entry_sign: 스킵할 음악이 없어요.", colour=0x2EFEF7))
            return
        await client.send_message(message.channel, embed=discord.Embed(title=":mute: 스킵했어요.", colour=0x2EFEF7))
        playerlist[id].stop()

    if message.content == "!목록":

        if playlist == []:
            await client.send_message(channel,
                                      embed=discord.Embed(title=":no_entry_sign: 재생목록이 없습니다.", colour=0x2EFEF7))
            return

        playstr = "```css\n[재생목록]\n\n"
        for i in range(0, len(playlist)):
            playstr += str(i + 1) + " : " + playlist[i] + "\n"
        await client.send_message(channel, playstr + "```")










    #
    #
    # # Personal Basic commands
    # if message.content.startswith('안녕'):
    #     await  client.send_message(channel, "안녕하세요, <@" + user + ">님")
    #
    # if message.content.startswith('준섭이 아빠 이름은?'):
    #     await  client.send_message(channel, "이영세입니다.")
    #
    # if message.content.startswith('이영세 아들 이름은?'):
    #     await  client.send_message(channel, "이준섭입니다.")
    #
    # if message.content.startswith('난 누구게'):
    #     await  client.send_message(channel, user + "님 입니다.")
    #
    # if message.content.startswith('유영이는 누구'):
    #     await  client.send_message(channel, "")
    #
    # if message.content.startswith('병목이는 누구'):
    #     await  client.send_message(channel, "")
    #
    # if message.content.startswith('현우는 누구'):
    #     await  client.send_message(channel, "")
    #
    # if message.content.startswith('지훈이는 누구'):
    #     await  client.send_message(channel, "골드에요..")
    #
    # if message.content.startswith('교준이는 누구'):
    #     await  client.send_message(channel, "골드에요..")
    #
    # if message.content.startswith('교준이형은 누구'):
    #     await  client.send_message(channel, "골드에요..")
    #
    # if message.content.startswith('섹스'):
    #     await  client.send_message(channel, "변태 새끼입니다.")
    #
    # if message.content.startswith('민재는 누구'):
    #     await client.send_message(channel, "실버 새끼에요 아이디는 0727chris 이구요 비번은 ehsahdmwk2580이에요 올려보세요 가능하면...")
    #
    # if message.content.startswith('유현'):
    #     await client.send_message(channel, "니애미")
    #
    # if message.content.startswith('노민'):
    #     if message.content == "노민아":
    #         if message.author.id():
    #             await client.send_message(channel, "뭐 병신아")
    #     else:
    #         await client.send_message(channel, "어쩌라고")
    #
    # if message.content.startswith('노민이 아빠 이름은?'):
    #     await client.send_message(channel, "킹갓재너럴임패럴킹왕짱 민재에용")
    #
    # if message.content.startswith('사랑해'):
    #     await client.send_message(channel, "저도요, " + user + "님 ♡♡")
    # if message.content.startswith('유영이는?'):
    #     await client.send_message(channel, "씹쌔끼입니다.")


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

if not discord.opus.is_loaded():
    discord.opus.load_opus()